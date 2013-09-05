#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: logging
   :platform: Unix, Windows
   :synopsis: Tools for logging in the Uriel project.

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 17:52

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import logging
import logging.config


def get_logger(logger_name=None):

    try:
        logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.ini'))
        logger = logging.getLogger(logger_name)
    except Exception:
        logger = logging.getLogger('FallbackLogger')
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s]:%(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.warning("Logger {0} could not be found. Using FallbackLogger...".format(
            logger_name))
    return logger
