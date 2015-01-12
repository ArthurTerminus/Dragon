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

    def display_list(self):
        """ドラゴンのモデルのディスプレイリスト(表示物をコンパイルしたOpenGLコマンド列)を応答する。"""
        if TRACE: print __name__, self.display_list.__doc__

        return self._display_list

    def open(self):
        """ドラゴンのモデルを描画するためのOpenGLのウィンドウを開く。"""
        if TRACE: print __name__, self.open.__doc__

        self._view = DragonView(self)

        glutMainLoop()

        return

    def rendering(self):
        """ドラゴンのモデルをレンダリングする。"""
        if TRACE: print __name__, self.rendering.__doc__

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

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(100, 100)
        glutInitWindowSize(self._width, self._height)
        glutCreateWindow("Dragon")

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self._controller.keyboard)
        glutMouseFunc(self._controller.mouse)
        glutMotionFunc(self._controller.motion)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_NORMALIZE)

        return

    def display(self):
        """OpenGLで描画する。"""
        if TRACE: print __name__, self.display.__doc__

        return

    def reshape(self, width, height):
        """OpenGLを再形成する。"""
        if TRACE: print __name__, self.reshape.__doc__

        return


class DragonController(object):
    """ドラゴンのコントローラ。"""

    def __init__(self, a_view):
        """ドラゴンのコントローラのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_view._model
        self._view = a_view

        return

    def keyboard(self, key, x, y):
        """キーボードを処理する。"""
        if TRACE: print __name__, self.keyboard.__doc__

        return

    def motion(self, x, y):
        """マウスボタンを押下しながらの移動を処理する。"""
        if TRACE: print __name__, self.motion.__doc__

        return

    def mouse(self, button, state, x, y):
        """マウスボタンを処理する。"""
        if TRACE: print __name__, self.mouse.__doc__

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

    def rendering(self):
        """ドラゴンの三角形をレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        return


def main():
    """ドラゴンの立体データを読み込んで描画する。"""
    if TRACE: print __name__, main.__doc__

    a_model = DragonModel()
    a_model.open()

    return 0


if __name__ == '__main__':
    sys.exit(main())