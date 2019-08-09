import pyrebase

config = {
    'apiKey': "AIzaSyDEaFcnSF0p2AR3JkdyVUgo0Ifno2EfG2M",
    'authDomain': "rupkotha.firebaseapp.com",
    'databaseURL': "https://rupkotha.firebaseio.com",
    'projectId': "rupkotha",
    'storageBucket': "rupkotha.appspot.com",
    'messagingSenderId': "403571374607",
    'appId': "1:403571374607:web:7dac8cb170ab8730"
}


def database():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db


def getStorage():
    firebase = pyrebase.initialize_app(config)

    store = firebase.storage()
    return store

