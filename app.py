import pyglet
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINES)
    glVertex2i(0, 0)
    glVertex2i(window.width, window.height)
    glEnd()

pyglet.app.run()