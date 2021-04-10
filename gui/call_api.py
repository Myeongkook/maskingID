import uuid
import time
import json
import base64
import requests


def callAPI(file_path):
    api_url = ''
    secret_key = ''
    image_file = file_path
    try:
        with open(image_file, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        return False
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo',
                'data': base64.b64encode(file_data).decode()
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': secret_key,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", api_url, headers=headers, data=payload)

    return response
