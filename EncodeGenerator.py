import cv2
import face_recognition
import pickle
import os

# Folder containing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)
print("Images found:", PathList)

imgList = []
studentIds = []
for path in PathList:
    # Check if the file is a .png image
    if path.endswith(".png"):
        img = cv2.imread(os.path.join(folderPath, path))
        imgList.append(img)
        studentIds.append(os.path.splitext(path)[0])

print("Student IDs:", studentIds)

# Function to encode images
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB
        faces = face_recognition.face_encodings(img)  # Detect all faces in the image
        if faces:  # If face(s) are found
            encode = faces[0]  # Take the encoding of the first face
            encodeList.append(encode)
        else:
            print("No face found in image, skipping...")
    return encodeList

# Encode the images
print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encodings to a file
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved")
