#!/usr/bin/env python3

import pyglet

from vecrec import Vector
from math import pi
from branch import Branch
        
# Create the tree
max_depth = 10
depth = 0
base_vector = Vector(350, 0)
branch_vector = Vector(0, 200)
attenuation = 0.6
handed = 1
turn = 3*pi/12
split = 4*pi/12

Branch.max_depth = max_depth
root = Branch(
        depth, base_vector, branch_vector,
        attenuation, handed, turn, split)

root.generate_tree_recursion()

# Display the tree
window = pyglet.window.Window()

def draw_line(coordinates):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', coordinates))

@window.event
def on_draw():
    window.clear()
    root.draw_recursive(draw_line)

pyglet.app.run()

