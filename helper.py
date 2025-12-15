import torch
import requests
from datetime import datetime
import pytz
import json



def get_payload(url):
    res =   requests.get(url).json()
    return res["Payload"]


def check_cuda():
    # Check for CUDA
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device in use:', device)
    return device



def send_request( url,data):
    res =  requests.post(url, json = data)
    print(f"post service status code:{res.status_code}")
    return res

def class_to_json(obj):
    json_data =  json.dumps(obj.__dict__)
    python_dict = json.loads(json_data)
    return python_dict

def get_time():
    now = datetime.now()

    timezone = pytz.timezone('Europe/Istanbul')
    now = timezone.localize(now)

    formatted_time = now.strftime('%Y-%m-%dT%H:%M:%S%z')
    return formatted_time