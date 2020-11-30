from flask import Flask, request
from config import PATH, PORT, BACKEND_API_PATH
import numpy as np
from recognition import getFaceLocations, drawRectangle, getFaceEncoding, getFaceEncodings, compareEncodings
from http_helper import success, badRequest, notFound, customErrorResponse
from cv2 import cv2
import dlib
import firebase
import json
import requests

app = Flask(__name__)
print("USE GPU: " + str(dlib.DLIB_USE_CUDA))


@app.route('/')
def index():
    return 'Welcome to I\'m Here Face Recognition Service!'


@app.route(PATH + '/checkFace', methods=['POST'])
def checkFace():
    imageFile = request.files["image"].read()
    image = np.frombuffer(imageFile, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    faceLocations = getFaceLocations(image)

    if len(faceLocations) > 1:
        return badRequest('There should be one face in the image!')
    if len(faceLocations) < 1:
        return notFound('No face found in the image!')

    # If face found, draw a rectangle around it
    drawRectangle(image, faceLocations[0])

    # Get encoding of the face
    faceEncoding = getFaceEncoding(image, faceLocations)
    faceEncoding = faceEncoding.tolist()
    faceEncoding = json.dumps(faceEncoding)

    # Encode image to upload
    isSuccess, encoded_image = cv2.imencode('.png', image)
    byteImage = encoded_image.tobytes()

    # Upload to firebase and get url of it
    image_url = firebase.uploadProfilePicture(byteImage)

    return success({
        "image_url": image_url,
        "face_encoding": faceEncoding
    })


@app.route(PATH + '/addAttendence', methods=['POST'])
def addAttendence():
    lectureCode = request.form["lectureCode"]
    imageFile = request.files["image"].read()
    image = np.frombuffer(imageFile, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    faceinfo_response = requests.get(BACKEND_API_PATH + "/FaceInfo/" + lectureCode)

    # Check FaceInfo service is Ok
    if faceinfo_response.status_code != 200:
        return customErrorResponse(faceinfo_response.text, faceinfo_response.status_code)

    knownFaceInfos = faceinfo_response.json()
    joinedStudentsEncodings = getFaceEncodings(image)
    joinedUsers = []

    for faceInfoObj in knownFaceInfos:
        user_id = faceInfoObj['user_id']

        # Casting face encoding string to numpy ndarray
        faceEncoding = faceInfoObj['face_encoding']
        faceEncoding = json.loads(faceEncoding)

        # Face Encoding of known user (user_id)
        faceEncoding = np.asarray(faceEncoding)

        # Check the user is in the image
        isUserJoined = compareEncodings(faceEncoding,joinedStudentsEncodings)

        if isUserJoined:
            joinedUsers.append(user_id)

    print(joinedUsers)
    return "OLDI"


app.run(host="0.0.0.0", port=PORT, debug=False)
