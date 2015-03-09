#!/usr/bin/env python3

import pyglet
from pyglet.window import key

from vecrec import Vector
from math import pi
from branch import Branch
        
def print_instructions():
    def print_key_pair(increase_key, decrease_key, value):
        print(increase_key, ": Increase ", value, ".", sep="")
        print(decrease_key, ": Decrease ", value, ".", sep="")

    print()
    print("Keys:")
    print("I: Print the instructions.")
    print_key_pair("Up Arrow", "Down Arrow", "turn angle")
    print_key_pair("Right Arrow", "Left Arrow", "split angle")
    print_key_pair("A", "S", "attenuation")
    print_key_pair("Q", "W", "branch length")
    print_key_pair("Z", "X", "maximum tree depth")
    print("Backspace: Generate a new tree.")
    print("Escape: Close the program.")
    print()


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
    if symbol == key.I:
        print_instructions()
    handle_turn_change(symbol)
    handle_split_change(symbol)
    handle_attenuation_change(symbol)
    handle_branch_vector_change(symbol)
    handle_tree_change(symbol)
    handle_depth_change(symbol)

def handle_turn_change(symbol):
    global init_turn
    if symbol == key.UP:
        init_turn += turn_step
    elif symbol == key.DOWN:
        init_turn -= turn_step
    else:
        return
    print("Changing turn angle to", init_turn, end="... ")#*180/pi)
    root.change_turn(init_turn*pi/180)
    print("Done!")

def handle_split_change(symbol):
    global init_split
    if symbol == key.RIGHT:
        init_split += split_step
    elif symbol == key.LEFT:
        init_split -= split_step
    else:
        return
    print("Changing split angle to", init_split, end="... ")#*180/pi)
    root.change_split(init_split*pi/180)
    print("Done!")

def handle_attenuation_change(symbol):
    global init_attenuation
    if symbol == key.A:
        init_attenuation += attenuation_step
    elif symbol == key.S:
        init_attenuation -= attenuation_step
    else:
        return
    print("Changing attenuation to", init_attenuation, end="... ")
    root.change_attenuation(init_attenuation)
    print("Done!")

def handle_branch_vector_change(symbol):
    global branch_vector
    if symbol == key.Q:
        branch_vector += branch_vector_step
    elif symbol == key.W:
        branch_vector -= branch_vector_step
    else:
        return
    print("Changing root branch vector to", branch_vector, end="... ")
    root.change_branch_vector(branch_vector)
    print("Done!")

def handle_tree_change(symbol):
    if symbol == key.BACKSPACE:
        global root
        # root.teardown()
        print("Generating a new tree", end="... ")
        root = generate_tree()
        print("Done!")
        print("   ", Branch.branch_count, " branches created.")

def handle_depth_change(symbol):
    global max_depth
    old_depth = max_depth
    old_count = Branch.branch_count
    if symbol == key.Z:
        max_depth += 1
    elif symbol == key.X:
        if max_depth > 1:
            max_depth -= 1
        else:
            print("Minimum depth is 1")
            return
    else:
        return

    print("Changing the maximum depth to", max_depth, end="... ")
    Branch.max_depth = max_depth
    root.change_depth_recursive(old_depth)
    print("Done!")

    new_count = Branch.branch_count
    count_diff = new_count - old_count
    if count_diff > 0:
        print("   ", count_diff , "branches" if count_diff>1 else "branch", "created for a new total of ", new_count, " branches.")
    elif count_diff < 0:
        print("   ", -count_diff , "branches" if -count_diff>1 else "branch", "destroyed for a new total of ", new_count, " branches.")
    else:
        print("   No branches created or destroyed for a total of ", new_count, " branches.")


print_instructions()
pyglet.app.run()
