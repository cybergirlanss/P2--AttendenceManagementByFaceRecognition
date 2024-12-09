import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-5fb29-default-rtdb.firebaseio.com/"
})

# Reference to the Firebase database
ref = db.reference('Students')

# Data to be added
data = {
    "852741": {
        "name": "Emily Blunt",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendence": 2,
        "standing": "Average",
        "year": 2,
        "image_url": "/Users/ansumgeorge/PycharmProjects/FaceRecognitionRealTimeDatabase/Images/852741.png",
        "last_attendence_time": "2024-12-11 00:54:34"
    },
    "963852": {
        "name": "Elon Musk",
        "major": "Robotics",
        "starting_year": 2020,
        "total_attendence": 5,
        "standing": "Good",
        "year": 2,
        "image_url": "/Users/ansumgeorge/PycharmProjects/FaceRecognitionRealTimeDatabase/Images/963852.png",
        "last_attendence_time": "2024-12-11 00:54:34"
    },
    "22bsa10229": {
        "name": "Ansu M George",
        "major": "Cloud Computing",
        "starting_year": 2022,
        "total_attendence": 4,
        "standing": "Good",
        "year": 4,
        "image_url": "/Users/ansumgeorge/PycharmProjects/FaceRecognitionRealTimeDatabase/Images/22bsa10229.png",
        "last_attendence_time": "2024-12-11 00:54:34"
    }
}

# Add data to Firebase
for key, value in data.items():
    ref.child(key).set(value)
