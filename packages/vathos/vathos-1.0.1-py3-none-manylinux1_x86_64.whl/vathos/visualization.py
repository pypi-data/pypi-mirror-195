# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""Visualization."""

import logging

import numpy as np

from vathos.products import get_product
from vathos.files import get_file

try:
  from imageio import imread
  import mayavi.mlab as mlab
  import trimesh
  VISUALIZATION_ENABLED = True
except ImportError:
  VISUALIZATION_ENABLED = False
  logging.warning('Optional dependencies for 3d visualization not installed!')

# conversion to meters
UNIT_CONVERSION_FACTOR = {'mm': 0.001, 'cm': 0.01, 'dm': 0.1, 'm': 1.0}


def unpack_short(rgb):
  """Unpacks two byte channels into a single channel of type short."""
  return rgb[:, :, 0] + 256 * rgb[:, :, 1]


def backproject(depth, K):
  """Backprojects a depth image into a point cloud."""
  size = depth.shape[::-1]

  u, v = np.meshgrid(np.arange(0, size[0]), np.arange(0, size[1]))

  xyz_image = np.zeros(depth.shape + (3,))

  xyz_image[:, :, 0] = depth / K[0, 0] * (u - K[0, 2])
  xyz_image[:, :, 1] = depth / K[1, 1] * (v - K[1, 2])
  xyz_image[:, :, 2] = depth

  pcl = np.reshape(xyz_image, (xyz_image.shape[0] * xyz_image.shape[1], 3))

  # filter out 0
  pcl = pcl[np.where(pcl[:, 2] > 0)[0], :]

  return pcl


def visualize_detections(detections,
                         test_image_path,
                         token,
                         fitness_threshold=0.7):
  """Visualizes a point cloud and detections.
  
  This function is only executed if mayavi and trimesh are installed.

  Args:
    model_file_name (str): path to a CAD model file on disk. Currently, the only
      supported format is Wavefront OBJ.
    unit (str): unit in which the CAD model is meaured. Must be one of
      `['m', 'dm', 'cm', 'mm']`.
    test_image_path (str): path of the depth image used in inference
    projection_matrix (numpy.ndarray): a $3\\times 3$ projection matrix of the 
      used camera
    detections (list): inferred object poses      
  """
  if not VISUALIZATION_ENABLED:
    logging.warning('Visualization is disabled.')
    return

  product = get_product(detections['product_id'], token)
  projection_matrix = np.reshape(np.array(product['camera']['intrinsics']),
                                 (3, 3), 'F')

  meshes = []
  for obj_model in product['models']:
    mesh = trimesh.load(get_file(obj_model, token),
                        file_type='OBJ',
                        color=(0.5, 0.5, 0.5))
    mesh.apply_scale(UNIT_CONVERSION_FACTOR[product['unit']])
    meshes.append(mesh)

  depth_img_compressed = imread(test_image_path)
  pcl = backproject(0.001 * unpack_short(depth_img_compressed),
                    projection_matrix)

  mlab.figure("Vathos: Cloud Inference",
              bgcolor=(0.0, 0.0666, 0.1137),
              size=(800, 600))
  mlab.points3d(pcl[:, 0], pcl[:, 1], pcl[:, 2], mode='point')

  for detection in detections['detections']:

    # frame is missing from the object if ICP has failed
    if 'frame' in detection and detection.get('fitness',
                                              1.0) > fitness_threshold:
      # might want to use a differrent color for low fitness detections later
      mesh_color = (0.5, 0.6, 0.7)
      # read class and center, depending on use of ICP
      if 'detection' in detection:
        detection_class = detection['detection']['class']
        detection_center = detection['detection']['center']
      else:
        detection_class = detection['class']
        detection_center = detection['center']
      mesh = meshes[int(product['class2product'][str(detection_class)])]

      # pose is in camera coordinates
      pose = np.reshape(np.array(detection['frame'], dtype='f'), (4, 4), 'F')
      vertices = mesh.vertices @ pose[0:3, 0:3].transpose() + np.ones(
          mesh.vertices.shape) @ np.diag(pose[0:3, 3])

      mlab.triangular_mesh(vertices[:, 0],
                           vertices[:, 1],
                           vertices[:, 2],
                           mesh.faces,
                           color=mesh_color,
                           opacity=0.5)
      if detection.get('fitness', False):
        mlab.text3d(x=detection_center[0],
                    y=detection_center[1],
                    z=detection_center[2],
                    text="{:.2f}".format(detection['fitness']),
                    color=(0.95, 0.71, 0.25),
                    scale=0.01)

  mlab.show()
