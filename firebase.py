from firebase_admin import credentials, initialize_app, storage

storageBucket = 'im-here-mobile.appspot.com'
cred = credentials.Certificate("credentials/firebaseCredentials.json")
initialize_app(cred, {'storageBucket': storageBucket})
bucket = storage.bucket()


def uploadProfilePicture(filename, image):
    path = "profilePictures/" + filename
    blob = bucket.blob(path)
    blob.upload_from_string(image,content_type='image/png')
    blob.make_public()

    return blob.public_url
