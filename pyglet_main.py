# importing pyglet module
import pyglet
import pyglet.window.key
from subdivision import PointSubdivision
from objects import Point
from draw import *
from event_managers import *

# TODO: add in mod functions

# width of window
width = 1500

# height of window
height = 1000

# caption i.e title of the window
title = "Conforming Subdivision"

# creating a window
window = pyglet.window.Window(width, height, title, )#resizable=False)

# text 
text = "GeeksforGeeks"

# creating a label with font = times roman
# font size = 36
# aligning it to the centre
label = pyglet.text.Label(text,
						font_name ='Times New Roman',
						font_size = 36,
						x = window.width//2, y = window.height//2,
						anchor_x ='center', anchor_y ='center')

new_label = pyglet.text.Label(text,
						font_name ='Times New Roman',
						font_size = 10,
						x = 25, y = 25)

subdivision = PointSubdivision()
subdivision_drawer = PointSubdivisionDrawer(subdivision)

manager = CircleInputManager()

# on draw event
@window.event
def on_draw(): 
    # clearing the window
    window.clear()
    window.dispatch_events()

    manager.on_draw()
    #subdivision_drawer.draw()

	
# key press event 
@window.event
def on_key_press(symbol, modifier):
    manager.on_key_press(symbol, modifier)
    # # key "C" get press
    # if symbol == pyglet.window.key.C:
        
    #     print("Key C is pressed")


# on mouse drag event
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    # printing some message
    #print(f"{x},{y}   {dx},{dy}")
	
@window.event
def on_mouse_press(x, y, button, modifiers):
    manager.on_mouse_press(x, y, button, modifiers)
    # p = Point(x, y)
    # subdivision.add_point(p)


@window.event
def on_mouse_release(x, y, button, modifiers):
    manager.on_mouse_release(x, y, button, modifiers)

				
# start running the application
pyglet.app.run()
