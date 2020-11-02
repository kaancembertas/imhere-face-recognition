import pyrebase


def getFirebaseConfig():
    #INPUT
    print("Enter firebase project id: ")
    projectId = "im-here-mobile"
    print("Enter firebase api key: ")
    apiKey = "AIzaSyCqA9BZHpZIDjsjVHwi4XZLSkavN6TZZaA"
    return {
        "apiKey": apiKey,
        "authDomain": projectId + ".firebaseapp.com",
        "storageBucket": projectId + ".appspot.com",
        "serviceAccount": "credentials/firebaseCredentials.json",
        "databaseURL": "https://databaseName.firebaseio.com",
    }


firebase = pyrebase.initialize_app(getFirebaseConfig())


def uploadProfilePicture(filename, image):
    storage = firebase.storage()
    path = "profilePictures/" + filename
    storage.child(path).put(image)
    #url = storage.child(path).get_url()
    #return url
