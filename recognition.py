import face_recognition
from cv2 import cv2
import numpy as np
from config import DISTANCE_BOUNDARY


def calculateEucledianDistance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)


def getFaceLocations(faceImg):
    return face_recognition.face_locations(faceImg, model="cnn")


def getFaceEncoding(faceImg, faceLocations):
    return face_recognition.face_encodings(faceImg, known_face_locations=faceLocations)[0]


def getFaceEncodings(faceImg):
    return face_recognition.face_encodings(faceImg)


def compareEncodings(faceEncoding, knownFaceEncodings):
    for knownFaceEncoding in knownFaceEncodings:
        distance = calculateEucledianDistance(faceEncoding, knownFaceEncoding)
        if distance < DISTANCE_BOUNDARY:
            return True
    return False


# Draws a rectangle to face
def drawRectangle(image, faceLocation):
    top, right, bottom, left = faceLocation
    cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
    return image
