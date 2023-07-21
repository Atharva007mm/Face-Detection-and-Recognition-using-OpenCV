import os
#provides the facility to establish the interaction between the user and the operating system.
import cv2  #OpenCV has a function to read video, which is cv2. VideoCapture().
import pickle  #the process whereby a Python object hierarchy is converted into a byte stream,
import cvzone #This is a Computer vision package that makes its easy to run Image processing and AI functions. At the core it uses OpenCV and Mediapipe libraries.
import face_recognition #Recognize and manipulate faces from Python or from the command line with. the world's simplest face recognition library.
import numpy as np #NumPy is a Python library used for working with arrays
import firebase_admin #Firebase Admin Python SDK enables server-side (backend) Python developers to integrate Firebase into their services and applications.
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

#DLIB-A toolkit for making real world machine learning and data analysis applications.
#What is Dlib? It's a landmark's facial detector with pre-trained models, the dlib is used to estimate the location of 68 coordinates (x, y) that map the
# facial points on a person's face like image below.

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://faceidrealtime-default-rtdb.firebaseio.com/",
    'storageBucket': "faceidrealtime.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background2.png')

#Importing the mode images into a list
folderModePath = 'Resources/Mode'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ....")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 + 480,55:55 + 640] = img
    imgBackground[44:44 + 633,808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print("matches", matches)
        #print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        #print("Match Index", matchIndex)

        if matches[matchIndex]:
            #print("Known Face Detected")
            #print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

            id = studentIds[matchIndex]

            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            if counter == 0:
                counter = 1
                modeType = 1

    if counter!= 0:

        if counter ==1:
            #get the data
            studentsInfo = db.reference(f'Students/{id}').get()
            print(studentsInfo)
            #get the image from the storage
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground, str(studentsInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)


        cv2.putText(imgBackground, str(studentsInfo['major']), (826, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(studentsInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(studentsInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(studentsInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)


        (w, h), _ =cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1,1)
        offset = (414-w)//2
        cv2.putText(imgBackground, str(studentsInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackground[175:175+216,909:909+216] = imgStudent
        



        counter+=(1)




    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)