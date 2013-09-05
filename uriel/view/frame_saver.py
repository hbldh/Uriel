#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`frame_saver` -- 
======================

.. module:: frame_saver
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 22:33

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import traceback
import cv2

from uriel.utils.logging import get_logger

logger = get_logger('uriel')


class FrameSaverException(Exception):
    pass


class FrameSaver(object):
    """A tool for saving OpenCV images to file."""

    def __init__(self, path_to_save_to="~/Uriel", file_prefix="Image_", file_format="png"):
        """Constructor for FrameViewer"""
        self.path_to_save_to = os.path.abspath(os.path.expanduser(path_to_save_to))
        self.filename_template = "{0}{{0}}{{1}}.{1}".format(file_prefix, file_format)

        self._frame_counter = 0

    def __enter__(self):
        if not os.path.exists(self.path_to_save_to):
            logger.info("Created folder: {0}...".format(self.path_to_save_to))
            os.makedirs(self.path_to_save_to)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            # Error while displaying images. Print logging of error.
            logger.error(traceback.format_exception(exc_type, exc_val, exc_tb))

    def __call__(self, *args, **kwargs):
        if len(args) != 0:
            if 'suffix' in kwargs:
                suffix = '_{0}'.format(kwargs['suffix'])
            else:
                suffix = ''
            filepath = os.path.join(self.path_to_save_to, self.filename_template.format(
                str(self._frame_counter).zfill(6), suffix))
            cv2.imwrite(filepath, args[0])
            logger.debug("Wrote file : {0}".format(filepath))
        else:
            raise FrameSaverException("No frame sent in!")
