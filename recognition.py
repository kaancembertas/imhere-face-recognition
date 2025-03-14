# Author: Kaan Çembertaş
# No: 200001684
import face_recognition
from cv2 import cv2
import numpy as np
from config import DISTANCE_TOLERANCE


def calculateEucledianDistance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)


def getFaceLocations(faceImg):
    return face_recognition.face_locations(faceImg, model="cnn")


def getFaceEncoding(faceImg, faceLocations):
    return face_recognition.face_encodings(faceImg, known_face_locations=faceLocations)[0]


def getFaceEncodings(faceImg, faceLocations):
    return face_recognition.face_encodings(faceImg, known_face_locations=faceLocations)


def compareEncodings(faceEncoding, knownFaceEncodings):
    for knownFaceEncoding in knownFaceEncodings:
        distance = calculateEucledianDistance(faceEncoding, knownFaceEncoding)
        if distance < DISTANCE_TOLERANCE:
            return True
    return False


# Draws a rectangle to face
def drawRectangle(image, faceLocation):
    top, right, bottom, left = faceLocation
    cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)


# Draws a rectangles to face
def drawRectangles(image, faceLocations):
    for faceLocation in faceLocations:
        drawRectangle(image, faceLocation)


def encodeImage(image):
    # Encode image to upload
    isSuccess, encoded_image = cv2.imencode('.png', image)
    byteImage = encoded_image.tobytes()
    return byteImage


def decodeImage(imageFile):
    image = np.frombuffer(imageFile, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image
