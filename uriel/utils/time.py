#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`time` -- 
======================

.. module:: time
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbh <henrik.blidh@nedomkull.com>

Created on 2013-09-05, 21:30

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import time
import datetime


def get_epoch():
    return time.time()


def epoch_to_string(epoch_value, n_decimals=6):
    return "{{0:{0}f}}".format(n_decimals).format(epoch_value)


def get_datetime():
    return datetime.datetime.now()


def get_timestring():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")