from OpenGL.GL import *
from PyQt5.QtOpenGL import QGLFormat, QGLWidget
from PyQt5.Qt import Qt
from .glseprogram import GLSEProgram, GLSEProgramError
from .mathGL import mat4, vec3, normalize, cross

import numpy
import math

RES_SHADER_VERT = "gui/shader/basic.vert"
RES_SHADER_FRAG = "gui/shader/basic.frag"


class Camera:
    """
    Класс камеры
    """

    def __init__(self, x, y, z, speed=0.1):
        self.position = vec3(x, y, z)
        self.direction = vec3(0, 0, -1)
        self.up = vec3(0, 1, 0)
        self.speed = speed
        self.proection = mat4()

    def set_perspective(self, fov, aspect, znear, zfar):
        """
        Устанавливает матрицу проекции матрицей перспективы
        :param  fovy:  Скаляр угол fovy
        :param aspect: Скаляр соотнощение сторон
        :param znear:  Скаляр расстояние до ближней плоскости отсечения
        :param zfar:   Скаляр расстояние до дальней плоскости отсечения
        """
        self.proection.set_perspective(fov, aspect, znear, zfar)

    def set_ortho(self, left, right, botom, up, near, far):
        """
        Устанавливает матрицу проекции ортогональной матрицей
        :param  left:    Скаляр расстояние до левого края  ближней плоскости отсечения
        :param  right:   Скаляр расстояние до правого края  ближней плоскости отсечения
        :param  bottom:  Скаляр расстояние до нижнего края ближней плоскости отсечения
        :param  top:     Скаляр расстояние до верхнего края ближней плоскости отсечения
        :param  near:    Скаляр расстояние до ближней плоскости отсечения вдоль линии взгляда
        :param  far:     Скаляр расстояние до дальней плоскости отсечения вдоль линии взгляда
        """
        self.proection.set_ortho(left, right, botom, up, near, far)

    def rotate(self, x, y, z):
        """
        Вращает камеру по вектору vec(x,y,z)
        param x: Скаляр x
        param y: Скаляр y
        param z: Скаляр z
        """

        self.direction += vec3(x, y, z)

    def move(self, x, y, z):
        """
        Перемещает  камеру на вектор vec(x,y,z)
        param x: Скаляр x
        param y: Скаляр y
        param z: Скаляр z
        """
        self.position += vec3(x, y, z)

    def get_view_matrix(self):
        """
        Функция возаращающая видовую матрицу
        """
        matrix = mat4()
        matrix.set_look_at(self.position,
                           self.direction + self.position,
                           self.up)
        return matrix

    def get_MVP(self):
        """
        Функция возаращающая произведение матрицы вида и матрицы проекции
        """
        mvp_matrix = mat4()
        mvp_matrix.muliply(self.get_view_matrix())
        mvp_matrix.muliply(self.proection)
        return mvp_matrix


class GLWidget(QGLWidget):
    """
    Класс виджета отображающий изображение
    """

    def __init__(self, image):
        gl_format = QGLFormat()
        gl_format.setVersion(3, 3)
        gl_format.setProfile(QGLFormat.CoreProfile)
        gl_format.setSampleBuffers(True)

        super().__init__(gl_format)
        self.image = image
        self.camera = Camera(0, 0, 1.7, speed=0.01)
        self.key = {Qt.Key_W: False,
                    Qt.Key_S: False,
                    Qt.Key_A: False,
                    Qt.Key_D: False,
                    Qt.Key_Up: False,
                    Qt.Key_Down: False}
        self.startTimer(1)

    def initializeGL(self):

        self.program = GLSEProgram()
        try:
            self.program.compile_shader(RES_SHADER_VERT)
            self.program.compile_shader(RES_SHADER_FRAG)
            self.program.link()
            self.program.validate()
            self.program.use()
        except GLSEProgramError as err:
            print(err)
            exit()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        height = self.image.height / self.image.width
        width = 1.0
        vericles = numpy.array([
            width, height, 0.0, 1.0, 1.0,
            width, -height, 0.0, 1.0, 0.0,
            -width, -height, 0.0, 0.0, 0.0,
            -width, height, 0.0, 0.0, 1.0,

        ], dtype=numpy.float32)

        indices = numpy.array([
            0, 1, 3,
            1, 2, 3
        ], dtype=numpy.uint32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.IBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     vericles.nbytes,
                     vericles,
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     indices.nbytes,
                     indices,
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glBindVertexArray(self.VAO)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))
        glBindVertexArray(0)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width, self.image.height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, self.image.pix_map)

        glBindTexture(GL_TEXTURE_2D, 0)
        self.model = mat4()

    def paintGL(self):
        """
        Переопределение метода рисования
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.program.set_uniform_m4('u_ModelMatrix', self.model)
        self.program.set_uniform_m4('u_MVP', self.camera.get_MVP())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(glGetUniformLocation(self.program.get_handle(), 'u_Texture'), 0)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)
        self.swapBuffers()

    def resizeGL(self, width, height):
        """
        Переопределение фунции изменения размера
        """
        glViewport(0, 0, width, height)
        self.camera.set_perspective(math.pi / 4, width / height, 0.01, 100)

    def keyPressEvent(self, event):
        """
        Метод переопределяет событя нажатия клавиш клавиатур
        Перемещает камеру при нажатии на клавиши
        """
        if event.nativeVirtualKey() in self.key:
            self.key[event.nativeVirtualKey()] = True

        if event.key() in self.key:
            self.key[event.key()] = True

    def move_camera(self):
        """
        Метод вызываетмый при нажатиях и отпусканиях клавиш клавиатуры
        """
        if self.key[Qt.Key_W]:
            self.camera.position += (self.camera.up * self.camera.speed)

        if self.key[Qt.Key_S]:
            self.camera.position -= (self.camera.up * self.camera.speed)

        if self.key[Qt.Key_A]:
            self.camera.position += (
                normalize(cross(self.camera.up, self.camera.direction)) * self.camera.speed)

        if self.key[Qt.Key_D]:
            self.camera.position += (
                normalize(cross(self.camera.direction, self.camera.up)) * self.camera.speed)

        if self.key[Qt.Key_Up]:
            self.camera.position += (self.camera.direction * self.camera.speed)

        if self.key[Qt.Key_Down]:
            self.camera.position -= (self.camera.direction * self.camera.speed)

    def keyReleaseEvent(self, event):
        """
        Метод переопределяет событя отпускания клавиш клавиатуры
        Перемещает камеру при нажатии на клавиши
        """
        if event.nativeVirtualKey() in self.key:
            self.key[event.nativeVirtualKey()] = False

        if event.key() in self.key:
            self.key[event.key()] = False


    def mouseDoubleClickEvent(self, event):
        """
        Метод переопределяет двойного клика по текущему виджету
        Устанавливет фокус на текущий виджет
        """
        self.setFocus()

    def timerEvent(self, *args, **kwargs):
        self.move_camera()
        self.paintGL()