#!python


import setuptools
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('EmbedOMIM/embed.py').read(),
    re.M).group(1)



with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="EmbedOMIM",
    version=version,
    author="David Blair",
    author_email="david.blair@ucsf.edu",
    description="A generative probability model for embedding Mendelian diseases based on their annotated symptoms (HPO) and their associated frequencies (discrete).",
    long_description_content_type="text/markdown",
    url="https://github.com/daverblair/EmbedOMIM",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'torch',
        'pyro-ppl'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
