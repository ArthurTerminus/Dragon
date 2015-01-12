# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

TRACE = True
DEBUG = False


class DragonModel(object):
    """ドラゴンのモデル。"""

    def __init__(self):
        """ドラゴンのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._triangles = []
        self._eye_point = [-5.5852450791872, 3.07847342734, 15.794105252496]
        self._sight_point = [0.27455347776413, 0.20096999406815, -0.11261999607086]
        self._up_vector = [0.1018574904194, 0.98480906061847, -0.14062775604137]
        self._fovy = 12.642721790235
        self._display_list = None
        self._view = None

        return


class DragonView(object):
    """ドラゴンのビュー。"""

    def __init__(self, a_model):
        """ドラゴンのビューのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_model
        self._controller = DragonController(self)
        self._angle_x = 0.0
        self._angle_y = 0.0
        self._angle_z = 0.0
        self._width = 400
        self._height = 400

        return


class DragonController(object):
    """ドラゴンのコントローラ。"""

    def __init__(self, a_view):
        """ドラゴンのコントローラのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_view._model
        self._view = a_view

        return


class DragonTriangle(object):
    """ドラゴンの三角形。"""

    def __init__(self, vertex1, vertex2, vertex3):
        """ドラゴンの三角形のコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self._vertex3 = vertex3

        return


def main():
    """ドラゴンの立体データを読み込んで描画する。"""
    if TRACE: print __name__, main.__doc__

    a_model = DragonModel()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
