# Face Recognition Based Attendance Management System

This project is an **Attendance Management System** using **Face Recognition** for real-time student attendance tracking.

## Features:
- Real-time attendance tracking using face recognition.
- Displays student details like name, major, and year.
- Stores attendance data in Firebase Realtime Database.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cybergirlanss/P2--AttendenceManagementByFaceRecognition.git
2. Navigate to the project folder:
    ```bash
   cd FaceRecognitionRealTimeDatabase

3. Install the required dependencies:
    ```bash
     pip install -r requirements.txt

4. Set up the Firebase credentials (serviceAccountKey.json) in the root directory.
     
## Usage

1. Run the main.py file to start the attendance system:
    ```bash
     python main.py
2. The system will detect faces and mark attendance based on the recognized student.
3. Ensure the camera is connected and working

## Requirements

* Python 3.x
* OpenCV
* face_recognition
* Firebase Admin SDK

## License

This project does not have a formal license. Use it at your own discretion.

### Explanation of Changes:
- **Bash commands**: All commands like `git clone`, `pip install`, and `python main.py` are now inside code blocks (using triple backticks).
- **License**: Since you didn’t select a license on GitHub, the **License** section now says: "This project does not have a formal license."

### Next Steps:
- Copy and paste this updated version into your `README.md` file in PyCharm.
- Follow the same steps to commit and push the changes to GitHub.

## Dependencies

The following Python libraries are required for the project:

* numpy – Numerical operations, required for image processing.
* opencv-python – OpenCV library for computer vision tasks, used for capturing video and processing images.
* face-recognition – Face recognition library, used for detecting and recognizing faces.
* firebase-admin – Firebase SDK for interacting with Firebase Realtime Database.
## Directory Structure

## Directory Structure
The project has the following directory structure:

```plaintext
FaceRecognitionRealTimeDatabase/
├── Images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Resources/
│   ├── background.png
│   ├── mode1.png
│   ├── mode2.png
│   └── ...
├── myenv/               # Virtual environment
├── serviceAccountKey.json
├── EncodeFile.p
├── EncodeGenerator.py
├── AddDataToDatabase.py
├── main.py
├── test.py
└── README.md


## Acknowledgments

* OpenCV: Used for real-time face recognition and camera operations.
* face_recognition: Used for face detection and recognition.
* Firebase: Used to store and manage attendance data.
* Python Community: For providing open-source libraries that helped in developing this system.

