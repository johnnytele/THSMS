from queue import Empty, PriorityQueue
from types import NoneType
import cv2 
import numpy as np
import os
from collections import deque
from datetime import datetime

# This is for the database
import requests
import json
server_url = 'http://localhost:5000/add_data'


def send_data_to_server(fileName, region):

    data_to_send = {
    'FileName': fileName,
    'Region': region,
    'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    # Convert the data to JSON
    data_json = json.dumps(data_to_send)

    # Set the headers to specify that you are sending JSON data
    headers = {'Content-Type': 'application/json'}

    # Make the POST request
    response = requests.post(server_url, data=data_json, headers=headers)

    # Check the response
    if response.status_code == 200:
        print('Data added successfully')
    else:
        print('Error:', response.status_code, response.text)



capture = cv2.VideoCapture(0)
count = 0
frameCount = 0
fileNumber = 1;

# Make a GET request to the Flask program to get the largest id
response = requests.get('http://localhost:5000/get_largest_id')

# Check if the response was successful
if response.status_code == 200:
    # Get the largest id from the response
    largest_id = response.json()

    # Set fileNumber to the largest id + 1
    if largest_id is not None:
        fileNumber = largest_id + 1


countdown = 0
countdown2 = 0
DEFAULT_FILE_NAME = "/var/www/html/event"

# Define the codec and create VideoWriter object
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)

photoQueue1 = deque()
photoQueue6 = deque()
photoQueue12= deque()
photoQueue24= deque()


fourcc = cv2.VideoWriter_fourcc(*'XVID')




if not capture.isOpened():
    print("Error: Coupld not open camera")
    exit()

fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)
print("skiball")
fgbgg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

x1, y1, x2, y2 = 0, 5, 350, 200
l1, w1, l2, w2 = 0, 350, 220, 900
#l1, w1, l2, w2 = 40, 685, 445, 1430

output_dir = ""
output_dir2 = ""


while(1):
    ret, frame = capture.read()

    if not ret:
        print("could not open frame")
        break

    frameCount += 1

    roi1 = frame[y1:y2, x1:x2]

    roi2 = frame[l1:l2, w1:w2]



    fgmask = fgbg.apply(roi1)
    fgmaskRoi2 = fgbgg.apply(roi2)

    count = np.count_nonzero(fgmask)
    countRoi2 = np.count_nonzero(fgmaskRoi2)


    currTime = datetime.now()

    if (frameCount > 3 and count > 900):
        print("ROI1" + str(count))
        if countdown == 0:
            temp = "event" + str(fileNumber)
            output_dir = os.path.join(DEFAULT_FILE_NAME, temp)
            os.makedirs(output_dir, exist_ok=True)
            video_filename = os.path.join(output_dir, 'video.mp4')
            out = cv2.VideoWriter(video_filename, fourcc, 24.0, size)
            timer1 = (currTime, output_dir)
            timer2 = (currTime, output_dir)
            timer3 = (currTime, output_dir)
            timer4 = (currTime, output_dir)
            photoQueue1.append(timer1)
            photoQueue6.append(timer2)
            photoQueue12.append(timer3)
            photoQueue24.append(timer4)
            send_data_to_server(temp, 1)

            photoName = os.path.join(output_dir, 'before.png')
            cv2.imwrite(photoName, roi1)
            print("event" + str(fileNumber) + " -- ROI1 -- frameCount: " + str(frameCount) )

            fileNumber += 1

        countdown = 120

    if (frameCount > 3 and countRoi2 > 1200):
        print("ROI2" + str(countRoi2))
        if countdown2 == 0:
            temp = "event" + str(fileNumber)
            output_dir2 = os.path.join(DEFAULT_FILE_NAME, temp)
            os.makedirs(output_dir2, exist_ok=True)
            video_filename = os.path.join(output_dir2, 'video.mp4')
            out2 = cv2.VideoWriter(video_filename, fourcc, 24.0, size)
            timer1 = (currTime, output_dir2)
            timer2 = (currTime, output_dir2)
            timer3 = (currTime, output_dir2)
            timer4 = (currTime, output_dir2)
            photoQueue1.append(timer1)
            photoQueue6.append(timer2)
            photoQueue12.append(timer3)
            photoQueue24.append(timer4)
            send_data_to_server(temp, 2)

            photoName = os.path.join(output_dir2, 'before.png')
            cv2.imwrite(photoName, roi2)
            print("event" + str(fileNumber) + " -- ROI2 -- frameCount: " + str(frameCount) )
            fileNumber += 1

        countdown2 = 120
    

    

    if countdown > 0:
        out.write(frame)

    if countdown == 1:
        out.release()
        photoName = os.path.join(output_dir, 'after.png')
        cv2.imwrite(photoName, roi1)
        print("releasing ROI1")


    if countdown > 0:
        countdown -= 1

    if countdown2 > 0:
        out2.write(frame)

    if countdown2 == 1:
        out2.release()
        photoName = os.path.join(output_dir2, 'after.png')
        cv2.imwrite(photoName, roi2)
        print("releasing ROI2")


    if countdown2 > 0:
        countdown2 -= 1


    
    #3600
    if (len(photoQueue1) > 0 and (currTime - photoQueue1[0][0]).total_seconds() >= 3600):
        photoName = os.path.join(photoQueue1[0][1], 'hour1.png')
        cv2.imwrite(photoName, frame)
        photoQueue1.popleft()

    #21600
    if (len(photoQueue6) > 0 and (currTime - photoQueue6[0][0]).total_seconds() >= 21600):
        photoName = os.path.join(photoQueue6[0][1], 'hour6.png')
        cv2.imwrite(photoName, frame)
        photoQueue6.popleft()

    #43200
    if (len(photoQueue12) > 0 and (currTime - photoQueue12[0][0]).total_seconds() >= 43200):
        photoName = os.path.join(photoQueue12[0][1], 'hour12.png')
        cv2.imwrite(photoName, frame)
        photoQueue12.popleft()

    #86400
    if (len(photoQueue24) > 0 and (currTime - photoQueue24[0][0]).total_seconds() >= 86400):
        photoName = os.path.join(photoQueue24[0][1], 'hour24.png')
        cv2.imwrite(photoName, frame)
        photoQueue24.popleft()
    
    

    k = cv2.waitKey(1) & 0xff
    if k == ord('q') or k == 27:
        break

capture.release()
out.release()
cv2.destroyAllWindows()