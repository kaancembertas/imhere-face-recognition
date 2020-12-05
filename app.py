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
from flask import jsonify

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
    token = request.headers["Authorization"].split()[1]
    requestHeaders = {
        'Authorization': 'Bearer ' + token
    }

    imageFile = request.files["image"].read()
    image = np.frombuffer(imageFile, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    lectureCode = request.form["lectureCode"]
    week = request.form["week"]

    faceinfoResponse = requests.get(
        BACKEND_API_PATH + "/FaceInfo/" + lectureCode,
        headers=requestHeaders)

    # Check FaceInfo service is Ok
    if faceinfoResponse.status_code != 200:
        return customErrorResponse(faceinfoResponse.text, faceinfoResponse.status_code)

    knownFaceInfos = faceinfoResponse.json()
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
        isUserJoined = compareEncodings(faceEncoding, joinedStudentsEncodings)

        if isUserJoined:
            joinedUsers.append(user_id)

    addAttendenceBody = {
        'lectureCode': lectureCode,
        'week': int(week),
        'userIds': joinedUsers
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
