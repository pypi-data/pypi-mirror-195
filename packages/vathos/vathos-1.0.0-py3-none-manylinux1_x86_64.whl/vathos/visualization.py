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

try:
  from imageio import imread
  import mayavi.mlab as mlab
  import trimesh
  VISUALIZATION_ENABLED = True
except ImportError:
  VISUALIZATION_ENABLED = False
  logging.warning('Optional dependencies for 3d visualization not installed!')


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


def visualize_detections(mesh_path, scale, test_image_path, projection_matrix,
                         detections):
  """Visualizes a point cloud and detections."""
  if not VISUALIZATION_ENABLED:
    logging.warning('Visualization is disabled.')
    return

  mesh = trimesh.load(mesh_path, file_type='OBJ', color=(0.5, 0.5, 0.5))
  mesh.apply_scale(scale)

  depth_img_compressed = imread(test_image_path)

  pcl = backproject(0.001 * unpack_short(depth_img_compressed),
                    projection_matrix)

  mlab.figure()
  mlab.points3d(pcl[:, 0], pcl[:, 1], pcl[:, 2], mode='point')

  for detection in detections:

    # frame is missing from the object if ICP has failed
    if 'frame' in detection:
      # pose is in camera coordinates
      pose = np.reshape(np.array(detection['frame'], dtype='f'), (4, 4), 'F')
      vertices = mesh.vertices @ pose[0:3, 0:3].transpose() + np.ones(
          mesh.vertices.shape) @ np.diag(pose[0:3, 3])

      mlab.triangular_mesh(vertices[:, 0],
                          vertices[:, 1],
                          vertices[:, 2],
                          mesh.faces,
                          color=(0.6, 0.2, 0.2),
                          opacity=0.5)

  mlab.show()
