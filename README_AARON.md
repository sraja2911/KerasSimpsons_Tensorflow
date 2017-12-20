#Requirements
##Python 3
### Windows
Python 3 is available from python.org:
https://www.python.org/downloads/

Version 3.6.4 tested with current software.

#### pip, setup_tools
Once installed run cmd:
>pip install --upgrade pip setup_tools

Then run:
>pip install virtualenv virtualenvwrapper

To make a new virtual env called Simpsons in cmd prompt run:
> mkvirtualenv Simpsons

To use virtual env in cmd prompt run:
> workon Simpsons

Then to pip install all python packages used with this repository in the same cmd window run:
> pip install -r requirements.txt

* Make sure you are in the cloned repository's base directory

## Nvidia CUDA toolkit
### Windows
tensorflow-gpu python package only works with CUDA toolkit v8.0

Download CUDA toolkit v8.0 here:
https://developer.nvidia.com/cuda-toolkit-archive

Run package install and make sure latest nvidia drivers are installed.

Download cuDNN v6 for CUDA toolkit v8.0 from:
https://developer.nvidia.com/rdp/cudnn-download

Requires being an nvidia developer community member.

Extract zip file and copy and paste all files in CUDA directory to CUDA toolkit directory:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0

* should be three directories bin, includes, lib that have files that belong in their corresponding directories in the CUDA toolkit directory

##Mongo DB
### Windows
#### Install mongoDb community server
Mongo DB community server is available from:
https://www.mongodb.com/download-center?jmp=nav#community

## Nodejs
### Windows
#### Nodejs
Download and install 8.9.3 LTS or version recommended for most users from nodejs.org:
https://nodejs.org/en/

In command prompt navigate to front-end-webpack directory:
> cd front-end-webpack

Run npm install
> npm install