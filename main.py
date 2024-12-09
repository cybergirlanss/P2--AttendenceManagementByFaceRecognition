import os
import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import time  # To handle the delayc

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-5fb29-default-rtdb.firebaseio.com/"
})

# Initialize the camera
cap = cv2.VideoCapture(1)  # Use 0 for the default webcam; 1 for an external camera
cap.set(3, 640)  # Set frame width
cap.set(4, 480)  # Set frame height

# Load the background image
imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
imgModeListPaths = [
    'Resources/Modes/1.png',  # First image
    'Resources/Modes/2.png',  # Second image
    'Resources/Modes/3.png',  # Third image
    'Resources/Modes/4.png',  # Fourth image
]

# Load images into a list
imgModeList = []
for path in imgModeListPaths:
    img = cv2.imread(path)
    if img is not None:
        imgModeList.append(img)
    else:
        print(f"Failed to load image: {path}")

# Check if background and mode images are loaded
if imgBackground is None:
    print("Error: Background image not found!")
    exit()

if len(imgModeList) == 0:
    print("Error: No mode images loaded!")
    exit()

# Load the encoding file
print("Loading Encode File..")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded..")

modeType = 1
counter = 0
id = -1

# Variable to track if attendance has been marked today
attendance_updated_today = {}

# Start the main loop
while True:
    success, img = cap.read()  # Capture the current frame
    if not success:
        print("Failed to capture image")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Place the webcam feed on the background
    imgBackground[162:162 + 480, 55:55 + 640] = img

    # Place the first mode image onto the background
    if len(imgModeList) > 0:
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = int(y1 * 4), int(x2 * 4), int(y2 * 4), int(x1 * 4)
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                counter = 1

    if counter != 0:
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            # Load the student ID image
            image_path = studentInfo['image_url']
            full_image_path = os.path.join(
                '/Users/ansumgeorge/PycharmProjects/FaceRecognitionRealTimeDatabase/Images', image_path
            )
            id_image = cv2.imread(full_image_path)
            if id_image is not None:
                id_image_resized = cv2.resize(id_image, (216, 216))
                imgBackground[175:175 + 216, 909:909 + 216] = id_image_resized
            else:
                print(f"Failed to load image: {full_image_path}")

            # Check if attendance has been marked today
            if id not in attendance_updated_today:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendence'] += 1
                ref.child('total_attendence').set(studentInfo['total_attendence'])
                attendance_updated_today[id] = True
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print("Attendance marked!")

                # Display "MARKING" for 5 seconds
                text = "MARKING"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                thickness = 2
                color = (0, 255, 0)
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                text_x = 909 + (216 - text_size[0]) // 2
                text_y = 160
                cv2.putText(imgBackground, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                time.sleep(5)

                # Display "MARKED" after 5 seconds
                text = "MARKED"
                cv2.putText(imgBackground, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

            else:
                text = "ALREADY MARKED"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                thickness = 2
                color = (0, 0, 255)
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                text_x = 909 + (216 - text_size[0]) // 2
                text_y = 160
                cv2.putText(imgBackground, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

        # Display student details
        cv2.putText(imgBackground, str(studentInfo['total_attendence']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
