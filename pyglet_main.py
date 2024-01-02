# importing pyglet module
import pyglet
import pyglet.window.key
from subdivision import PointSubdivision
from objects import Point
from draw import *
from event_managers import *
from pyglet.gl import *
from pyglet.math import *

# width of window
width = 1500

# height of window
height = 1000

# caption i.e title of the window
title = "Conforming Subdivision"

# creating a window
window = pyglet.window.Window(width, height, title)
pyglet.gl.glClearColor(24/255,24/255,24/255,1)



def mod_func(x, y):
    return x + 0.5, y + 0.5

def inverse_mod_func(x, y):
    return x - 0.5, y - 0.5

instruction_bar = InstructionBar(width, height, height * 0.15)
manager = CircleInputManager(mod_func, inverse_mod_func, instruction_bar)

# on draw event
@window.event
def on_draw(): 
    # clearing the window
    window.clear()
    window.dispatch_events()

    manager.on_draw()
    instruction_bar.draw()

# @window.event       
# def on_resize(width, height):
#     pass
#     # glMatrixMode(gl.GL_PROJECTION)
#     # glLoadIdentity()

#     # glViewport(0, 0, width, height)
#     # gluOrtho2D(0, self.default_width, 0, self.default_height)
#     # glMatrixMode(gl.GL_MODELVIEW)
#     # glViewport(0, 0, *window.get_framebuffer_size())
#     # window.projection = Mat4.orthogonal_projection(0, width, 0, height, -255, 255)
    
# @window.event
# def on_resize(width, height):
#     if width != 1500 or height != 1000:
#         window.set_size(1500, 1000)

# key press event 
@window.event
def on_key_press(symbol, modifier):
    global manager

    ret = manager.on_key_press(symbol, modifier)
    if symbol == pyglet.window.key.ENTER and not (ret is None):
        manager = ret


# on mouse drag event
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    # printing some message
    #print(f"{x},{y}   {dx},{dy}")
	
@window.event
def on_mouse_press(x, y, button, modifiers):
    print(x, y)
    manager.on_mouse_press(x, y, button, modifiers)
    # p = Point(x, y)
    # subdivision.add_point(p)


@window.event
def on_mouse_release(x, y, button, modifiers):
    manager.on_mouse_release(x, y, button, modifiers)

				
# start running the application
pyglet.app.run()
