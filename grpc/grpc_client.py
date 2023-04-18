"""
This program is used to implement a gRPC client that sends rgb images to the server.
"""

import grpc 

# import the generated classes
import rgb_image_pb2
import rgb_image_pb2_grpc

# Import libraries for data encoding and decoding
import base64
import io
import zlib
import numpy as np
import cv2
import argparse

from tkinter import filedialog
from tkinter import *
from tkinter import Button, Tk
from tkinter import messagebox


import os
import sys



# Define the client class
class RgbImageClient(object):
    """
    This class is used to implement a gRPC client that sends rgb images to the server.
    """
    def __init__(self, ip_address, port):
        """
        Initialize the client class
        """
        # create a channel to the server
        channel = grpc.insecure_channel(ip_address + ":" + port)

        # create a stub (client)
        self.stub = rgb_image_pb2_grpc.Predict_serviceStub(channel)

        # Create a root window
        self.root = None

        # Data to sent to the server
        self.image = None
        self.nm = None
        self.h = None
        self.w = None
        self.depth = None

        # Data to receive from the server
        self.label = ""
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.height_image = 0
        self.width_image = 0
        self.depth_image = 0
        self.confidence = 0

    def send_image(self, image, nm, h, w):
        """
        Send an image to the server
        """
        try :
            # encode the image
            if image is not None:
                image_bytes = image.tobytes()
                image_bytes_compressed = zlib.compress(image_bytes)
                image_bytes_encoded = base64.b64encode(image_bytes_compressed)
    
                # create a request object
                request = rgb_image_pb2.RGB_image(image = image_bytes_encoded, name = nm, height =h , width = w, depth = 3)
                
                # make the call
                print("Sending image to server...") 
                response = self.stub.Predict(request)
                if response.label != "":
                    self.label = response.label
                    self.x = response.x
                    self.y = response.y
                    self.width = response.width
                    self.height = response.height
                    self.height_image = response.height_image
                    self.width_image = response.width_image
                    self.depth_image = response.depth_image
                    self.confidence = response.confidence
                    print("Received response from server:")
                    messagebox.showinfo("Image sent", "Image sent to server")
                    messagebox.showinfo("Received data", f"Confidence: {self.confidence}, Label: {self.label}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, height_image: {self.height_image}, width_image: {self.width_image}, depth_image: {self.depth_image}")


                else:
                    messagebox.showinfo("Image Classification", "No classification found")
            else:
                messagebox.showinfo("Image Sending", "No image selected, please select an image")
        except Exception as e:
            messagebox.showinfo("Error", "Error: " + str(e))
       
        
            
    
    def select_image(self):
        """
        Select an image from the client
        """
        # Open file dialog
        self.root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

        try:
            if self.root.filename != "":
                messagebox.showinfo("Image Selection", "Image selected: " + self.root.filename.split("/")[-1])
            else:
                messagebox.showinfo("Image Selection", "No image selected")
            # Read the image
            self.image = cv2.imread(self.root.filename)

            # Get the image name
            self.nm = self.root.filename.split("/")[-1]

            # Get the image height and width
            self.h = self.image.shape[0]
            self.w = self.image.shape[1]

        except Exception as e:
            messagebox.showinfo("Error", "Error: " + str(e))



def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type = str, default="localhost", help="The ip of the gRPC server")
                
    parser.add_argument("--port", type=str, default=50051,
                        help="The port of the gRPC server. Default to 50051")
    args = parser.parse_args()

    ip_address = str(args.ip)
    port = str(args.port)
    # Create a client
    client = RgbImageClient(ip_address, port)

    # Get current working directory
    cwd = os.getcwd()

    # Set size of the window
    window_width = 300
    window_height = 600



    # Create a root window
    client.root = Tk()
    client.root.title("Image Selection")
    client.root.geometry("{}x{}".format(window_width, window_height))

    # Create a Canvas widget
    canvas = Canvas(client.root, width = window_width, height = window_height)
    canvas.pack()

    # Image background
    image_background = PhotoImage(file = cwd + "/images/background.png")

    # Add the background image
    canvas.create_image(0, 0, image = image_background, anchor = NW)

    # Add the image selection button
    image_selection_button = Button(client.root, text = "Select image", command = client.select_image)
    image_selection_button.place(x = window_width/2 - 50, y = window_height/2 - 50)

    # Uploid the send logo
    #image_uploid_logo = PhotoImage(file = cwd + "/images/upload.png")
    #image_selection_button.config(image = image_uploid_logo, compound = RIGHT)


    # Add the image sending button
    image_sending_button = Button(client.root, text = "Send image", command = lambda: client.send_image(client.image, client.nm, client.h, client.w))
    image_sending_button.place(x = window_width/2 - 50, y = window_height/2 + 50)

    # Loop for the GUI
    client.root.mainloop()


if __name__ == "__main__":
    main()

    
    
