from flask import Flask, request
from config import PATH, PORT, BACKEND_API_PATH
import numpy as np
import recognition
from http_helper import success, badRequest, notFound, customErrorResponse
from cv2 import cv2
import dlib
import firebase
import json
import requests
from flask import jsonify

app = Flask(__name__)
print("USE GPU: " + str(dlib.DLIB_USE_CUDA))


@app.route('/')
def index():
    return 'Welcome to I\'m Here Face Recognition Service!'


@app.route(PATH + '/checkFace', methods=['POST'])
def checkFace():
    imageFile = request.files["image"].read()
    image = recognition.decodeImage(imageFile)

    faceLocations = recognition.getFaceLocations(image)

    if len(faceLocations) > 1:
        return badRequest('There should be one face in the image!')
    if len(faceLocations) < 1:
        return notFound('No face found in the image!')

    # If face found, draw a rectangle around it
    recognition.drawRectangle(image, faceLocations[0])

    # Get encoding of the face
    faceEncoding = recognition.getFaceEncoding(image, faceLocations)
    faceEncoding = faceEncoding.tolist()
    faceEncoding = json.dumps(faceEncoding)

    encodedImage = recognition.encodeImage(image)
    # Upload to firebase and get url of it
    image_url = firebase.uploadProfilePicture(encodedImage)

    return success({
        "image_url": image_url,
        "face_encoding": faceEncoding
    })


@app.route(PATH + '/addAttendence', methods=['POST'])
def addAttendence():
    token = request.headers["Authorization"].split()[1]
    imageFile = request.files["image"].read()
    lectureCode = request.form["lectureCode"]
    week = request.form["week"]

    requestHeaders = {'Authorization': 'Bearer ' + token}
    image = recognition.decodeImage(imageFile)

    faceinfoResponse = requests.get(
        BACKEND_API_PATH + "/FaceInfo/" + lectureCode,
        headers=requestHeaders)

    # Check FaceInfo service is Ok
    if faceinfoResponse.status_code != 200:
        return customErrorResponse(faceinfoResponse.text, faceinfoResponse.status_code)

    knownFaceInfos = faceinfoResponse.json()
    faceLocations = recognition.getFaceLocations(image)
    joinedStudentsEncodings = recognition.getFaceEncodings(image, faceLocations)
    joinedUsers = []

    for faceInfoObj in knownFaceInfos:
        user_id = faceInfoObj['user_id']

        # Casting face encoding string to numpy ndarray
        faceEncoding = faceInfoObj['face_encoding']
        faceEncoding = json.loads(faceEncoding)

        # Face Encoding of known user (user_id)
        faceEncoding = np.asarray(faceEncoding)

        # Check the user is in the image
        isUserJoined = recognition.compareEncodings(faceEncoding, joinedStudentsEncodings)

        if isUserJoined:
            joinedUsers.append(user_id)

    recognition.drawRectangles(image, faceLocations)
    encodedImage = recognition.encodeImage(image)
    image_url = firebase.uploadAttendencePicture(encodedImage)

    addAttendenceBody = {
        'lectureCode': lectureCode,
        'week': int(week),
        'userIds': joinedUsers,
        'image_url': image_url
    }
    print(addAttendenceBody)
    addAttendenceResponse = requests.post(
        BACKEND_API_PATH + '/Attendence/AddAttendence',
        headers=requestHeaders,
        json=addAttendenceBody
    )
    if addAttendenceResponse.status_code != 204:
        return customErrorResponse(addAttendenceResponse.text, addAttendenceResponse.status_code)

    return success()


app.run(host="0.0.0.0", port=PORT, debug=False)
