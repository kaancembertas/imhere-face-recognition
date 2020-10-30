import face_recognition
from cv2 import cv2


def getFaceLocations(faceImg):
    return face_recognition.face_locations(faceImg, model="cnn")


def getFaceEncoding(faceImg, faceLocations):
    return face_recognition.face_encodings(faceImg, known_face_locations=faceLocations)[0]


def compareEncodings(faceImg1, faceImg2):
    return face_recognition.compare_faces([faceImg1], faceImg2)[0]


# Draws a rectangle to face
def drawRectangle(image, faceLoction):
    top, right, bottom, left = faceLoction
    cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
    return image
