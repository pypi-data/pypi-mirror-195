# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""File operations."""

from io import BytesIO

import requests

from vathos import BASE_URL


def upload_files(file_list, token):
  """Uploads one or multiple files.
  
  Args:
    file_list (list): list of paths of files on disk to upload

  Returns:
    list: meta data objects of uploaded files
  """
  upload_body = {}
  for i, file in enumerate(file_list):
    upload_body[f'file_{str(i).zfill(2)}'] = open(file, 'rb')
  upload_response = requests.post(f'{BASE_URL}/blobs',
                                  files=upload_body,
                                  headers={'Authorization': f'Bearer {token}'},
                                  timeout=120)
  return upload_response.json()

def get_file(file_id, token):
  """Downloads a file from the REST API.

  Args:
  file_id (str): id of the file to get

  Returns:
    BytesIO: byte representation of the file
  """
  http_request = requests.get(f'{BASE_URL}/blobs/{file_id}',
                              headers={'Authorization': 'Bearer ' + token},
                              stream=True)
  http_request.raw.decode_content = True

  return BytesIO(http_request.content)