#!/usr/bin/env python3

import pyglet
from pyglet.window import key

from vecrec import Vector
from math import pi
from branch import Branch
        
window = pyglet.window.Window()

# Default variable values
max_depth = 10
depth = 0
base_vector = Vector(window.width/2, 0)
branch_vector = Vector(0, window.height/3)
init_attenuation = 0.6
init_handed = 1
init_turn = 45 #3*pi/12
init_split = 60 #4*pi/12

def generate_tree():
    global max_depth, base_vector, branch_vector, init_attenuation
    global init_handed, init_turn, init_split

    Branch.max_depth = max_depth
    root = Branch(depth)
    root.set_branch(
            base_vector, branch_vector, init_attenuation,
            init_handed, init_turn*pi/180, init_split*pi/180)
    root.update_tree_recursion()

    return root


root = generate_tree()

# Display the tree
def draw_line(coordinates):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', coordinates))

@window.event
def on_draw():
    window.clear()
    root.draw_recursive(draw_line)


# User input
turn_step = 5 #pi / 30
split_step = 5 #pi / 30
attenuation_step = 0.01
branch_vector_step = branch_vector/10

@window.event
def on_key_press(symbol, modifier):
    global init_turn, init_split, init_attenuation, branch_vector

    if symbol == key.UP:
        init_turn += turn_step
        root.change_turn(init_turn*pi/180)
        print("Changing turn angle to", init_turn)#*180/pi)

    elif symbol == key.DOWN:
        init_turn -= turn_step
        root.change_turn(init_turn*pi/180)
        print("Changing turn angle to", init_turn)#*180/pi)

    elif symbol == key.RIGHT:
        init_split += split_step
        root.change_split(init_split*pi/180)
        print("Changing split angle to", init_split)#*180/pi)

    elif symbol == key.LEFT:
        init_split -= split_step
        root.change_split(init_split*pi/180)
        print("Changing split angle to", init_split)#*180/pi)

    elif symbol == key.A:
        init_attenuation += attenuation_step
        root.change_attenuation(init_attenuation)
        print("Changing attenuation to", init_attenuation)

    elif symbol == key.S:
        init_attenuation -= attenuation_step
        root.change_attenuation(init_attenuation)
        print("Changing attenuation to", init_attenuation)

    elif symbol == key.Q:
        branch_vector += branch_vector_step
        root.change_branch_vector(branch_vector)
        print("Changing root branch vector to", branch_vector)

    elif symbol == key.W:
        branch_vector -= branch_vector_step
        root.change_branch_vector(branch_vector)
        print("Changing root branch vector to", branch_vector)

    elif symbol == key.BACKSPACE:
        global root
        # root.teardown()
        root = generate_tree()
        print("Generating a new tree")


pyglet.app.run()
