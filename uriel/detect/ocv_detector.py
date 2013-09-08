#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`ocv_detector` -- 
======================

.. module:: ocv_detector
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-08, 20:56

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import traceback
import cv2
import cv2.cv as cv

from uriel.utils.logging import get_logger

logger = get_logger('uriel')


if sys.platform == 'win32':
    path_to_ocv_data_dir = os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.environ['OPENCV_DIR']))), 'data', 'haarcascades')
else:
    raise NotImplementedError("Only Win32 as of yet!")


class OCVDetectorException(Exception):
    pass


class OCVDetector(object):
    """Applying OpenCV detectors."""

    def __init__(self, name="OpenCV Haar detector",
                 main_classifier='haarcascade_frontalface_default.xml',
                 nested_classifier='haarcascade_mcs_eyepair_big.xml'):
        """Constructor for OCVDetector"""
        self.name = name

        # Load the specified classifiers.
        self.main_classifier = cv2.CascadeClassifier(os.path.join(
            path_to_ocv_data_dir, main_classifier))
        if nested_classifier:
            self.nested_classifier = cv2.CascadeClassifier(os.path.join(
                path_to_ocv_data_dir, nested_classifier))
        else:
            self.nested_classifier = None

    def classify(self, frame):
        detection_results = {}

        # Convert to gray scale and perform histogram equalization.
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray_image)

        # Apply main detector.
        main_detections = self._detect(gray, self.main_classifier)
        for md in main_detections:
            x1, y1, x2, y2 = md
            detection_results[tuple(md)] = []
            if self.nested_classifier:
                roi = gray[y1:y2, x1:x2]
                nested_detections = self._detect(roi.copy(), self.nested_classifier)
                for nd in nested_detections:
                    detection_results[tuple(md)].append(nd)

        return detection_results

    def _detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4,
                                         minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        return rects