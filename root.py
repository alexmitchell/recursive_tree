from kxg import vecrec.Vector
from math import pi
from branch import Branch

class Root:
    def __init__(self):
        # Default variables for the root branch.

        max_depth = 5
        base_vector = Vector.null()
        branch_vector = Vector(0, 1)
        attenuation = 0.5
        handed = 1
        turn = pi/6
        split = pi/3

        self.branch = Branch(
                self, depth, base_vector, branch_vector,
                attenuation, handed, turn, split)
        Branch.max_depth = max_depth

    def generate_tree():
        self.branch.generate_tree_recursion()
