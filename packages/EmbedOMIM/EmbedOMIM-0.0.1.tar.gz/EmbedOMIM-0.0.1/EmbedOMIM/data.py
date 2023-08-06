import pandas as pd
import numpy as np
import torch
from scipy import sparse
import itertools
import pickle



class OMIMSymptomDataset:

	def __init__(self,disease_labels,symptom_freq_pairs,ordinal_freq_map,missing_label='NA'):
		"""Dataset that stores disease-symptom annotations as a sparse array that can be used for disease embedding.
		
		Args:
		    disease_labels (Array of Strings): Strings that make up the index of the disease dataset
		    symptom_freq_pairs (Array of iterables): Each list contains the symptoms-frequency pairs annotated to each disease. Symptoms-frequencies are stored as a tuple.
		    ordinal_freq_map (Dictionary): Dictionary providing ordinal rank of each frequency used to describe the symptoms. 
		    missing_label (str, optional): String used to denote missing frequency information.
		"""
		self.dataset=pd.DataFrame(columns=['SympFreqs'],index=disease_labels)
		orig_symp_values = pd.Series(symptom_freq_pairs,index=disease_labels)
		all_unique_symptoms=sorted(list(set().union(*orig_symp_values.apply(lambda x:[y[0] for y in x]).values)))
		self.symptom_map=dict(zip(all_unique_symptoms,range(len(all_unique_symptoms))))
		self.inverse_symptom_map=dict(zip(self.symptom_map.values(),self.symptom_map.keys()))
		self.ordinal_freq_map=ordinal_freq_map
		assert -1 not in ordinal_freq_map.values(),"-1 is not allowed as ordinal value for symptom frequency. This represents missing data in the model."
		self.ordinal_freq_map[missing_label]=-1

		new_symptoms = orig_symp_values.apply(lambda x: [(self.symptom_map[y[0]],self.ordinal_freq_map[y[1]]) for y in x])

		self.dataset['SympFreqs']=new_symptoms

	def SetNewTrainingState(self, training_fraction, validation_fraction):

		assert (training_fraction+validation_fraction)<=1.0,"Training and validation fraction added together cannot exceed 1.0"
		if (training_fraction+validation_fraction)==1.0:
		    print("Warning: Setting a model training state without allowing for a test fraction. There will be test fraction available for independent replication.")

		num_training_diseases=int(np.floor(training_fraction*self.dataset.shape[0]))
		num_validation_diseases=int(np.ceil(validation_fraction*self.dataset.shape[0]))
		num_testing_diseases=int(self.dataset.shape[0]-num_training_diseases-num_validation_diseases)

		self.training_index=pd.Index(np.random.choice(self.dataset.index,size=num_training_diseases,replace=False))
		if (num_training_diseases+num_validation_diseases)==self.dataset.index.shape[0]:
		    self.validation_index=self.dataset.index.difference(self.training_index)
		else:
		    self.validation_index=pd.Index(np.random.choice(self.dataset.index.difference(self.training_index),size=num_validation_diseases,replace=False))

		self.testing_index=self.dataset.index.difference(np.union1d(self.training_index,self.validation_index))

		self.training_index=self.training_index.values
		self.validation_index=self.validation_index.values
		self.testing_index=self.testing_index.values

	def ShuffleTrainingValidation(self):
		combined_index=np.concatenate([self.training_index,self.validation_index])
		np.random.shuffle(combined_index)
		self.training_index=combined_index[0:self.training_index.shape[0]]
		self.validation_index=combined_index[self.training_index.shape[0]:]

	def SaveTrainingState(self,fName):
		if fName[-4:]!='.pth':
			fName+='.pth'
		currentState = dict()
		currentState['training_index']=self.training_index
		currentState['validation_index']=self.validation_index
		currentState['testing_index']=self.testing_index

		with open(fName, 'wb') as f:
			pickle.dump(currentState,f)

	def LoadTrainingState(self,fName):
		if fName[-4:]!='.pth':
			fName+='.pth'

		with open(fName, 'rb') as f:
			currentState = pickle.load(f)

		self.training_index=currentState['training_index']
		self.validation_index=currentState['validation_index']
		self.testing_index=currentState['testing_index']

		assert np.setdiff1d(np.union1d(np.union1d(self.training_index,self.validation_index),self.testing_index),self.dataset.index.values).shape[0]==0,"Index of stored and loaded state do not match."




	def _torchWrapper(self,x):
		"""
		Note, all torch floating point tensors are converted to 32-bits to
		ensure GPU compatibility.
		"""

		if x.dtype==np.float32:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.float32)
		    else:
		        return torch.tensor(x,dtype = torch.float32)

		elif x.dtype==np.float64:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.float32)
		    else:
		        return torch.tensor(x,dtype = torch.float32)
		else:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.long)
		    else:
		        return torch.tensor(x,dtype = torch.long)


	def _return_coo_matrix(self,index=[]):

		if len(index)==0:
		    index = self.dataset.index

		x_inds = list(itertools.chain.from_iterable([[i]*len(x) for i,x in enumerate(self.dataset.loc[index]['SympFreqs'])]))
		y_inds= list(itertools.chain.from_iterable(self.dataset.loc[index]['SympFreqs'].apply(lambda x: [y[0] for y in x])))
		values_freqs= list(itertools.chain.from_iterable(self.dataset.loc[index]['SympFreqs'].apply(lambda x: [y[1] for y in x])))

		values_symps= np.ones((len(x_inds)))

		return sparse.coo_matrix((values_symps,(x_inds,y_inds)),shape=(len(index),len(self.symptom_map)),dtype=np.float32),sparse.coo_matrix((values_freqs,(x_inds,y_inds)),shape=(len(index),len(self.symptom_map)),dtype=np.float32)

	def ReturnDataArrays(self,index,useTorch=True):
		"""Returns symptoms and frequencies alinged to index diseases as a pair of torch tensors. Missing data in the frequencies is denoted using -1.
		
		Args:
		    index (TYPE): list/array of indices.
		"""

		symp_incidence_array, symp_freq_array=self._return_coo_matrix(index)
		if useTorch:
			return self._torchWrapper(symp_incidence_array),self._torchWrapper(symp_freq_array)
		else:
			return symp_incidence_array, symp_freq_array

	def DropSymptoms(self,symptom_list):

		oldSymptomToIntMap=self.symptom_map

		allSymptoms=set(oldSymptomToIntMap.keys())

		removedSymptoms=set(symptom_list)

		assert len(removedSymptoms.difference(allSymptoms))==0, "Symptoms: {0:s} not in set of possible symptoms.".format(','.join(list(removedSymptoms.difference(allSymptoms))))

		keptInts = set([oldSymptomToIntMap[x] for x in allSymptoms.difference(symptom_list)])


		for old_symp in removedSymptoms:
		    del oldSymptomToIntMap[old_symp]

		newSymptomToIntMap = {}
		oldToNewIntMap={}
		for i,key in enumerate(oldSymptomToIntMap):
			oldToNewIntMap[oldSymptomToIntMap[key]]=i
			newSymptomToIntMap[key] = i


		self.symptom_map=newSymptomToIntMap
		self.dataset['SympFreqs']=self.dataset['SympFreqs'].apply(lambda x: [(oldToNewIntMap[y[0]],y[1]) for y in x if y[0] in keptInts])

	def DropDiseases(self, disease_list):
		disease_list=pd.Index(disease_list)
		assert len(disease_list.difference(self.dataset.index))==0,"Subjects: {0:s} not in data table.".format(','.join(list(disease_list.difference(self.dataset.index))))
		self.dataset.drop(index=disease_list,inplace=True)


	def FindAllDiseases_wSymptom(self,symptom):

		if symptom not in self.symptom_map.keys():
			raise KeyError("Symptom {0:s} not in possible set.".format(symptom))
		else:
			intVal = self.symptom_map[symptom]
			return self.dataset.index[self.dataset['SympFreqs'].apply(lambda x: intVal in set([y[0] for y in x]))]


