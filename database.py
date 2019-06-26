import pyrebase
def database():
    config = {
        'apiKey': "AIzaSyB0wL9XVyyRrz6RGxA6SM4ycnZTrxLnFe0",
        'authDomain': "test-74097.firebaseapp.com",
        'databaseURL': "https://test-74097.firebaseio.com",
        'projectId': "test-74097",
        'storageBucket': "",
        'messagingSenderId': "271652598314",
        'appId': "1:271652598314:web:e7e3027f4bc9d8d1",
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db