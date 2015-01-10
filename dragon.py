__author__ = 'Arthur'

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

TRACE = True
DEBUG = False

def main():
    """ドラゴンの立体データを読み込んで描画する。"""
    if TRACE: print __name__.main.__doc__

    return 0

if __name__ == '__main__':
    sys.exit(main())
