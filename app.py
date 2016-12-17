import pyglet
from pyglet.gl import *
from ctypes import *

from pyglet.libs.win32.constants import NULL

window = pyglet.window.Window(width=640, height=480, resizable=True, caption='App')

program = glCreateProgram()

vertex_shader = b'''
    #version 330 core

    layout (location = 0) in vec3 position;

    void main()
    {
        gl_Position = vec4(position, 1.0);
    }

'''

fragment_shader = b'''
    #version 330 core

    out vec4 color;

    void main()
    {
        color = vec4(1.0, 0.5, 0.2, 1.0);
    }
'''

vertices = [
    -0.5, -0.5, 0,
    0.5, -0.5, 0,
    0, 0.5, 0
]
vertices_gl = (GLfloat * len(vertices))(*vertices)
vbo = GLuint(0)

vao = GLuint(0)

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

@window.event
def on_draw():
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)

    glBindVertexArray(vao)
    #Не работает без этих строчек, хотя по урокам не пишут их#
    #glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_gl), vertices_gl, GL_STATIC_DRAW)
    #
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)


def compile_shader(shader_type, shader_source):
    shader_name = glCreateShader(shader_type)
    src_buffer = create_string_buffer(shader_source)
    buf_pointer = cast(pointer(pointer(src_buffer)), POINTER(POINTER(c_char)))
    length = c_int(len(shader_source) + 1)
    glShaderSource(shader_name, 1, buf_pointer, byref(length))
    glCompileShader(shader_name)
    success = GLint(0)
    infoLog = GLchar(0)
    glGetShaderiv(shader_name, GL_COMPILE_STATUS, success)
    if not success:
        glGetShaderInfoLog(shader_name, 512, NULL, infoLog)
        print(infoLog)
    return shader_name

def init():
    vs = compile_shader(GL_VERTEX_SHADER, vertex_shader)
    fs = compile_shader(GL_FRAGMENT_SHADER, fragment_shader)
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    glDeleteShader(vs)
    glDeleteShader(fs)

    glGenVertexArrays(1, vao)
    glGenBuffers(1, vbo)
    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), 0)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

if __name__ == '__main__':
    init()
    pyglet.app.run()