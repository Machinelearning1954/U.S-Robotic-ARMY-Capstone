# GitHub - jonasrenault/adomvi: Automated Detection of Military Vehicles from Video Input

**URL:** https://github.com/jonasrenault/adomvi

---

Skip to content
Navigation Menu
Platform
Solutions
Resources
Open Source
Enterprise
Pricing
Sign in
Sign up
jonasrenault
/
adomvi
Public
Notifications
Fork 8
 Star 45
Code
Issues
2
Pull requests
2
Actions
Projects
Wiki
Security
Insights
jonasrenault/adomvi
 main
3 Branches
4 Tags
Code
Folders and files
Name	Last commit message	Last commit date

Latest commit
jonasrenault
Update dreambooth notebook
a010c97
 · 
History
69 Commits


.github/workflows
	
Add the search 2 dataset (#13)
	


adomvi
	
Add the search 2 dataset (#13)
	


notebooks
	
Update dreambooth notebook
	


resources
	
Adding dreambooth ss
	


tests
	
Add README and dependencies
	


.gitignore
	
Update version to 1.3.0
	


.pre-commit-config.yaml
	
Update version to 1.3.0
	


LICENSE
	
Initial commit
	


README.md
	
Update Readme
	


poetry.lock
	
Update version to 1.3.0
	


pyproject.toml
	
Update version to 1.3.0
	
Repository files navigation
README
MIT license
Automated Detection of Military Vehicles from Video Input (ADOMVI)
Introduction

This repository contains notebooks and resources used to train a state-of-the-art military vehicle tracker. Its main focus is on building a dataset of relevant images and annotations to fine-tune pre-trained object detection models, namely a Yolov8 model.

We start by building a training dataset from images available in open source object detection datasets (ImageNet, OpenImages, Roboflow). We also use scraping tools to collect more images of military vehicles from Google images. This allows us to define four broad classes of military vehicles that our model can then discriminate: Armoured Fighting Vehicle (AFV), Armoured Personnel Carrier (APC), Military Engineering Vehicle (MEV) and Light Armoured Vehicle (LAV). We provide a sample annotated dataset for these classes.

We also explore using diffusion models and the dreambooth method to generate new training images in different scenes and conditions.

Contents
The adomvi directory contains utility functions to fetch and format datasets for training a Yolov8 model for object detection.
The resources directory contains video samples for vehicle detection task.
The notebooks directory contains exemple notebooks on how to
Prepare a custom dataset of images annotated for automatic detection of military vehicles.
Train train a Yolov8 model using the prepared dataset.
Run tracking using the trained model on a sample video.
Fine tune Dreambooth to generate images of a tank.
Installation

To install the project, clone the repository and install the project in a python environment, either using pip

git clone git@github.com:jonasrenault/adomvi.git
cd adomvi
pip install --editable .

or using poetry

git clone git@github.com:jonasrenault/adomvi.git
cd adomvi
poetry install
Run the notebooks

To run the notebooks, start a jupyter lab server with

jupyter lab

and open one of the notebooks in the notebooks directory.

Tracking of military vehicles with multi-class object detection model

Some sample results of tracking different types of military vehicles (AFV, APC, MEV, LAV) using a finetuned yolov8-large model.

  
Generating diversity in our training dataset using Stable Diffusion and dreambooth
About

Automated Detection of Military Vehicles from Video Input

Topics
deep-learning detection pytorch image-recognition military vehicle-detection diffusion-models yolov8 military-ai
Resources
 Readme
License
 MIT license
 Activity
Stars
 45 stars
Watchers
 1 watching
Forks
 8 forks
Report repository


Releases 4
v1.3.0
Latest
+ 3 releases


Languages
Jupyter Notebook
99.3%
 
Python
0.7%
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
Manage cookies
Do not share my personal information
