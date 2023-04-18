# AI Powered visual inspection for manufacturing
This repository contains all needed materials to our project of building a visual inspection system for manufacturing.

## Directory structure
This project is divided into several subdirectories :
* `database` : contains all the database files and the database management system
* `grpc` : contains all the gRPC files and the gRPC server and client which are used to make the application available to the outside world
* `models` : contains all the pre-trained models which will be used to make the visual inspection and prediction
* `notebooks` : contains all the files which are used to preprocess the data, implement the machine learning algorithms models and train the models
* `source` : contains the principal files of the project, predict.py that will be used to load the models and make the prediction, main.py that will the main file of the project
* `suggested frameworks` : contains all the frameworks that are suggested to be used in the project
* `train` : contains all the files which are used to train the models

## Installation
### Linux
To be able to use the project on a Linux machine, you need to do the following :
* Install the Python 3.8.x or higher version
* Install the needed packages with `pip install -r requirements.txt`
* Install qt5-default with `sudo apt-get install qt5-default`
* Install Tkinter with `sudo apt-get install python3-tk`
### Windows
For Windows, you need :
* Python 3.8.x or higher version
* The needed packages with `pip install -r requirements.txt`
## Usage
### Main file
Execute the main file of the project with `python3 main.py`

### Separate files
Since the project architecture is divided into server and client, you can execute the server with `python3 grpc/server.py` and the client with `python3 gui/qml_connector.py`

## gRPC
The gRPC server is used to make the application available to the outside world. It is used to make the prediction of the images and to send the results to the client. 

The received messages and the sent messages are defined in the `grpc/rgb_image.proto` file. They can be modified to fit the needs of the project.

after any modification, you need to regenerate grpc files with `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. rgb_image.proto`
















