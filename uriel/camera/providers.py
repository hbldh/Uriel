#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`camera` -- 
======================

.. module:: camera
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@tobii.com>

Created on 2013-09-05, 16:50

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import traceback
import cv2
import cv2.cv as cv

import uriel.utils.time as utime
from uriel.utils.logging import get_logger

logger = get_logger('uriel')


class WebcameraProviderError(Exception):
    pass


class WebcameraProvider(object):
    """A generator class for providing images from webcameras."""

    def __init__(self, camera_nbr=-1):
        """Constructor for WebcameraHandler"""
        self.camera_nbr = camera_nbr

        self._frame_counter = 0
        self._vc = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            # Error while reading images. Print logging of error.
            logger.error(traceback.format_exception(exc_type, exc_val, exc_tb))
        self.close()

    def __call__(self, max_n_frames=None):
        while self._vc.isOpened() and self._frame_counter < max_n_frames:
            return_value, frame = self._vc.read()
            timestamp = utime.get_epoch()
            if return_value:
                logger.debug("Captured frame at {0}.".format(utime.epoch_to_string(timestamp)))
                yield timestamp, frame
                self._frame_counter += 1
            else:
                logger.debug("Got return value: {0}!".format(return_value))
                raise StopIteration()

    def open(self):
        # Create a video capture object with this camera.
        self._vc = cv2.VideoCapture(self.camera_nbr)
        # Wait some time to let it register as open.
        cv2.waitKey(100)

        if not self._vc.isOpened():
            raise WebcameraProviderError("Could not open the camera!")

        logger.info("Initializing camera...")
        self._vc.set(cv.CV_CAP_PROP_GAIN, 2.0)
        # Reading 10 frames just to let the camera focus and establish lighting parameters.
        for k in xrange(10):
            self._vc.read()
            cv2.waitKey(1)
        logger.info("Initialization done.")

    def close(self):
        self._vc.release()
        self._vc = None
        self._frame_counter = 0
        logger.info("Released the webcamera...")

    def get_configuration_parameters(self):
        """
        CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
        CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
        CV_CAP_PROP_FPS Frame rate.
        CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
        CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
        CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
        CV_CAP_PROP_HUE Hue of the image (only for cameras).
        CV_CAP_PROP_GAIN Gain of the image (only for cameras).
        CV_CAP_PROP_EXPOSURE Exposure (only for cameras).

        :return: Dictionary of parameters for camera.
        :rtype: dict

        """
        if self._vc.isOpened():
            return {'FRAME_WIDTH': self._vc.get(cv.CV_CAP_PROP_FRAME_WIDTH),
                    'FRAME_HEIGHT': self._vc.get(cv.CV_CAP_PROP_FRAME_HEIGHT),
                    'FPS': self._vc.get(cv.CV_CAP_PROP_FPS),
                    'BRIGHTNESS': self._vc.get(cv.CV_CAP_PROP_BRIGHTNESS),
                    'CONTRAST': self._vc.get(cv.CV_CAP_PROP_CONTRAST),
                    'SATURATION': self._vc.get(cv.CV_CAP_PROP_SATURATION),
                    'HUE': self._vc.get(cv.CV_CAP_PROP_HUE),
                    'GAIN': self._vc.get(cv.CV_CAP_PROP_GAIN),
                    'EXPOSURE': self._vc.get(cv.CV_CAP_PROP_EXPOSURE)}
        else:
            raise WebcameraProviderError("Camera was not opened yet!")

