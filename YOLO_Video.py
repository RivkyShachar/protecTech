from ultralytics import YOLO
import cv2
import math
import time
import os
import threading
import pygame

# from super_gradients.common.object_names import Models
# from super_gradients.training import models
from Send_Message import send_Mes
#from insert_Db import process_and_insert_data

from playsound import playsound
import logging

logger = logging.getLogger()
threshold_x = 100
threshold_y = 100

# Define the path to the alarm sound file
#alarm_sound_file=r'C:\ProtecTeck_PEE_Detection\ProtecTeck_PEE_Detection\sound.wav'
# Event to control the alarm sound

# Define the path to the alarm sound file
alarm_sound_file = r'C:\ProtecTeck_PEE_Detection\ProtecTeck_PEE_Detection\sound1.wav'

# Event to control the alarm sound
alarm_event = threading.Event()


# Function to play the alarm sound
def play_alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_sound_file)
    pygame.mixer.music.play()


# Function to turn on the alarm sound
def AlarmOn():
    if not alarm_event.is_set():
        alarm_event.set()
        # Start the alarm sound in a separate thread
        threading.Thread(target=play_alarm_sound).start()


# Function to turn off the alarm sound
def AlarmOff():
    if alarm_event.is_set():
        alarm_event.clear()
        # Stop the alarm sound
        pygame.mixer.music.stop()


def check_condition(class_name):
    # vest = "NO-Safety Vest"
    mask = "NO-Mask"
    hat = "NO-Hardhat"
    if any(s in class_name for s in [ mask, hat]):
        logger.info("hi")
        # Process the condition here or call the desired function
        #send_Mes()


def video_detection(path_x):
    video_capture = path_x
    # Create a Webcam Object
    cap=cv2.VideoCapture(video_capture)
    frame_width=int(cap.get(3))
    frame_height=int(cap.get(4))
    # out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

    # model=models.get(Models.YOLOX_N,pretrained_weights="coco")
    # model=models.get('yolo_nas_l', num_classes=2, checkpoint_path="YOLO_Weights.best")
    model = YOLO("YOLO-Weights/best.pt")
    classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest',
                  'machinery', 'vehicle']
    sendMes = True
    start_time = time.time()
    start_time_db = time.time()
    interval_minutes = 0.1
    interval_seconds = interval_minutes * 60
    interval_minutes_db = 5
    interval_seconds_db = interval_minutes_db * 60
    no_hats=0
    no_hats_db=0
    no_vests=0
    counter_db=0
    counter=0
    alarm = False
    while True:
        success, img = cap.read()
        if not success:
            continue
        if path_x == 1:
            cv2.line(img, (threshold_x, 0), (threshold_x, img.shape[0]), (0, 255, 0), 2)
            cv2.line(img, (0, threshold_y), (img.shape[1], threshold_y),(0,255, 0),2)
        results=model(img,stream=True)
        class_Name_List = []
        counter += 1
        for r in results:
            boxes = r.boxes
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}'#{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                if class_name == 'Person':
                    if path_x == 1:
                        if y1 < threshold_y or x1 < threshold_x:
                            cv2.line(img, (threshold_x, 0), (threshold_x, img.shape[0]), (0, 0, 255), 2)
                            cv2.line(img, (0, threshold_y), (img.shape[1], threshold_y), (0, 0, 255), 2)
                            color = (0,0,255)
                            AlarmOn()
                        else:
                            AlarmOff()
                    else:
                        AlarmOff()

                else:
                    AlarmOff()

                if class_name == 'NO-Hardhat':
                    color=(0, 204, 255)
                    class_Name_List.append(class_name)
                    no_hats += 1
                    no_hats_db+=1
                    #process_and_insert_data(SiteName, DangerType, DateAndHour):
                # elif class_name == "NO-Mask":
                #     color = (222, 82, 175)
                #     class_Name_List.append(class_name)
                    #process_and_insert_data(SiteName, DangerType, DateAndHour):
                elif class_name == "NO-Safety Vest":
                    color = (0, 149, 255)
                    class_Name_List.append(class_name)
                    no_vests +=1
                    #process_and_insert_data(SiteName, DangerType, DateAndHour):
                else:
                    continue
                    #color = (85,45,255)
                if conf>0.5 and class_name is not 'Person':
                    cv2.rectangle(img, (x1,y1), (x2,y2), color,3)
                    cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
                #Check if 5 minutes have passed
                logger.info("what")
            #sends to teh database every 5 min
            # if time.time() - start_time >= interval_seconds:
            #     average_no_hats = round(no_hats_db / counter)
            #     print(average_no_hats)
            #     if average_no_hats > 1:
            #         AlarmOn()
            #     else:
            #         AlarmOff()
            #     no_hats_db = 0
            #     counter_db = 0
            #     start_time_db = time.time()

            # alarm will go off if someone doesn't wear helmet longer than 10 seconds
            if time.time() - start_time_db >= interval_seconds_db:

                # Reset the start time
                average_no_hats = round(no_hats / counter)
                average_no_vests = round(no_vests / counter)
                # sends to the database from what camera and the average no hats and no vests.

                no_hats_db = 0
                no_vests_db = 0
                counter_db = 0
                start_time = time.time()

            if "NO-Hardhat" in class_Name_List and no_hats>3 and time.time() - start_time >= interval_seconds:
                AlarmOn()
                if sendMes:
                    # Call the check_condition function
                    check_condition(class_Name_List)
                    sendMes=False
                #play_alarm_sound()
                class_Name_List=[]
                no_hats=0
            else:
                time.sleep(0.1)
                AlarmOff()
        yield img
cv2.destroyAllWindows()






