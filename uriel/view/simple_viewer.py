#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`simple_viewer` -- 
======================

.. module:: simple_viewer
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 22:12

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import cv2

from uriel.utils.logging import get_logger

logger = get_logger('uriel')


class SimpleWebcameraViewer(object):

    def __init__(self, name="UrielViewer", camera_nbr=-1):
        """Constructor for WebcameraVideoViewer."""
        self.name = name
        self.camera_nbr = camera_nbr

    def show(self):

        cv2.namedWindow(self.name)
        vc = cv2.VideoCapture(self.camera_nbr)
        cv2.waitKey(100)

        if vc.isOpened():  # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

        while rval:
            cv2.imshow(self.name, frame)
            rval, frame = vc.read()
            key = cv2.waitKey(1000//30)
            if key == 27:  # exit on ESC
                break

        cv2.destroyWindow(self.name)
        vc.release()

    def save(self, folder_to_save_to='~/Uriel', max_nbr_of_files=200):
        folder_to_save_to = os.path.abspath(os.path.expanduser(folder_to_save_to))
        if not os.path.exists(folder_to_save_to):
            os.makedirs(folder_to_save_to)

        vc = cv2.VideoCapture(self.camera_nbr)
        cv2.waitKey(100)

        if vc.isOpened():  # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

        logger.info("Waiting for camera initialization...")
        # Reading 20 frames just to let the camera focus and establish lighting parameters.
        for k in xrange(10):
            rval, frame = vc.read()
            cv2.waitKey(1000//30)

        frame_counter = 0
        while rval:
            if frame_counter >= max_nbr_of_files:
                break
            filename = "Image_{0}.png".format(str(frame_counter).zfill(6))
            cv2.imwrite(os.path.join(folder_to_save_to, filename), frame)
            logger.debug("Wrote file : {0}".format(os.path.join(folder_to_save_to, filename)))
            frame_counter += 1
            rval, frame = vc.read()
        vc.release()