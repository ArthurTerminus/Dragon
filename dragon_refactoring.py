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


class OpenGLModel(object):
    """OpenGLモデル。"""

    def __init__(self):
        """OpenGLモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._display_object = []
        self._eye_point = None
        self._sight_point = None
        self._up_vector = None
        self._fovy = self._default_fovy = None
        self._display_list = None
        self._view = None

        return

    def default_controllerew_class(self):
        """OpenGLモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_controllerew_class.__doc__

        return OpenGLController

    def default_view_class(self):
        """OpenGLモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_view_class.__doc__

        return OpenGLView

    def default_window_title(self):
        """OpenGLウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Untitled"

    def display_list(self):
        """OpenGLモデルのディスプレイリスト(表示物をコンパイルしたOpenGLコマンド列)を応答する。"""
        if TRACE: print __name__, self.display_list.__doc__

        if self._display_list == None:
            self._display_list = glGenLists(1)
            glNewList(self._display_list, GL_COMPILE)
            glColor4d(0.5, 0.5, 1.0, 1.0)
            for index, each in enumerate(self._display_object):
                if DEBUG: print index,
                each.rendering()
            glEndList()

        return self._display_list

    def open(self):
        """OpenGLモデルを描画するためのOpenGLのウィンドウを開く。"""
        if TRACE: print __name__, self.open.__doc__

        view_class = self.default_view_class()
        self._view = view_class(self)

        return

    def rendering(self):
        """OpenGLモデルをレンダリングする。"""
        if TRACE: print __name__, self.rendering.__doc__

        glCallList(self.display_list())

        return


class OpenGLView(object):
    """OpenGLビュー。"""

    window_postion = [100, 100]

    @classmethod
    def get_window_postion(a_class):
        """ウィンドウを開くための位置を応答する。"""
        if TRACE: print __name__, a_class.get_window_postion.__doc__

        current_position = a_class.window_postion
        a_class.window_postion = map((lambda value: value + 30), a_class.window_postion)

        return current_position

    def __init__(self, a_model):
        """OpenGLビューのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_model
        controller_class = self._model.default_controllerew_class()
        self._controller = controller_class(self)
        self._angle_x = 0.0
        self._angle_y = 0.0
        self._angle_z = 0.0
        self._width = 400
        self._height = 400

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(*OpenGLView.get_window_postion())
        glutInitWindowSize(self._width, self._height)
        glutCreateWindow(self._model.default_window_title())

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self._controller.keyboard)
        glutMouseFunc(self._controller.mouse)
        glutMotionFunc(self._controller.motion)
        glutWMCloseFunc(self._controller.close)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_NORMALIZE)

        return

    def display(self):
        """OpenGLで描画する。"""
        if TRACE: print __name__, self.display.__doc__

        eye_point = self._model._eye_point
        sight_point = self._model._sight_point
        up_vector = self._model._up_vector
        fovy = self._model._fovy

        aspect = float(self._width) / float(self._height)
        near = 0.01
        far = 100.0

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_point[0], eye_point[1], eye_point[2],
                  sight_point[0], sight_point[1], sight_point[2],
                  up_vector[0], up_vector[1], up_vector[2])

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, 0.0)
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1.0)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, 0.0, -1.0])
        glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 90.0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0)
        glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)
        glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)

        self.display_axes()

        glRotated(self._angle_x, 1.0, 0.0, 0.0)
        glRotated(self._angle_y, 0.0, 1.0, 0.0)
        glRotated(self._angle_z, 0.0, 0.0, 1.0)

        self._model.rendering()

        glutSwapBuffers()

        return

    def display_axes(self):
        """世界座標系を描画する。"""
        if TRACE: print __name__, self.display_axes.__doc__

        glBegin(GL_LINES)
        glColor([1.0, 0.0, 0.0, 1.0])
        glVertex([-1.000, 0.0, 0.0])
        glVertex([1.618, 0.0, 0.0])
        glColor([0.0, 1.0, 0.0, 1.0])
        glVertex([0.0, -1.000, 0.0])
        glVertex([0.0, 1.618, 0.0])
        glColor([0.0, 0.0, 1.0, 1.0])
        glVertex([0.0, 0.0, -1.000])
        glVertex([0.0, 0.0, 1.618])
        glEnd()

        return

    def reshape(self, width, height):
        """OpenGLを再形成する。"""
        if TRACE: print __name__, self.reshape.__doc__

        self._width = width
        self._height = height

        glViewport(0, 0, width, height)

        return


class OpenGLController(object):
    """OpenGLコントローラ。"""

    def __init__(self, a_view):
        """OpenGLコントローラのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_view._model
        self._view = a_view

        return

    def close(self):
        """ウィンドウを閉じる際の処理をする。"""
        if TRACE: print __name__, self.close.__doc__

        sys.exit(0)

        return

    def keyboard(self, key, x, y):
        """キーボードを処理する。"""
        if TRACE: print __name__, self.keyboard.__doc__

        if key in "qQ\33":
            sys.exit(0)
        if key == 'r' or key == 'R':
            self._view._angle_x = 0.0
            self._view._angle_y = 0.0
            self._view._angle_z = 0.0
            self._model._fovy = self._model._default_fovy
        if key == 'x':
            self._view._angle_x += 1.0
        if key == 'y':
            self._view._angle_y += 1.0
        if key == 'z':
            self._view._angle_z += 1.0
        if key == 'X':
            self._view._angle_x -= 1.0
        if key == 'Y':
            self._view._angle_y -= 1.0
        if key == 'Z':
            self._view._angle_z -= 1.0
        if key == 's':
            self._model._fovy += 1.0
        if key == 'S':
            self._model._fovy -= 1.0

        self._view.display()  # glutPostRedisplay()

        return

    def motion(self, x, y):
        """マウスボタンを押下しながらの移動を処理する。"""
        if TRACE: print __name__, self.motion.__doc__

        print "motion at (" + str(x) + ", " + str(y) + ")"

        return

    def mouse(self, button, state, x, y):
        """マウスボタンを処理する。"""
        if TRACE: print __name__, self.mouse.__doc__

        if button == GLUT_LEFT_BUTTON:
            print "left",
        elif button == GLUT_MIDDLE_BUTTON:
            print "middle"
        elif button == GLUT_RIGHT_BUTTON:
            print "right",
        else:
            pass

        print "button is",

        if state == GLUT_DOWN:
            print "down",
        elif state == GLUT_UP:
            print "up",
        else:
            pass

        print "at (" + str(x) + ", " + str(y) + ")"

        return


class OpenGLObject(object):
    """OpenGLオブジェクト。"""

    def __init__(self):
        """OpenGLオブジェクトのコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        self._rgb = [1.0, 1.0, 1.0]

        return

    def rendering(self):
        """OpenGLオブジェクトをレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        glColor4d(self._rgb[0], self._rgb[1], self._rgb[2], 1.0)

        return

    def rgb(self, red, green, blue):
        """OpenGLオブジェクトの色を設定する。"""
        if DEBUG: print __name__, self.rgb.__doc__

        self._rgb = [red, green, blue]

        return


class OpenGLTriangle(OpenGLObject):
    """OpenGL三角形。"""

    def __init__(self, vertex1, vertex2, vertex3):
        """OpenGL三角形のコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        super(OpenGLTriangle, self).__init__()
        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self._vertex3 = vertex3

        ux, uy, uz = map((lambda value1, value0: value1 - value0), vertex2, vertex1)
        vx, vy, vz = map((lambda value1, value0: value1 - value0), vertex3, vertex1)
        normal_vector = [(uy * vz - uz * vy), (uz * vx - ux * vz), (ux * vy - uy * vx)]
        distance = sum(map((lambda value: value * value), normal_vector)) ** 0.5
        self._normal_unit_vector = map((lambda vector: vector / distance), normal_vector)

        return

    def rendering(self):
        """OpenGL三角形をレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        super(OpenGLTriangle, self).rendering()
        glBegin(GL_TRIANGLES)
        glNormal3fv(self._normal_unit_vector)
        glVertex3fv(self._vertex1)
        glVertex3fv(self._vertex2)
        glVertex3fv(self._vertex3)
        glEnd()

        return


class OpenGLPolygon(OpenGLObject):
    """OpenGL多角形。"""

    def __init__(self, vertexes):
        """OpenGL多角形のコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        super(OpenGLPolygon, self).__init__()
        self._vertexes = vertexes

        x = 0.0
        y = 0.0
        z = 0.0
        length = len(vertexes)
        for i in range(0, length):
            j = (i + 1) % length
            k = (i + 2) % length
            ux, uy, uz = map((lambda each1, each2: each1 - each2), vertexes[j], vertexes[i])
            vx, vy, vz = map((lambda each1, each2: each1 - each2), vertexes[k], vertexes[j])
            x = x + (uy * vz - uz * vy)
            y = y + (uz * vx - ux * vz)
            z = z + (ux * vy - uy * vx)
        normal_vector = [x, y, z]
        distance = sum(map((lambda each: each * each), normal_vector)) ** 0.5
        self._normal_unit_vector = map((lambda vector: vector / distance), normal_vector)

        return

    def rendering(self):
        """OpenGL多角形をレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        super(OpenGLPolygon, self).rendering()
        glBegin(GL_POLYGON)
        glNormal3fv(self._normal_unit_vector)
        for vertex in self._vertexes:
            glVertex3fv(vertex)
        glEnd()

        return


class DragonModel(OpenGLModel):
    """ドラゴンのモデル。"""

    def __init__(self):
        """ドラゴンのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(DragonModel, self).__init__()
        self._eye_point = [-5.5852450791872, 3.07847342734, 15.794105252496]
        self._sight_point = [0.27455347776413, 0.20096999406815, -0.11261999607086]
        self._up_vector = [0.1018574904194, 0.98480906061847, -0.14062775604137]
        self._fovy = self._default_fovy = 12.642721790235

        filename = os.path.join(os.getcwd(), 'dragon.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Dragon/dragon.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_triangles":
                    number_of_triangles = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_triangles):
                        a_list = get_tokens(a_file)
                        indexes = map(int, a_list[0:3])
                        vertexes = map(index_to_vertex, indexes)
                        a_tringle = OpenGLTriangle(*vertexes)
                        a_tringle.rgb(0.5, 0.5, 1.0)
                        self._display_object.append(a_tringle)

        return

    def default_window_title(self):
        """ドラゴンのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Dragon"


class WaspModel(OpenGLModel):
    """スズメバチのモデル。"""

    def __init__(self):
        """スズメバチのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(WaspModel, self).__init__()
        self._eye_point = [-5.5852450791872, 3.07847342734, 15.794105252496]
        self._sight_point = [0.19825005531311, 1.8530999422073, -0.63795006275177]
        self._up_vector = [0.070077999093727, 0.99630606032682, -0.049631725731267]
        self._fovy = self._default_fovy = 41.480099231656

        filename = os.path.join(os.getcwd(), 'wasp.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Wasp/wasp.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_polygons":
                    number_of_polygons = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        number_of_indexes = int(a_list[0])
                        index = number_of_indexes + 1
                        indexes = map(int, a_list[1:index])
                        vertexes = map(index_to_vertex, indexes)
                        rgb_color = map(float, a_list[index:index + 3])
                        a_polygon = OpenGLPolygon(vertexes)
                        a_polygon.rgb(*rgb_color)
                        self._display_object.append(a_polygon)

        return

    def default_view_class(self):
        """スズメバチのモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_view_class.__doc__

        return WaspView

    def default_window_title(self):
        """スズメバチのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Wasp"


class WaspView(OpenGLView):
    """スズメバチのビュー。"""

    def display_axes(self):
        """世界座標系を描画する。"""
        if TRACE: print __name__, self.display_axes.__doc__

        scaled_by_n = (lambda vertex: map((lambda value: value * 4.0), vertex))
        glBegin(GL_LINES)
        glColor([1.0, 0.0, 0.0, 1.0])
        glVertex(scaled_by_n([-1.00, 0.0, 0.0]))
        glVertex(scaled_by_n([1.68, 0.0, 0.0]))
        glColor([0.0, 1.0, 0.0, 1.0])
        glVertex(scaled_by_n([0.0, -1.00, 0.0]))
        glVertex(scaled_by_n([0.0, 1.68, 0.0]))
        glColor([0.0, 0.0, 1.0, 1.0])
        glVertex(scaled_by_n([0.0, 0.0, -1.00]))
        glVertex(scaled_by_n([0.0, 0.0, 1.68]))
        glEnd()

        return


class BunnyModel(OpenGLModel):
    """うさぎのモデル。"""

    def __init__(self):
        """うさぎのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(BunnyModel, self).__init__()

        filename = os.path.join(os.getcwd(), 'bunny.ply')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Bunny/bunny.ply'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "element":
                    second_string = a_list[1]
                    if second_string == "vertex":
                        number_of_vertexes = int(a_list[2])
                    if second_string == "face":
                        number_of_faces = int(a_list[2])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (lambda index: collection_of_vertexes[index])
                    for n_th in range(number_of_faces):
                        a_list = get_tokens(a_file)
                        indexes = map(int, a_list[1:4])
                        vertexes = map(index_to_vertex, indexes)
                        a_tringle = OpenGLTriangle(*vertexes)
                        a_tringle.rgb(1.0, 1.0, 1.0)
                        self._display_object.append(a_tringle)
                if first_string == "comment":
                    second_string = a_list[1]
                    if second_string == "eye_point_xyz":
                        self._eye_point = map(float, a_list[2:5])
                    if second_string == "sight_point_xyz":
                        self._sight_point = map(float, a_list[2:5])
                    if second_string == "up_vector_xyz":
                        self._up_vector = map(float, a_list[2:5])
                    if second_string == "zoom_height" and a_list[3] == "fovy":
                        self._fovy = self._default_fovy = float(a_list[4])

        return

    def default_view_class(self):
        """うさぎのモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_view_class.__doc__

        return BunnyView

    def default_window_title(self):
        """うさぎのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Stanford Bunny"


class BunnyView(OpenGLView):
    """うさぎのビュー。"""

    def display_axes(self):
        """世界座標系を描画しない。"""
        if TRACE: print __name__, self.display_axes.__doc__

        return


def main():
    """OpenGL立体データを読み込んで描画する。"""
    if TRACE: print __name__, main.__doc__

    a_model = DragonModel()
    a_model.open()

    a_model = WaspModel()
    a_model.open()

    a_model = BunnyModel()
    a_model.open()

    glutMainLoop()

    return 0


if __name__ == '__main__':
    sys.exit(main())