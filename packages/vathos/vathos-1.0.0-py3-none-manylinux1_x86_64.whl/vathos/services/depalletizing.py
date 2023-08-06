# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################

import json
import logging
from time import perf_counter

import requests

from vathos import BASE_URL
from vathos.products import get_product
from vathos.configurations import get_configuration
from vathos.files import upload_files


def train_product(product_id, calibration_image_path, token, device_id=None):
  """Starts a training.
  
  Args: 
    product_id (str): id of the product to start the training for. A product
      is created with the function `create_product()` from the module
      `vathos.products`.
    calibration_image_path (str): path of an image for extrinsic calibration.
    The image must be a depth image of the plane the detected objects will rest
    upon during inference. It is converted to millimeters, then cast to a short
    integer array whose LSB and MSB are put into the red respectively green
    channel of an 8-bit RGB image before storing it as a PNG-compressed file.
    token (str): API access token

  Returns:
    str: id of the training task
    
  """
  # upload calib image id
  calib_image = upload_files([calibration_image_path], token)[0]

  train_data = {
      'workflow':
          'votenet',
      'product':
          product_id,
      'device':
          device_id,
      'tasks': [{
          'service': 'extrinsic.calibration.vathos.net',
          'parameters': {
              'planeImage': calib_image['_id']
          }
      }, {
          'service': 'rendering.votenet.detection.vathos.net'
      }, {
          'service': 'train.votenet.detection.vathos.net'
      }, {
          'service': 'conversion.trt.vathos.net'
      }]
  }

  post_task_response = requests.post(
      f'{BASE_URL}/compositetasks',
      json=train_data,
      headers={'Authorization': f'Bearer {token}'},
      timeout=5)

  return post_task_response.json()['_id']


def run_inference(product_id, test_image_path, token):
  """Runs an inference request.
  
  Args: 
    product_id (str): id of the product to start the training for. A product
      is created with the function `create_product()` from the module
      `vathos.products`.
    test_image_path (str): path of image to run inference on. This image
    must measure the depth of each pixe in millimeters, where each pixel is
    stored as a short integer, whose LSB and MSB are packed into the red
    respectively green channel of an 8-bit RGB image before storing it as a
    PNG-compressed file.
    token (str): API access token

  Returns:
    list: detected objects  
  """
  product = get_product(product_id, token)
  configuration = get_configuration(product_id, 'votenet.workflows.vathos.net',
                                    token)

  # get depth image for visualization purposes and convert to m
  inference_url = f'{BASE_URL}/workflows/votenet'
  files = {'files': open(test_image_path, 'rb')}
  values = {
      'product': json.dumps(product),
      'configuration': json.dumps(configuration)
  }

  tic = perf_counter()
  inference_response = requests.post(
      inference_url,
      files=files,
      data=values,
      headers={'Authorization': 'Bearer ' + token},
      timeout=20)

  toc = perf_counter()
  logging.info('Inference took %f s', toc - tic)

  response_json = inference_response.json()

  return response_json['detections']
