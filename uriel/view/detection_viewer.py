#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`detection_viewer` -- 
======================

.. module:: detection_viewer
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-08, 20:01

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import traceback
import cv2
import numpy as np

from uriel.utils.logging import get_logger

logger = get_logger('uriel')


class DetectionViewerException(Exception):
    pass


class DetectionViewer(object):
    """A tool for displaying OpenCV images and detections in the image."""

    def __init__(self, name="Uriel Detection Viewer"):
        """Constructor for DetectionViewer"""
        self.name = name

        self._start_time = None
        self._timestamps = []
        self._last_timestamp = None

    def __enter__(self):
        cv2.namedWindow(self.name)
        self._start_time = self._clock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            # No exception. Just destroy window and be done with it.
            cv2.destroyWindow(self.name)
        else:
            # Error while displaying images. Print logging of error.
            logger.error(traceback.format_exception(exc_type, exc_val, exc_tb))

    def __call__(self, *args, **kwargs):
        if len(args) != 0:
            frame = args[0]
            if len(args) == 2:
                detections = args[1]
            else:
                detections = {}

            # Apply timestamp to image.
            timestamp = self._clock() - self._start_time
            self._draw_string(frame, (20, 20),
                              'Time: {0:.1f} ms'.format(timestamp*1000))

            if self._last_timestamp:
                self._timestamps.append(timestamp - self._last_timestamp)
                self._draw_string(frame, (20, 40),
                                  'FPS: {0:.1f} Hz'.format(1. / np.mean(self._timestamps)))

            # Plot detections from main classifier.
            self._draw_rects(frame, detections.keys(), (0, 255, 0))
            for main_detection in detections.keys():
                if detections[main_detection]:
                    # Nested detection as well. Plot these as well.
                    x1, y1, x2, y2 = main_detection
                    vis_roi = frame[y1:y2, x1:x2]
                    self._draw_rects(vis_roi, detections[main_detection], (0, 0, 255))

            cv2.imshow(self.name, frame)
            cv2.waitKey(1)
            self._last_timestamp = timestamp
        else:
            raise DetectionViewerException("No frame sent in!")

    def _clock(self):
        return cv2.getTickCount() / cv2.getTickFrequency()

    def _draw_string(self, dst, (x, y), s):
        cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv2.CV_AA)
        cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)

    def _draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)