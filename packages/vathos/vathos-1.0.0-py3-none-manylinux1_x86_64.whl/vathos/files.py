# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""File operations."""

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
