from OpenGL.GL                  import *

GLSL_SHADER = {
        'VERTEX':         GL_VERTEX_SHADER, 
        'FRAGMENT':       GL_FRAGMENT_SHADER,
        'GEOMETRY':       GL_GEOMETRY_SHADER,
        'TESS_CONTROL':   GL_TESS_CONTROL_SHADER,
        'TESS_EVALUATION':GL_TESS_EVALUATION_SHADER,
        'COMPUTE':        GL_COMPUTE_SHADER }

SHADER_FILE_EXTENSION = {
        "vs":   GLSL_SHADER['VERTEX'],
        "vert": GLSL_SHADER['VERTEX'],
        "gs":   GLSL_SHADER['GEOMETRY'],
        "geom": GLSL_SHADER['GEOMETRY'],
        "tcs":  GLSL_SHADER['TESS_CONTROL'],
        "tes":  GLSL_SHADER['TESS_EVALUATION'],
        "fs":   GLSL_SHADER['FRAGMENT'],
        "frag": GLSL_SHADER['FRAGMENT'],
        "cs":   GLSL_SHADER['COMPUTE'] }

GLSE_TYPE_STRING = {
        GL_FLOAT:        "float",
        GL_FLOAT_VEC2:   "vec2",
        GL_FLOAT_VEC3:   "vec3",
        GL_FLOAT_VEC4:   "vec4",
        GL_DOUBLE:       "double",
        GL_INT:          "int",
        GL_UNSIGNED_INT: "unsigned int",
        GL_BOOL:         "bool",
        GL_FLOAT_MAT2:   "mat2",
        GL_FLOAT_MAT3:   "mat3",
        GL_FLOAT_MAT4:   "mat4", }

class GLSEProgramError(Exception):
    """
    Класс BGLSEProgramErro
    Вызывает исключения при ошибке компиляции GLSEProgram
    """
    pass

class GLSEProgram:
    """
    Класс шейдерной программы
    """
    def __init__(self):
        self._handle = 0
        self._linked = False
        self._uniform_location = {}
        
    def _get_uniform_location(self, name):
        """
        Получает индетефикатор uniforn переменной в шейдерной прогрмме по ее имени
        :param name: Имя переменной 
        :return: Индетефикатор шейдерной программы
        """
        return glGetUniformLocation(self._handle, name);
   
   
    def compile_shader(self, file_name):
        """
        Метод компилируюший шейдер из файла
        :param file_name: Название файла в файловой системе
        """
        with open(file_name, 'r') as f:
            if self._handle <= 0: 
                self._handle = glCreateProgram()
                if self._handle == None: 
                    raise GLSEProgramError("ERROR CREATING SHADER PROGRAM.")   
            if self._handle == 0: 
                raise GLSEProgramError("UNABLE TO CREATE SHADER PROGRAM.")
            try: 
                type_shader = SHADER_FILE_EXTENSION[file_name.split('.')[-1]]
            except KeyError:
                raise GLSEProgramError("NOT FOUND SHADER TYPE: {}".format(type_shader))
            self._compile_shader_from_string(f.read(), type_shader)
        
    def _compile_shader_from_string(self, source, type_shader):

        """
        Метод компилируюший шейдерер из из исходной строки
        :param file_name: Исходная строка
        :paran type_shader: Тип шейдерной программы
        """
        shader_handle = glCreateShader(type_shader)
        if shader_handle == None: 
            raise GLSEProgramError("ERROR CREATING SHADER TYPE: {}".format(type_shader))

        glShaderSource(shader_handle, source)
        glCompileShader(shader_handle)

        error_success = glGetShaderiv(shader_handle, GL_COMPILE_STATUS)
        if error_success != GL_TRUE:
            info_log = glGetShaderInfoLog(shader_handle)
            raise GLSEProgramError("ERROR: SHADER {} \n{}".format(type_shader, info_log.decode()))
        glAttachShader(self._handle, shader_handle);
    
    def link(self):
        """
        Метод линкующий шейдереры в шейдерную программу
        """
        if self._linked: return 
        if self._handle <= 0:
            raise GLSEProgramError("PROGRAM HAS NOT BEEN COMPILED.")
        glLinkProgram(self._handle)

        error_success = glGetProgramiv(self._handle, GL_LINK_STATUS)
        if error_success != GL_TRUE:
            info_log = glGetProgramInfoLog(self._handle)
            raise GLSEProgramError("ERROR::SHADER::PROGRAM::LINKING_FAILED \n", info_log.decode())
        self._linked = True
        self._uniform_location.clear()
             
    def validate(self):
        """
        Метод на проверку на успешность линкования
        """
        if not self.is_linked(): 
            raise GLSEProgramError("PROGRAM IS NOT LINKED.")  
        glValidateProgram(self._handle)

        error_success = glGetProgramiv(self._handle, GL_VALIDATE_STATUS)
        if error_success != GL_TRUE:
            info_log = glGetProgramInfoLog( self._handle)
            raise GLSEProgramError("INVALID SHADER PROGRAM: ".format(info_log.decode()))     

    def use(self):
        """
        Метод указываюший что нужно использовать текущую шейдерную прогрмму при отрисовке
        """
        if self._handle <= 0 or (not self._linked):
            raise GLSEProgramError("SHADER HAS NOT BEEN LINKED")
        glUseProgram( self._handle )

    def get_handle(self):
        """
        Функция возврающий индетефикатор щейдрной прогрммы в OpenGL
        :returb: Индетефикатор OpenGL
        """
        return self._handle
    def is_linked(self):
        """
        Функция возврающее истинное или ложное значние линковки
        :return: bool linked
        """
        return self._linked

    def bind_attrib_location(self, location, name):
        """
        Метод устанавливающий шейдерной прогрмме значения атрибутов из буферов
        :param location: Индетефикатор буффера
        :param name: Название атрибутов в шейдерной прогрмме       
        """
        glBindAttribLocation(self._handle, location, name)
   

    def set_uniform_xyz(self, name, x, y, z):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param x: Значение x
        :param y: Значение y
        :param z: Значение z
        """

        loc = self._get_uniform_location(name)
        glUniform3f(loc, x, y, z);
        
    def set_uniform_v2(self, name, vec2):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param vec2: Вектор dim(2)
        """
        loc = self._get_uniform_location(name)      
        glUniform2f(loc, vec2.x, vec2.y);
       
    def set_uniform_v3(self, name, vec3):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param vec3: Вектор dim(3)
      
        """
        loc = self._get_uniform_location(name);  
        glUniform3f(loc, vec3.x, vec3.y, vec3.z);
        
    def set_uniform_v4(self, name, vec4):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param vec4: Вектор dim(4)
       
        """
        loc = self._get_uniform_location(name) 
        glUniform4f(loc, vec3.x, vec3.y, vec3.z, vec3.w)
       
    def set_uniform_m4(self, name, mat4):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param mat4: Матрица  dim(4*4)
        """
        loc = self._get_uniform_location(name)    
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat4.get());
   
   
    def set_uniform_i(self, name, ival):
        """
        Метод устанавливающий значение Uniform переменных в шейдерной программе
        :param name: Название переменной в шейдерной прогрмме
        :param ival: Значение типа int
        """
        loc = self._get_uniform_location(name)    
        glUniform1i(loc, ival);
   
            
    def get_type_str(self, type_GL):
        try:
            GLSE_TYPE_STRING[type_GL]
        except KeyError:
            return "?"
        else:
            return GLSE_TYPE_STRING[type_GL]
         