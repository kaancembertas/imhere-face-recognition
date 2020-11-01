import pyrebase


def getFirebaseConfig():
    print("Enter firebase project id: ")
    projectId = input()
    print("Enter firebase api key: ")
    apiKey = input()
    config = {
        "apiKey": apiKey,
        "authDomain": projectId + ".firebaseapp.com",
        "storageBucket": projectId + ".appspot.com",
        "serviceAccount": ""
    }

