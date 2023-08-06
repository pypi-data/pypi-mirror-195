import pandas as pd
import numpy as np
import torch
import pickle
import pyro
import copy

from .model import DiseaseVAE
from .data import OMIMSymptomDataset
from .optim import AutoEncoderOptimizer

__version__ = "0.0.1"


class EmbedOMIM:

	def _readModelFromFile(self,fName):
		with open(fName,'rb') as f:
			model_dict = torch.load(f,map_location='cpu')
		return model_dict


	def __init__(self,diseaseDataset,nLatentDim,isLinear=True,**kwargs):
		self.diseaseDataset = diseaseDataset

		self.all_model_kwargs = kwargs

		if 'encoder_hyperparameters' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['encoder_hyperparameters']={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True}
		if 'decoder_hyperparameters' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['decoder_hyperparameters']={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True}

		if 'missing_freq_priors' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['missing_freq_priors']=[0.0,3.0]

		if 'frequency_cut_points' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['frequency_cut_points']=[0.04,0.3,0.8,0.99]
		assert (len(self.all_model_kwargs['frequency_cut_points'])+1)==(len(self.diseaseDataset.ordinal_freq_map)-1), "Number of model cutpoints must equal number frequency classes in dataset, excluding the Unknown class"

		self.nLatentDim=nLatentDim
		self.isLinear=isLinear
		self.numSymptoms=len(self.diseaseDataset.symptom_map)
		self.numFreqCats=len(self.diseaseDataset.ordinal_freq_map)-1

		self.embed_model=DiseaseVAE(self.numSymptoms,self.numFreqCats,self.nLatentDim,isLinear=self.isLinear,encoder_hyperparameters=self.all_model_kwargs['encoder_hyperparameters'],decoder_hyperparameters=self.all_model_kwargs['decoder_hyperparameters'],missing_freq_prior_mean=self.all_model_kwargs['missing_freq_priors'][0],missing_freq_prior_scale=self.all_model_kwargs['missing_freq_priors'][1],cut_points=self.all_model_kwargs['frequency_cut_points'])


	def FitModel(self,batch_size,logFile=None,verbose=True,**kwargs):
		"""


		Parameters
		----------


		batch_size : int,
		    Size of dataset batches for inference. 

		verbose : bool, optional
		    Indicates whether or not to print (to std out) the loss function values and error after every epoch. The default is True.

		logFile: str, optional

		    File to log model fitting process.

		Keyword Parameters
		----------
		maxLearningRate: float, optional
		    Specifies the maximum learning rate used during inference. Default is 0.05

		errorTol: float, optional
		    Error tolerance in ELBO (computed on held out validation data) to determine convergence. Default is 1e-4.

		numParticles: int, optional
		    Number of particles (ie random samples) used to approximate gradient. Default is 1. Computational cost increases linearly with value.

		maxEpochs: int, optional
		    Maximum number of epochs (passes through training data) for inference. Note, because annealing and learning rate updates depend on maxEpochs, this offers a simple way to adjust the speed at which these values change. Default is 200.

		computeDevice: str or None, optional
		    Specifies compute device for inference. Default is None, which instructs algorithm to use cpu. Two other options are supported: 'cuda' and 'mps'. Note, if device number is not included (ex: 'cuda:0'), then it is automatically assumed to be '0'

		numDataLoaders: int
		    Specifies the number of threads used to process data and prepare for upload into the gpu. Note, due to the speed of gpu, inference can become limited by data transfer speed, hence the use of multiple DataLoaders to improve this bottleneck. Default is 0, meaning just the dedicated cpu performs data transfer.

		OneCycleParams: dict with keys 'pctCycleIncrease','initLRDivisionFactor','finalLRDivisionFactor'
		    Parameters specifying the One-Cycle learning rate adjustment strategy, which helps to enable good anytime performance.
		    pctCycleIncrease--fraction of inference epochs used for increasing learning rate. Default: 0.1
		    initLRDivisionFactor--initial learning rate acheived by dividing maxLearningRate by this value. Default: 25.0
		    finalLRDivisionFactor--final learning rate acheived by dividing maxLearningRate by this value. Default: 1e4


		KLAnnealingParams: dict with keys 'initialTemp','maxTemp','fractionalDuration','schedule'
		    Parameters that define KL-Annealing strategy used during inference, important for avoiding local optima. Note, annealing is only used for computation of ELBO and gradients on training data. Validation data ELBO evaluation, used to monitor convergence, is performed at the maximum desired temperature (typically 1.0, equivalent to standard variational inference). Therefore, it is possible for the model to converge even when the temperature hasn't reached it's final value. It's also possible that further cooling would find a better optimum, but this is highly unlikely in practice.
		    initialTemp--initial temperature during inference. Default: 1.0 (no annealing)
		    maxTemp--final temperature obtained during inference. Default: 1.0 (standard variational inference)
		    fractionalDuration--fraction of inference epochs used for annealing. Default is 0.25
		    schedule--function used to change temperature during inference. Defualt is 'cosine'. Options: 'cosine','linear'



		Returns
		-------
		output : list
		    List containing the following information: [loss function value of best model (computed on validation data),sequence of training loss values, sequence of validation loss values, error estimates across iterations (computed on validation data)].



		"""


		######### Parse Keyword Arguments #########
		allKeywordArgs = list(kwargs.keys())


		if 'maxLearningRate' in allKeywordArgs:
		    maxLearningRate=kwargs['maxLearningRate']
		else:
		    maxLearningRate=0.05


		if 'errorTol' in allKeywordArgs:
		    errorTol=kwargs['errorTol']
		else:
		    errorTol=1e-4

		if 'numParticles' in allKeywordArgs:
		    numParticles=kwargs['numParticles']
		else:
		    numParticles=1


		if 'maxEpochs' in allKeywordArgs:
		    maxEpochs=kwargs['maxEpochs']
		else:
		    maxEpochs=500


		if 'computeDevice' in allKeywordArgs:
		    computeDevice=kwargs['computeDevice']
		else:
		    computeDevice=None

		if 'numDataLoaders' in allKeywordArgs:
		    numDataLoaders=kwargs['numDataLoaders']
		    if computeDevice in [None,'cpu']:
		        assert numDataLoaders==0,"Specifying number of dataloaders other than 0 only relevant when using GPU computing"
		else:
		    numDataLoaders=0

		if 'OneCycleParams' in allKeywordArgs:
		    OneCycleParams=kwargs['OneCycleParams']
		    assert set(OneCycleParams.keys())==set(['pctCycleIncrease','initLRDivisionFactor','finalLRDivisionFactor']),"One-cycle LR scheduler requires the following parameters:'pctCycleIncrease','initLRDivisionFactor','finalLRDivisionFactor'"

		else:
		    OneCycleParams={'pctCycleIncrease':0.1,'initLRDivisionFactor':25.0,'finalLRDivisionFactor':1.0}

		if 'KLAnnealingParams' in allKeywordArgs:
		    KLAnnealingParams=kwargs['KLAnnealingParams']
		    assert set(KLAnnealingParams.keys())==set(['initialTemp','maxTemp','fractionalDuration','schedule']),"KL Annealing Parameters must be dictionary with the following keys: 'initialTemp','maxTemp','fractionalDuration','schedule'"
		else:
		    KLAnnealingParams={'initialTemp':0.0,'maxTemp':1.0,'fractionalDuration':0.25,'schedule': 'cosine'}


		if 'EarlyStopPatience' in allKeywordArgs:
			EarlyStopPatience=kwargs['EarlyStopPatience']
		else:
			EarlyStopPatience=np.inf


		pyro.clear_param_store()

		optimizer=AutoEncoderOptimizer(self.embed_model,self.diseaseDataset,optimizationParameters={'maxLearningRate': maxLearningRate,'maxEpochs': maxEpochs,'numParticles':numParticles},computeConfiguration={'device':computeDevice,'numDataLoaders':numDataLoaders},OneCycleParams=OneCycleParams,KLAnnealingParams=KLAnnealingParams)
		output=optimizer.BatchTrain(batch_size,errorTol=errorTol,verbose=verbose,logFile=logFile,early_stop_patience=EarlyStopPatience)
		print('Inference complete. Final Loss: {0:10.2f}'.format(output[0]))
		return output


	def EmbedOMIMDiseases(self,index=None,hpo_freq_pairs=None,returnStdErrors=False):
		assert (index is not None) ^ (hpo_freq_pairs is not None),"Must provide either index or HPO-frequency pairs to generate data."

		if index is not None:
			data=self.diseaseDataset.ReturnDataArrays(index)
			keys=list(index)
		else:
			#generate data tensors
			annot_array=torch.zeros((len(hpo_freq_pairs),self.numSymptoms),dtype=torch.float32)
			freq_array=torch.zeros((len(hpo_freq_pairs),self.numSymptoms),dtype=torch.float32)

			keys=[]

			for t,(d_id,hpo_freq_vec) in enumerate(hpo_freq_pairs.items()):
				keys+=[d_id]
				idx_vec=[self.diseaseDataset.symptom_map[x[0]] for x in hpo_freq_vec]
				freq_vec=[self.diseaseDataset.ordinal_freq_map[x[1]] for x in hpo_freq_vec]
				annot_array[t,idx_vec]=1.0
				freq_array[t,idx_vec]=torch.tensor(freq_vec,dtype=torch.float32)
			data=(annot_array,freq_array)
		p_m,p_std=self.embed_model.posterior_latent_state(*data)


		if returnStdErrors:
			p_m_df=pd.DataFrame(p_m.detach().numpy(),columns=['LD:{0:d}'.format(d) for d in range(self.nLatentDim)],index=keys)
			p_std_df=pd.DataFrame(p_std.detach().numpy(),columns=['LD:{0:d}'.format(d) for d in range(self.nLatentDim)],index=keys)
			output = dict([(col,list(zip(p_m_df[col], p_std_df[col]))) for col in p_m_df])
			return pd.DataFrame(output, index=keys)

		else:
			return pd.DataFrame(p_m.detach().numpy(),columns=['LD:{0:d}'.format(d) for d in range(self.nLatentDim)],index=keys)


	def EstimateMissingAnnotationRates(self,index=None,hpo_freq_pairs=None):
		assert (index is not None) ^ (hpo_freq_pairs is not None),"Must provide either index or HPO-frequency pairs to generate data."

		mapping_dict={}
		if index is not None:
			data=self.diseaseDataset.ReturnDataArrays(index)
			for i,d_id in enumerate(index):
				mapping_dict[d_id]=torch.where(data[0][i]==1.0)[0]
		else:
			for d_id,hpo_freq_vec in hpo_freq_pairs.items():
				mapping_dict[d_id]=torch.tensor([self.diseaseDataset.symptom_map[x[0]] for x in hpo_freq_vec],dtype=torch.long)

		posterior_table=self.EmbedOMIMDiseases(index=index,hpo_freq_pairs=hpo_freq_pairs,returnStdErrors=True)

		output_dictionary={}
		for dis,post_vec in posterior_table.iterrows():
			embed_tensor=torch.tensor([x[0] for x in post_vec],dtype=torch.float32)
			pred_missing_full=self.embed_model.missing_freq_disease_decoder(embed_tensor)+self.embed_model.missing_freq_intercepts_post_mean
			pred_missing=torch.sigmoid(pred_missing_full[mapping_dict[d_id]]).detach().numpy()
			output_dictionary[dis]=list(zip([self.diseaseDataset.inverse_symptom_map[x] for x in mapping_dict[d_id].detach().numpy()],pred_missing))
		return output_dictionary


	def ImputeMissingSymptomFrequencies(self,index=None,hpo_freq_pairs=None,useExpectationApprox=True,num_samples=100):
		assert (index is not None) ^ (hpo_freq_pairs is not None),"Must provide either index or HPO-frequency pairs to generate data."

		missing_dict={}
		if index is not None:
			data=self.diseaseDataset.ReturnDataArrays(index)
			for i,d_id in enumerate(index):
				missing_dict[d_id]=torch.where(data[1][i]==-1.0)[0]
		else:
			#generate data tensors

			for d_id,hpo_freq_vec in hpo_freq_pairs.items():
				missing_dict[d_id]=torch.tensor([self.diseaseDataset.symptom_map[x[0]] for x in hpo_freq_vec if x[1]=='NA'],dtype=torch.long)

		posterior_table=self.EmbedOMIMDiseases(index=index,hpo_freq_pairs=hpo_freq_pairs,returnStdErrors=True)

		output_dictionary={}
		for dis,post_vec in posterior_table.iterrows():
			if useExpectationApprox:
				embed_tensor=torch.tensor([x[0] for x in post_vec],dtype=torch.float32)
				pred_class_full=pyro.distributions.OrderedLogistic(self.embed_model.symptom_frequency_decoder(embed_tensor),self.embed_model.cut_points).logits
				pred_annots=torch.exp(pred_class_full[missing_dict[d_id],:]).detach().numpy()
			else:
				pm=torch.tensor([x[0] for x in post_vec],dtype=torch.float32)
				ps=torch.tensor([x[1] for x in post_vec],dtype=torch.float32)
				samples=pyro.distributions.Normal(pm,ps).sample(torch.tensor([num_samples]))
				pred_class_full=pyro.distributions.OrderedLogistic(self.embed_model.symptom_frequency_decoder(samples),self.embed_model.cut_points).logits
				pred_annots=torch.exp(pred_class_full[:,missing_dict[d_id],:]).mean(axis=0).detach().numpy()
				

			output_dictionary[dis]=list(zip([self.diseaseDataset.inverse_symptom_map[x] for x in missing_dict[d_id].detach().numpy()],pred_annots))

		return output_dictionary


	def LoadModel(self,stored_model):
		"""
		Loads previously fit model either from a dictionary (generated using PackageModel) or from a file path (with file constructed using PackageModel)

		Parameters
		----------
		stored_model : either dict or str (file path)

		Returns
		-------
		None.

		"""
		if not isinstance(stored_model,dict):
			assert isinstance(stored_model,str),"Expects file name if not provided with dictionary."
			stored_model = self._readModelFromFile(stored_model)
		assert set(stored_model.keys())==set(['model_state','meta_data','variational_post_params']),"Model dictionary must contain the following elements: 'model_state','meta_data'"


		self.embed_model = DiseaseVAE(
			stored_model['meta_data']['numSymptoms'],
			stored_model['meta_data']['numFreqCats'],
			stored_model['meta_data']['nLatentDim'],
			isLinear=stored_model['meta_data']['isLinear'],
			encoder_hyperparameters=stored_model['meta_data']['all_model_kwargs']['encoder_hyperparameters'],
			decoder_hyperparameters=stored_model['meta_data']['all_model_kwargs']['decoder_hyperparameters'],
			missing_freq_prior_mean=stored_model['meta_data']['all_model_kwargs']['missing_freq_priors'][0],
			missing_freq_prior_scale=stored_model['meta_data']['all_model_kwargs']['missing_freq_priors'][1],
			cut_points=stored_model['meta_data']['all_model_kwargs']['frequency_cut_points']
			)

		self.embed_model.load_state(stored_model)



	def PackageModel(self,fName=None):
		"""
		Packages the current model and returns it as a python dictionary. Will optionally write this dictionary to disk using PyTorch.

		Parameters
		----------
		fName : str, default None
		    File path to save model to disk. The default is None, which means that only a model dictionary will be returned.

		Returns
		-------
		model_dict : dict
		    Dictionary containing fitted model parameters in addition to general meta data.

		"""
		model_dict = self.embed_model.package_state()
		model_dict['meta_data']={}
		model_dict['meta_data']['numSymptoms']=self.numSymptoms
		model_dict['meta_data']['numFreqCats']=self.numFreqCats
		model_dict['meta_data']['nLatentDim']=self.nLatentDim
		model_dict['meta_data']['isLinear']=self.isLinear
		model_dict['meta_data']['all_model_kwargs']=self.all_model_kwargs
		if fName is not None:
		    with open(fName,'wb') as f:
		        torch.save(model_dict,f)
		return model_dict



