import base64

from flask import Flask, request
from constant import PATH
import numpy as np
from http_helper import success, badRequest,notFound
from recognition import getFaceLocations, drawRectangle, getFaceEncoding
from cv2 import cv2
import dlib
import firebase

app = Flask(__name__)
print("USE GPU: " + str(dlib.DLIB_USE_CUDA))


@app.route('/')
def index():
    return 'Welcome to I\'m Here Face Recognition Service!'


@app.route(PATH + '/checkFace', methods=['POST'])
def checkFace():
    imageFile = request.files["image"].read()
    email = request.form["email"]

    image = np.frombuffer(imageFile, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    faceLocations = getFaceLocations(image)

    if len(faceLocations) > 1:
        return badRequest('There should be one face in the image!')
    if len(faceLocations) < 1:
        return notFound('No face found in the image!')

    # If face found, draw a rectangle around it
    drawRectangle(image, faceLocations[0])

    # Encode image to upload
    isSuccess, encoded_image = cv2.imencode('.png', image)
    byteImage = encoded_image.tobytes()

    # Upload to firebase and get url of it
    image_url = firebase.uploadProfilePicture(email+".png", byteImage)
    return success({"image_url": image_url})


app.run(host="localhost", port=5000, debug=False)
