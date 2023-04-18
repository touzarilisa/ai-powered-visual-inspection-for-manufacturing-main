"""
This program aims to upload the mobilenet model and use it to predict the class of an image.
"""

import os
import sys
import argparse
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras import backend as K
import scipy


class Predict:
    """
    This class is used to predict the class of an image.
    """

    def __init__(self, model_path):
        """
        Initialize the Predict class.

        :param model_path: The path to the model.
        :param image_path: The path to the image.
        """
        self.model_path = model_path
        self.prediction = None
        self.model = self.load_model()
        self.CAM = None

    def load_model(self):
        """
        Load the model.

        :return: The model.
        """
        model = tf.keras.models.load_model(self.model_path)
        return model

    def predict(self, model, image):
        """
        Predict the class of an image.

        :param model: The model.
        :param image: The image.
        :return: The class of the image.
        """
        self.prediction = model.predict(image)

    def get_image(self, image):
        """
        :param image_path:
        :return:
        """
        image = cv2.resize(image, (224, 224))
        image = np.array(image)
        image = image.astype('float32')
        image /= 255
        image = np.expand_dims(image, axis=0)
        return image

    def image_size(self, image):
        """
        Get the size of the image.

        :param image: The image.
        :return: The size of the image.
        """
        width, height, depth = image.size

        return width, height, depth

    def get_class(self):
        """
        :param index:
        :return:
        """
        classes = {
            0: "Defected",
            1: "Not Defected"
        }
        return classes[np.argmax(self.prediction)]

    def get_confidence(self):
        """
        :param index:
        :return:
        """
        return self.prediction[0][np.argmax(self.prediction)]

    def get_class_activation_map(self, image):
        """
        :param image:
        :return:
        """
        self.predict(self.model, image)
        class_weights = self.model.layers[-4].get_weights()[0]
        class_weights_winner = class_weights[:, np.argmax(self.prediction)]
        final_conv_layer = self.model.get_layer("out_relu")
        get_output = K.function([self.model.layers[0].input], [final_conv_layer.output, self.model.layers[-1].output])
        [conv_outputs, predictions] = get_output([image])
        conv_outputs = np.squeeze(conv_outputs)
        mat_for_mult = scipy.ndimage.zoom(conv_outputs, (32, 32, 1), order=1)

        final_output = np.dot(mat_for_mult.reshape((224*224, 1280)), class_weights_winner).reshape(224,224)

        self.CAM = final_output

    def get_bounding_box(self, img):
        """
        Get bounding box from class activation map
        """
        label_index = np.argmax(self.prediction)
        # If defected
        if label_index == 0:
            CAM2 = tf.keras.preprocessing.image.img_to_array(self.CAM, dtype=np.uint8)
            thresh = cv2.threshold(CAM2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # find contours and get the external one
            cnts = cv2.findContours(CAM2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            # sort contours on their size
            boundingBoxes = [cv2.boundingRect(c) for c in cnts]

            # Get the biggest bounding box
            (cx, cy, w, h) = max(boundingBoxes, key=lambda boundingBox: boundingBox[2] * boundingBox[3])

        else:
            (cx, cy, w, h) = (0, 0, 0, 0)

        return (cx, cy, w, h)





def main():
    # Get current working directory
    cwd = os.getcwd()
    # Instantiate the Predict class.
    predict = Predict(model_path=cwd+"/../models/mobilenet.hdf5")
    # Load the image.
    image = cv2.imread(cwd+"/../data/x_test/AE00008_080949_00_2_2_2001.jpg")
    if image is None:
        print("Image not found")
        sys.exit(1)
    # Get the image.
    image = predict.get_image(image)

    # Predict the class of the image.
    predict.predict(model=predict.model, image=image)
    # Get the class of the image.
    class_ = predict.get_class()
    # Get the confidence of the image.
    confidence = predict.get_confidence()

    # Print the class and confidence.
    print("Class: {}".format(class_))
    print("Confidence: {}".format(confidence))
    # Get the class activation map.
    predict.get_class_activation_map(image)

    # Get the bounding box.
    (cx, cy, w, h) = predict.get_bounding_box(image)

    # Print the bounding box.
    print("Bounding Box: {}".format((cx, cy, w, h)))


    # Draw the bounding box.
    cv2.rectangle(image, (cx, cy), (cx + w, cy + h), (0, 255, 0), 2)

    # Show the image.
    cv2.imshow("Image", image)

    # Wait for a key press.
    cv2.waitKey(0)


if __name__ == "__main__":
    main()