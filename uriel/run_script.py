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

import pprint

from uriel.camera.providers import WebcameraProvider
from uriel.view.frame_viewer import FrameViewer
from uriel.view.frame_saver import FrameSaver
import uriel.utils.time as utime

# # Save while capturing.
# with FrameSaver() as fs:
#     with WebcameraProvider() as wcp:
#         for timestamp, frame in wcp(30):
#             fs(frame, suffix=utime.epoch_to_string(timestamp))

# View while capturing.
with FrameViewer() as fv:
    with WebcameraProvider() as wcp:
        for timestamp, frame in wcp(30):
            fv(frame)
        pprint.pprint(wcp.get_configuration_parameters())

# # Capture first and save later.
# with WebcameraProvider() as wcp:
#     frames = {}
#     for timestamp, frame in wcp(30):
#         frames[timestamp] = frame
#
# with FrameSaver() as fs:
#     for k in sorted(frames.keys()):
#         fs(frames[k], suffix=utime.epoch_to_string(k))