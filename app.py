from flask import Flask, request
from constant import PATH
import numpy as np
from helper import success, badRequest
from recognition import getFaceLocations,drawRectangle,getFaceEncoding
from cv2 import cv2
import dlib

app = Flask(__name__)
print("USE GPU: "+str(dlib.DLIB_USE_CUDA))

@app.route('/')
def index():
    return 'Welcome to I\'m Here Face Recognition Service!'


@app.route(PATH + '/checkFace', methods=['POST'])
def checkFace():
    imageFile = request.files["image"].read()
    img = np.frombuffer(imageFile, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    faceLocations = getFaceLocations(img)

    if len(faceLocations) > 1:
        return badRequest('There should be one face in the image!')
    if len(faceLocations)<1:
        return badRequest('No face found in the image!')

    drawRectangle(img,faceLocations[0])
    cv2.imwrite("images/newImage.png",img)
    faceEncoding = getFaceEncoding(img,faceLocations)

    return success("OLDUOLDU")


app.run(host="localhost", port=5000, debug=True)
