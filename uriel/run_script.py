#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`run_script` -- Run script for Uriel project.
======================

.. module:: run_script
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 16:52

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import cv2
import cv2.cv as cv

from uriel.camera.providers import WebcameraProvider
from uriel.view.detection_viewer import DetectionViewer
from uriel.view.frame_saver import FrameSaver
from uriel.detect.ocv_detector import OCVDetector

detector = OCVDetector('OpenCV Haar Detector, Face->EyeROI',
                       'haarcascade_frontalface_default.xml',
                       'haarcascade_mcs_eyepair_big.xml')

with DetectionViewer() as dv:
    with WebcameraProvider() as wcp:
        for timestamp, frame in wcp(6000):
            # Perform classification in the image.
            detections = detector.classify(frame)
            # Plot the results.
            dv(frame, detections)

            # Listen to ESC key to break the loop.
            if cv2.waitKey(5) == 27:
                break
