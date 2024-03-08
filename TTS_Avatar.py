#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import json
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import requests

# logging.basicConfig(stream=sys.stdout, level=logging.INFO,  # set to logging.DEBUG for verbose output
#         format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
 
logs_path = os.path.join( "logs", LOG_FILE)
 
os.makedirs(logs_path,exist_ok=True)
 
log_file_path = os.path.join(logs_path,LOG_FILE)
logging.basicConfig(

      filename=log_file_path,

format="[%(asctime)s]: %(levelname)s -['User_Name':Mahir]: -['filename']:%(filename)s -['function_name']:%(funcName)s -['line_no']:%(lineno)d - %(message)s ",

level=logging.INFO

)
# logger = logging.getLogger(__name__)

# Your Speech resource key and region
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY", '--------') #add subscription key
SERVICE_REGION = os.getenv("SERVICE_REGION", "westus2") # Add Region

NAME = "Simple avatar synthesis"
DESCRIPTION = "Simple avatar synthesis description"

# The service host suffix.
SERVICE_HOST = "customvoice.api.speech.microsoft.com"


def submit_synthesis():
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        'displayName': NAME,
        'description': DESCRIPTION,
        "textType": "PlainText",
        'synthesisConfig': {
            "voice": "en-US-JennyNeural",
        },
        # Replace with your custom voice name and deployment ID if you want to use custom voice.
        # Multiple voices are supported, the mixture of custom voices and platform voices is allowed.
        # Invalid voice name or deployment ID will be rejected.
        'customVoices': {
            # "YOUR_CUSTOM_VOICE_NAME": "YOUR_CUSTOM_VOICE_ID"
        },
        "inputs": [
            {
                 "text": "Hello Danush, Happy womens day",
                # "text": input()
            },
        ],
        "properties": {
            "customized": False, # set to True if you want to use customized avatar
            "talkingAvatarCharacter": "lisa",  # talking avatar character
            "talkingAvatarStyle": "graceful-sitting",  # talking avatar style, required for prebuilt avatar, optional for custom avatar
            "videoFormat": "webm",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "vp9",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "transparent",
            "kbitrate": "400",
        }
    }

    response = requests.post(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logging.info('Batch avatar synthesis job submitted successfully')
        logging.info(f'Job ID: {response.json()["id"]}')
        return response.json()["id"]
    else:
        logging.error(f'Failed to submit batch avatar synthesis job: {response.text}')


def get_synthesis(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logging.debug('Get batch synthesis job successfully')
        logging.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            logging.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
        return response.json()['status']
    else:
        logging.error(f'Failed to get batch synthesis job: {response.text}')
  
  
def list_synthesis_jobs(skip: int = 0, top: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar?skip={skip}&top={top}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logging.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logging.info(response.json())
    else:
        logging.error(f'Failed to list batch synthesis jobs: {response.text}')
  
  
if __name__ == '__main__':
    job_id = submit_synthesis()
    if job_id is not None:
        while True:
            status = get_synthesis(job_id)
            if status == 'Succeeded':
                logging.info('batch avatar synthesis job succeeded')
                break
            elif status == 'Failed':
                logging.error('batch avatar synthesis job failed')
                break
            else:
                logging.info(f'batch avatar synthesis job is still running, status [{status}]')
                time.sleep(5)
