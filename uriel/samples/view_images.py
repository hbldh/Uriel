#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`view_images` -- Viewing webcamera stream sample
=====================================================

.. module:: view_images
   :platform: Unix, Windows
   :synopsis: Simple example for viewing images from webcamera.

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-08, 19:57

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import sys
from uriel.camera.providers import WebcameraProvider
from uriel.view.frame_viewer import FrameViewer
from uriel.utils.logging import get_logger

logger = get_logger('uriel')


def main(number_of_frames_to_view):
    with FrameViewer() as fv:
        with WebcameraProvider() as wcp:
            for timestamp, frame in wcp(number_of_frames_to_view):
                fv(frame)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        n_frames = 30
    else:
        n_frames = int(argv[1])

    main(n_frames)