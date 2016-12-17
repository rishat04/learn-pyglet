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
    -0.5, 0.5, 0,
    0.5, 0.5, 0,
    0.5, -0.5, 0

]
vertices_gl = (GLfloat * len(vertices))(*vertices)
vbo = GLuint(0)

indices = [0, 1, 2, 0, 2, 3]
indices_gl = (GLfloat * len(indices))(*indices)
ebo = GLuint(0) # Element buffer object

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
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
    #glDrawArrays(GL_TRIANGLES, 0, 3)
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
    glDeleteShader(shader_name)

def init():
    glAttachShader(program, compile_shader(GL_VERTEX_SHADER, vertex_shader))
    glAttachShader(program, compile_shader(GL_FRAGMENT_SHADER, fragment_shader))
    glLinkProgram(program)

    glGenVertexArrays(1, vao)
    glBindVertexArray(vao)

    glGenBuffers(1, ebo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices_gl), indices_gl, GL_STATIC_DRAW)

    glGenBuffers(1, vbo)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_gl), vertices_gl, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), 0)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

if __name__ == '__main__':
    init()
    pyglet.app.run()