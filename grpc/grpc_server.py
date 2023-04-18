"""
This program is a gRPC server that receives rgb images from the client.
"""

# import the grpc package
import os
import sys
import grpc
from concurrent import futures

# import the generated classes
import rgb_image_pb2_grpc 
import rgb_image_pb2
import time

import zlib 
import base64
import numpy as np

# Change the path to the directory where the script predicts.py is located
cwd = os.getcwd()
sys.path.append(cwd + '/./source/')
from predict import Predict


class RgbImageServicer(rgb_image_pb2_grpc.Predict_serviceServicer):
    """
    This class is used to implement a gRPC server that receives rgb images from the client.
    """

    def __init__(self):
        """
        Initialize the server class
        """
        self.server = None
        # Instance of the model
        self.classifier = Predict(cwd + '/./models/mobilenet.hdf5')
        if self.classifier.model is None:
            print("Error loading model")
        else:
            print("Model loaded")
            print("Model: ", self.classifier.model)

    
    def start(self, ip_address, port):
        """
        Start the server
        """
        # create a server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # add the service to the server
        rgb_image_pb2_grpc.add_Predict_serviceServicer_to_server(self, self.server)

        # start the server
        self.server.add_insecure_port(ip_address + ":" + port)

        # start the server
        self.server.start()
        print("Server started...")

    def stop(self):
        """
        Stop the server
        """
        self.server.stop(0)
        print("Server stopped...")
    
    def loop(self):
        """
        Loop the server
        """
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.stop()
    
    def Predict(self, request, context):
        """
        Method where will be doing our processing and storing the result in Database

        TODO: Add your processing here
        TODO: Add your storing here

        """
        print("Received image:")
        print("Name: " + request.name)
        print("Height: " + str(request.height))
        print("Width: " + str(request.width))

        # decode the image and display it
        image = np.frombuffer(zlib.decompress(base64.b64decode(request.image)), dtype=np.uint8).reshape(request.height, request.width, 3)

        # predict the image
        image = self.classifier.get_image(image)
        # Predict the image
        self.classifier.predict(model=self.classifier.model, image=image)

        # Get class acctivation map
        self.classifier.get_class_activation_map(image)

        # Get bounding box
        (x, y, w, h) = self.classifier.get_bounding_box(image)

        # create a valid response
        response = rgb_image_pb2.Predicted()
        response.label = self.classifier.get_class()
        response.confidence = self.classifier.get_confidence()
        response.x = x
        response.y = y
        response.height_image = 224
        response.width_image = 224
        response.depth_image = 3
        response.width = w
        response.height = h

        # Send the response

        return response

def main():
    # create a server
    server = RgbImageServicer()

    # start the server
    server.start("localhost", "50051")

    # loop the server
    server.loop()

if __name__ == "__main__":
    main()
    
