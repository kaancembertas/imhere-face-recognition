from flask import Flask, request
from constant import PATH
import numpy as np
from helper import success, badRequest
from recognition import getFaceLocations,drawRectangle
from cv2 import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to I\'m Here Face Recognition Service!'


@app.route(PATH + '/checkFace', methods=['POST'])
def checkFace():
    print("checkFace")
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

    return success()


app.run(host="localhost", port=5000, debug=True)
