#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`frame_viewer` -- 
======================

.. module:: frame_viewer
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 22:14

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import traceback
import cv2

from uriel.utils.logging import get_logger

logger = get_logger('uriel')


class FrameViewerException(Exception):
    pass


class FrameViewer(object):
    """A tool for displaying OpenCV images."""

    def __init__(self, name="Uriel Frame Viewer"):
        """Constructor for FrameViewer"""
        self.name = name

    def __enter__(self):
        cv2.namedWindow(self.name)
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
            cv2.imshow(self.name, args[0])
            cv2.waitKey(1)
        else:
            raise FrameViewerException("No frame sent in!")

