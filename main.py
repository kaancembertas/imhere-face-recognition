import face_recognition
from cv2 import cv2


def getFaceLocations(faceImg):
    return face_recognition.face_locations(faceImg, model="cnn")


def getFaceEncoding(faceImg, faceLocations):
    return face_recognition.face_encodings(faceImg, known_face_locations=faceLocations)[0]


def compareEncodings(faceImg1, faceImg2):
    return face_recognition.compare_faces([faceImg1], faceImg2)[0]


obama1 = face_recognition.load_image_file("images/obama1.png")
obama2 = face_recognition.load_image_file("images/obama2.png")
obama1_original = cv2.imread("images/obama1.png")
obama2_original = cv2.imread("images/obama2.png")

obama1Locations = getFaceLocations(obama1)
obama2Locations = getFaceLocations(obama2)

obama1Encoding = getFaceEncoding(obama1, obama1Locations)
obama2Encoding = getFaceEncoding(obama2, obama2Locations)

comparing = compareEncodings(obama1Encoding, obama2Encoding)
print(comparing)

top, right, bottom, left = obama1Locations[0]
cv2.rectangle(obama1_original,(left,top),(right,bottom),(255,0,0),2)

top, right, bottom, left = obama2Locations[0]
cv2.rectangle(obama2_original,(left,top),(right,bottom),(255,0,0),2)

cv2.imshow("KAAN", obama1_original)
cv2.waitKey(0)
cv2.imshow("KAAN2", obama2_original)
cv2.waitKey(0)
cv2.destroyAllWindows()

