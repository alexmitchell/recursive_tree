
class Branch:
    max_depth = 1
    def __init__(self, depth, base_vector, branch_vector, attenuation,
                 handed, turn, split):
        # The variables are present in the order that they will be 
        # calculated.

        # Current depth of tree starting at 0.
        # Will be less than Branch.max_depth
        self.depth = depth
        # Position vector of the base of the branch.
        self.base_vector = base_vector
        # Vector representing the branch.
        self.branch_vector = branch_vector
        # Shortening ratio for each iteration.
        self.attenuation = attenuation
        # 1 for left-oriented or -1 right-oriented branch.
        self.handed = handed
        # Angle between this branch and handed-side child branch.
        # Measured as if vector bases were aligned.
        self.turn = turn
        # Angle between the children branches.
        self.split = split

        self.handed_child = None
        self.second_child = None

    def generate_tree_recursion(self):

        child_depth = self.depth + 1
        if (child_depth < Branch.max_depth):
            base_vector = self.base_vector + self.branch_vector

            # Calculate the child vectors.
            proto_vector = self.branch_vector * self.attenuation
            handed_vector = proto_vector.get_rotated(self.handed * self.turn)
            second_vector = handed_vector.get_rotated(-self.handed * self.split)

            # Modify these variables as a function of depth for cooler 
            # effects.
            attenuation = self.attenuation
            turn = self.turn
            split = self.split

            # Make the children.
            self.handed_child = Branch(
                    child_depth, base_vector, handed_vector,
                    attenuation, self.handed, turn, split)
            self.second_child = Branch(
                    child_depth, base_vector, second_vector,
                    attenuation, -self.handed, turn, split)

            # Recurse.
            self.handed_child.generate_tree_recursion()
            self.second_child.generate_tree_recursion()

    def draw_recursive(self, draw_line):
        x0, y0 = self.base_vector.get_tuple()
        x1, y1 = (self.base_vector + self.branch_vector).get_tuple()

        draw_line((x0, y0, x1, y1))

        if self.handed_child is not None:
            self.handed_child.draw_recursive(draw_line)
        if self.second_child is not None:
            self.second_child.draw_recursive(draw_line)

