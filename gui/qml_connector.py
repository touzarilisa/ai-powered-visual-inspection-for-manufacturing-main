"""
This program aims to implement Q methods to send signals to QML files and receive slots from it.
It will also use grpc client to send data to server
"""

# Importing libraries
import sys
import os, shutil
import time
import threading
import queue
import logging
import logging.config
import signal
import json
import grpc
import numpy as np
import cv2
import argparse
import zlib
import base64
from datetime import datetime
from gi.repository import GLib
import argparse

# Change directory to the directory of this file
cwd = os.getcwd()

sys.path.append(cwd + '/./database/')
from db import create_connection, insert_card, generate_report, save_report
from pdf import PDF

sys.path.append(cwd + '/./grpc/')
import rgb_image_pb2
import rgb_image_pb2_grpc


import PySide2 as Qt
from PySide2.QtCore import QObject, Signal, Slot, QTimer, QThread, QMutex, QMutexLocker
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine



# Define a class to connect to QML
class QmlConnector(QObject):
    """
    This class is used to connect to QML and send signals to it.
    """
    label = Signal(str, arguments=['Label'])
    progress_value = Signal(float)

    x = Signal(int, arguments=['X'])
    y = Signal(int, arguments=['Y'])
    width = Signal(int, arguments=['Width'])
    height = Signal(int, arguments=['Height'])
    
    text = Signal(str, arguments=['text'])


    def __init__(self,ip_address, port):
        super(QmlConnector, self).__init__()

        # Create a channel to the server
        channel = grpc.insecure_channel(ip_address + ":" + port)

        # Create a stub (client)
        self.stub = rgb_image_pb2_grpc.Predict_serviceStub(channel)

        # Create a root window
        self.root = None

        # Data to sent to the server
        self.image = None
        self.nm = None
        self.h = None
        self.w = None
        self.depth = None
        self.die = None

        # Data to receive from the server

        
  
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.height_image = 0
        self.width_image = 0
        self.depth_image = 0
        self.confidence = 0

        #Create database
        #self.db = Sqlite_db(cwd + '/../database/database.db')
        #self.db.create_cards_table()

        #Progess Value
        self.progress = 0  
           

    @Slot(str)
    def load_image(self, path):
        """
        :param data:
        :return:
        """
        # Clean up the path
        # If linux or mac
        if os.name == 'posix':
            path = path.replace('file://', '')
        # If windows
        elif os.name == 'nt':
            path = path.replace('file:///', '')
    
        # Read image from path

        # Delete CRLF from path
        path = path.replace('\r', '')
        path = path.replace('\n', '')
        
        image = cv2.imread(path)
        if image is None:
            print("Image not found")
            return
        #Get the image name
        image_name = path.split('/')[-1]

        # Display image
        print("Image name: ", image_name)
        print("Image shape: ", image.shape)
        print("Image type: ", image.dtype)

        # Get the image data
        self.h = image.shape[0]
        self.w = image.shape[1]
        self.depth = image.shape[2]

        self.image = image
        self.nm = image_name
        self.die = int(image_name[18])

    
    @Slot(result=list)
    def send_image(self):
        """
        Send an image to the server
        """
        try :
            # encode the image
            if self.image is not None:
                image_bytes = self.image.tobytes()
                image_bytes_compressed = zlib.compress(image_bytes)
                image_bytes_encoded = base64.b64encode(image_bytes_compressed)

                # create a request object
                request = rgb_image_pb2.RGB_image(image = image_bytes_encoded, name = self.nm, height =self.h , width = self.w, depth = self.depth)

                # make the call
                print("Sending image to server...") 
                response = self.stub.Predict(request)
                print("Response : ",response.x)
                print("Response : ",response.y)
                if response.label != "":
                   

                    self.height_image = response.height_image
                    self.width_image = response.width_image
                    self.depth_image = response.depth_image
                    self.confidence = response.confidence
                    insert_card(self.nm,self.die,response.label,self.confidence,str(response.x)+','+str(response.y)+','+str(response.width)+','+str(response.height)) 
                    
                    # Adapt confidence 
                    self.confidence = self.confidence * 100
                    self.confidence = round(self.confidence,2)
                    return [self.nm, response.label, self.confidence, response.x, response.y, response.width, response.height]
                    print("Received response from server:")

        except Exception as e:
            print("Error: ", e)
        
    @Slot() 
    def report_csv(self):
        save_report(case=0, DIE=1, decision = "Defected",date ="2022")
        
    @Slot()
    def report_download(self):        
        pdf = PDF()
        pdf.generate_report()  
        downloads_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        f = "report"+"_"+datetime.today().strftime('%Y-%m-%d')+".csv"
        shutil.copy(f, downloads_dir)
            
        
    @Slot()
    def report_pdf(self):        
        pdf = PDF()
        pdf.generate_report()  
        
    @Slot(str)  
    def report_csv_die(self, text):        
        save_report(case=1, DIE=int(text), decision = "Defected",date ="2022")
        
        
    @Slot(str) 
    def report_csv_type(self, text):
        if text == '0': decision = "Defected"
        elif text == '1': decision = "NOT Defected"
        
        save_report(case=2, DIE=1, decision = decision,date ="2022")
            
        
    @Slot(str) 
    def report_csv_date(self, text):
        save_report(case=3, DIE=1, decision = "Defected",date =text)
        
    
def main():
    """
    Main function
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description='Client for the RGB_image_server')
    parser.add_argument('--ip_address', default='localhost', help='IP address of the server')
    parser.add_argument('--port', default='50051', help='Port of the server')
    args = parser.parse_args()

    # Create a QApplication
    app = QGuiApplication(sys.argv)

    # Create a QQmlApplicationEngine
    engine = QQmlApplicationEngine()

    # Create a QmlConnector
    qml_connector = QmlConnector(ip_address= args.ip_address, port=args.port)

    # Connect to QML
    engine.rootContext().setContextProperty("QmlConnector", qml_connector)

    # Load QML file
    engine.load(os.path.join(os.path.dirname(__file__), "./main.qml"))


    # Execute the QApplication
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()
