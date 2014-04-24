#!/usr/bin/env python
import pyglet

# direct opengl commands to this window
window = pyglet.window.Window()


@window.event
def on_draw():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glBegin(pyglet.gl.GL_LINES)

    pyglet.gl.glVertex2f(5, 5)
    pyglet.gl.glVertex2f(5, 100)

    pyglet.gl.glVertex2f(100, 5)
    pyglet.gl.glVertex2f(100, 100)

    pyglet.gl.glVertex2f(100, 100)
    pyglet.gl.glVertex2f(5, 100)

    pyglet.gl.glVertex2f(100, 5)
    pyglet.gl.glVertex2f(5, 5)
    pyglet.gl.glEnd()


if __name__ == "__main__":
    pyglet.app.run()
