import numpy
import math


def cross(v1, v2):
    """
    Функция возвращеюее векторной произведение векторв
    :param v1:  Вектор dim(3)
    :param v2:  Вектор dim(3)
    :return     Вектор dim(3) резултат векторного произведения
    """
    return vec3(v1.y * v2.z - v1.z * v2.y,
                v1.z * v2.x - v1.x * v2.z,
                v1.x * v2.y - v1.y * v2.x)


def dot(v1, v2):
    """
    Функция возвращеюее векторной произведение векторв
    :param v1: Вектор dim(3)
    :param v2: Вектор dim(3)
    :return    Cкаляр резутат скалярного произведения v1 и v2
    """
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def length(v):
    """
    Функция возвращая длинну вектора
    :param v: Вектор dim(3)
    :return Скаляр длинна вектора v
    """
    return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)


def normalize(v):
    """
    Функция возвращая нормализованный вектор
    :param v: Вектор dim(3)
    :return   Нормализованный вектор v
    """
    try:
        g = 1 / length(v)
    except Exception:
        g = 0
    x = v.x * g
    y = v.y * g
    z = v.z * g
    return vec3(x, y, z)


class vec3:
    """
    Класс вектора dim(3)
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z



    def __str__(self):
        return "vec3({},{},{})".format(self.x, self.y, self.z)
    """
    Перегрузка бинарных операций сложения и вычитания векторов,
    а так же перегрузка __mul__ на скалярное произведение
    """
    def __add__(self, value):
        return vec3(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value):
        return vec3(self.x - value.x, self.y - value.y, self.z - value.z)

    def __mul__(self, value):
        return vec3(self.x * value, self.y * value, self.z * value)


class vec2:
    """
    Класс вектора dim(2)
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "vec2({},{})".format(self.x, self.y)

    """
    Перегрузка бинарных операций сложения и вычитания векторов,
    а так же перегрузка __mul__ на скалярное произведение
    """
    def __add__(self, value):
        return vec2(self.x + value.x, self.y + value.y)

    def __sub__(self, value):
        return vec2(self.x - value.x, self.y - value.y)

    def __mul__(self, value):
        return vec2(self.x * value, self.y * value)


class mat4:
    """
    Класс матрицы dim(4*4)
    """
    def __init__(self, arr=None):
        if arr is not None:
            self.m = numpy.array(arr, dtype=numpy.float32)
        else:
            self.m = numpy.identity(4, dtype=numpy.float32)

    def rotateX(self, alpha):
        """
        Метод умножающий текущую матрицу на матрицу
        вращения вокруг оси X на угол alpha
        :param alpha: Угол в радианах
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[1][1] = math.cos(alpha)
        mat4[1][2] = (-math.sin(alpha))
        mat4[2][1] = math.sin(alpha)
        mat4[2][2] = math.cos(alpha)
        self.m = numpy.dot(mat4, self.m)

    def rotateY(self, alpha):
        """
        Метод умножающий текущую матрицу на матрицу
        вращения вокруг оси Y на угол alpha
        :param alpha: Угол в радианах
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][0] = math.cos(alpha)
        mat4[0][2] = math.sin(alpha)
        mat4[2][0] = (-math.sin(alpha))
        mat4[2][2] = math.cos(alpha)
        self.m = numpy.dot(mat4, self.m)

    def rotateZ(self, alpha):
        """
        Метод умножающий текущую матрицу на матрицу
        вращения вокруг оси Z на угол alpha
        :param alpha: Угол в радианах
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][0] = math.cos(alpha)
        mat4[0][1] = (-math.sin(alpha))
        mat4[1][0] = math.sin(alpha)
        mat4[1][1] = math.cos(alpha)
        self.m = numpy.dot(mat4, self.m)

    def rotate(self, alpha, v):
        """
        Метод умножающий текущую матрицу на матрицу
        вращения вокруг вектора v на угол alpha
        :param alpha: Угол в радианах
        :paran v: Вектор dim(3)
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        f = v.get_normal()
        c = math.cos(alpha)
        cd = 1 - math.cos(alpha)
        s = math.sin(alpha)

        mat4[0][0] = c + cd * f.x * f.x
        mat4[0][1] = cd * f.x * f.y - s * f.z
        mat4[0][2] = cd * f.x * f.z + s * f.y
        mat4[1][0] = cd * f.y * f.x + s * f.z
        mat4[1][1] = c + cd * f.y * f.y
        mat4[1][2] = cd * f.y * f.z - s * f.x
        mat4[2][0] = cd * f.z * f.x - s * f.y
        mat4[2][1] = cd * f.z * f.y + s * f.x
        mat4[2][2] = c + cd * f.z * f.z

        self.m = numpy.dot(mat4, self.m)

    def scale(self, x, y, z):
        """
        Метод умножающий текущую матрицу на матрицу
        маштабирования по координатам x, y, z
        :param x: Скляр x
        :paran y: Скляр y
        :param z: Скляр z
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][0] = x
        mat4[1][1] = y
        mat4[2][2] = z
        self.m = numpy.dot(mat4, self.m)

    def translate(self, v):
        """
        Метод умножающий текущую матрицу на матрицу
        перемещения на вектор v
        :param v: Вектор dim(3)
        
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][3] = v.x
        mat4[1][3] = v.y
        mat4[2][3] = v.z
        self.m = numpy.dot(mat4, self.m)

    def set_translate(self, v):
        """
        Метод устанавливающий текущую матрицу на матрицу
        перемещения на вектор v
        :param v: Вектор dim(3)
        
        """
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][3] = v.x
        mat4[1][3] = v.y
        mat4[2][3] = v.z
        self.m = mat4

    def set_look_at(self, eye_v, center_v, up_v):
        """
        Метод устанавливающий текущую матрицу на матрицу вида
        
        :param eye_v: Вектор dim(3) Точка наблюдения
        :param center_v: Вектор dim(3) Направление взгляда
        :param up_v: Вектор dim(3)     Вектор вращения по оси направления взглада
        """
        m = numpy.identity(4, dtype=numpy.float32)
        f = normalize(center_v - eye_v)
        s = normalize(cross(f, up_v))
        u = cross(s, f)
        m[0][0] = s.x
        m[0][1] = s.y
        m[0][2] = s.z
        m[1][0] = u.x
        m[1][1] = u.y
        m[1][2] = u.z
        m[2][0] = -f.x
        m[2][1] = -f.y
        m[2][2] = -f.z
        m[0][3] = -dot(s, eye_v)
        m[1][3] = -dot(u, eye_v)
        m[2][3] =  dot(f, eye_v)

        self.m = m

    def set_perspective(self, fovy, aspect, znear, zfar):
        """
        Метод устанавливающий текущую матрицу на матрицу проекции(перспективную)
        
        :param  fovy:  Скаляр угол fovy
        :param aspect: Скаляр соотнощение сторон
        :param znear:  Скаляр расстояние до ближней плоскости отсечения
        :param zfar:   Скаляр расстояние до дальней плоскости отсечения
        """
        f = 1 / math.tan(fovy / 2)
        a = (zfar + znear) / (zfar - znear)
        b = (2 * zfar * znear) / (zfar - znear)
        mat4 = numpy.identity(4, dtype=numpy.float32)
        mat4[0][0] = f / aspect
        mat4[1][1] = f
        mat4[2][2] = -a
        mat4[2][3] = -b
        mat4[3][2] = -1
        mat4[3][3] =  0
        self.m = mat4

    def set_ortho(self, left, right, bottom, top, near, far):
        """
        Метод устанавливающий текущую матрицу на матрицу проекции(ортогональная)
        :param  left:    Скаляр расстояние до левого края  ближней плоскости отсечения
        :param  right:   Скаляр расстояние до правого края  ближней плоскости отсечения
        :param  bottom:  Скаляр расстояние до нижнего края ближней плоскости отсечения
        :param  top:     Скаляр расстояние до верхнего края ближней плоскости отсечения
        :param  near:    Скаляр расстояние до ближней плоскости отсечения вдоль линии взгляда
        :param  far:     Скаляр расстояние до дальней плоскости отсечения вдоль линии взгляда
        """
        a = right - left
        b = top - bottom
        c = far - near
        d = right + left
        e = top + bottom
        g = far + near
        m = numpy.identity(4, dtype=numpy.float32)
        m[0][0] = 2 / a
        m[0][3] = -(d / a)
        m[1][1] = 2 / b
        m[1][3] = -(e / b)
        m[2][2] = -(2 / c)
        m[2][3] = -(g / c)
        self.m = m

    def transpose(self):
        """
        Метод транспонируюший текущую матрицу
        
        """
        self.m = self.m.transpose()

    def set_inverse_of(self, n):
        """
        Метод устанавливающий текущую матрицу обратнойе ец    
        """
        
        self.m = numpy.linalg.inv(n.get())

    def get(self):
        """
        Функция получающая текующую матрицу
        :return Возвращает матрицу numpy
        """
        return self.m

    def muliply(self, m):
        """
        Метод умножающий  текущую матрицу на матрицу m
        :param m: Матрица dim(4*4) 
        """
        self.m = numpy.dot(m.get(), self.m)
