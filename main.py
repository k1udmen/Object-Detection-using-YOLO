from warnings import filterwarnings
filterwarnings('ignore')
from predict import Detector, ValfCounter, ImgProcess
import configparser
import cv2
from camera import Camera
from helper import check_cuda, get_payload, get_time, class_to_json, send_request
import sys
from fastapi import FastAPI
import uvicorn
import asyncio
from schema.request_schema import RequestModel
import tracemalloc
tracemalloc.start()
import os
import threading
import time
import pathlib
app = FastAPI()

def conf(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


valf_control = {"isRunnedProcess":False,"selfNo":1, "is_completed_valf1":False, "pass":False,"is_all_completed":False,"is_completed_valf2": False}

@app.get("/test")
def test(): 
    if valf_control['isRunnedProcess'] == False:
        valf_control['isRunnedProcess'] = True
        payload = get_payload(url=get_payload_url)
        print(f"payload: {payload}")
        request_model = RequestModel(requestId=payload, appCode=valf_app_code)
        thread = threading.Thread(target=process, args=(request_model,))
        thread.start()
        return {"message": "Background task started."}
    return {"message": "Background task  has been already started."}

def save_ss(frame, self_no, request_id):
    cv2.imwrite(f"{ss_folder}/{request_id}/{self_no}.png", frame)
    
def create_folders(request_id):
    os.makedirs(f"{ss_folder}/{request_id}", exist_ok=True)
import numpy as np


@app.get("/test_normal")
def test_normal():
    if valf_control['isRunnedProcess'] == False:
        valf_control['isRunnedProcess'] = True
        payload = get_payload(url=get_payload_url)
        print(f"payload: {payload}")
        request_model = RequestModel(requestId=payload, appCode=valf_app_code)
        process(request_model)
       # thread = threading.Thread(target=process, args=(request_model,))
        #thread.start()
        return {"message": "Background task started."}
    return {"message": "Background task  has been already started."}

def process(request_model):
    k = 1

    while True:
        k+=1
        if valf_control['is_all_completed'] == True:
            print("true sonrası")
            request_model.requestId = get_payload(get_payload_url)
            print("new payload", request_model.appCode)
            valf_control['is_all_completed'] = False
            valf_control['is_completed_valf1'] = False
            valf_control['is_completed_valf2'] = False
            valf_control['pass'] = False
        
        frame = camera.capture()
        if frame is None:
        	#print("frame is None")
                camera.exit()
                camera.setCamera( camera_address, camera_height, camera_width)
                continue
        if k%2==0:
           cv2.imwrite(f"D:/Prod/Valf_Analitik/images/{k}.png", frame)
        start = time.time()
        request_model.status = False
        print(frame.shape)
        frame = ImgProcess.crop(frame)
        #frame = ImgProcess.rotate(frame)
        frame = ImgProcess.preprocess(frame, device)
        pred = detector.predict(frame)
        imgNp = ImgProcess.postprocess(frame)
        count_valf = ValfCounter.counter(pred, imgNp)
        print(f"Valf Count: {count_valf}")

        request_model.valfQuantity = count_valf
        request_model.transactionDate = get_time()
#        print(f"Valf Count: {count_valf}")

        request_model.selfNo = valf_control['selfNo']
        
        if count_valf <= 40 and valf_control["pass"]:
            
            if valf_control['selfNo'] == 2:
                valf_control['selfNo'] = 1
                valf_control['is_all_completed'] = True
                valf_control['is_completed_valf1'] = False
                valf_control["pass"] = False
                request_model.requestId = get_payload(get_payload_url)

            else:
                valf_control['selfNo'] = 2
                valf_control['is_completed_valf1'] = True
                valf_control["pass"]=False

        if count_valf >=42 and valf_control['pass']:
            continue
        
        request_model.selfNo = valf_control['selfNo']
        
        if valf_control['is_completed_valf1']:
            request_model.status=True
        # turn the valf2
        if valf_control['selfNo'] == 1  and valf_control['is_completed_valf1'] == False and count_valf >=50:
                request_model.status = True

                create_folders(request_id=request_model.requestId)
                request_model.status = True
                save_ss(imgNp, valf_control['selfNo'], request_model.requestId)    

                valf_control["pass"] = True
                json_data = class_to_json(request_model)
            # add post request to background task dont wait response
                end = time.time()
                passedTime = round((end-start), 3)

                res = send_request(send_data_url, json_data)
                print(f"Passed time: {passedTime}")
                print(f"afterRequestPassedTime: {round((time.time() - start), 3)}")
                
                continue
            
        
        #  turn the valf1
        if  valf_control['selfNo'] == 2 and valf_control['is_completed_valf2'] == False and count_valf >=50:
                create_folders(request_id=request_model.requestId)
                save_ss(imgNp, valf_control['selfNo'], request_model.requestId)    
                request_model.isPrinted=True
                valf_control["pass"] = True
                json_data = class_to_json(request_model)
            # add post request to background task dont wait response
                end = time.time()
                passedTime = round((end-start), 3)
                res = send_request(send_data_url, json_data)
                request_model.status = False
                request_model.isPrinted=False

                print(f"Passed time: {passedTime}")
                print(f"afterRequestPassedTime: {round((time.time() - start), 3)}")
                continue

       

        
        json_data = class_to_json(request_model)
        # add post request to background task dont wait response
        end = time.time()
        passedTime = round((end-start), 3)

        res = send_request(send_data_url, json_data)
        print(f"Passed time: {passedTime}")
        print(f"afterRequestPassedTime: {round((time.time() - start), 3)}")
    

  
if __name__ == "__main__":
    config_path = "D:/Prod/Valf_Analitik/config/config.ini"
    print(os.listdir("D:/Prod/Valf_Analitik/config"))
    config = conf(config_path)
    # server
    host = config['Server']['host']
    port = config['Server'].getint('port')
    
    # detector
    model_path = config['Model']['model_path']
    model_confidence = config['Model'].getfloat('model_confidence')
    model_iou = config['Model'].getfloat('model_iou')
    
    # valf
    valf_app_code = config['Data_Model']['valf_app_code']

    ## secreenshot folder
    ss_folder = config['Folders']['ss_folder']


    # camera
    camera_address = config['Camera']['camera_address']
    camera_height = config.getint('Camera', 'camera_height')
    camera_width = config.getint('Camera', 'camera_width')

    # send data server
    send_data_url = config['API_SERVER']['send_data_url']
    get_payload_url = config['API_SERVER']['get_payload_url']


    print(host, port, model_path, model_confidence, model_iou, camera_address, camera_width, camera_height, sep="\n")

    # camera instance
    camera = Camera(camera_address,camera_height, camera_width)

    # check cuda
    device = check_cuda()

    # create yolo detector instance
    detector = Detector(model_path, device)
    # all ops
    uvicorn.run(app, host=host, port=port)
