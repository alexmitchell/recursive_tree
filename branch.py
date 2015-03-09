from random import random

class Branch:
    max_depth = 1
    branch_count = 0
    def __init__(self, depth):
        # Current depth of tree starting at 0.
        # Will be less than Branch.max_depth
        # Ex: max_depth of 10 means branches will be depth 0 through 9.
        Branch.branch_count += 1
        self.depth = depth
        self.procreate()

    def __del__(self):
        Branch.branch_count -= 1

    def procreate(self):
        #self.procreate_full()
        self.procreate_random()
        #self.procreate_alternating()

    def procreate_full(self):
        child_depth = self.depth + 1
        self.handed_child = None
        self.second_child = None
        if (child_depth < Branch.max_depth):
            self.handed_child = Branch(child_depth)
            self.second_child = Branch(child_depth)

    def procreate_random(self):
        child_depth = self.depth + 1
        self.handed_child = None
        self.second_child = None
        if (child_depth < Branch.max_depth):
            if random() < 0.95**child_depth:
                self.handed_child = Branch(child_depth)
            if random() < 0.95**child_depth:
                self.second_child = Branch(child_depth)

    def procreate_alternating(self):
        child_depth = self.depth + 1
        self.handed_child = None
        self.second_child = None
        if (child_depth < Branch.max_depth):
            mod = self.depth % 4
            if mod in (0,2,3):
                self.handed_child = Branch(child_depth)
            if mod in (0,1,2):
                self.second_child = Branch(child_depth)

    def set_branch(self, base_vector, branch_vector, attenuation,
                 handed, turn, split):
        # The variables are present in the order that they will be 
        # calculated.

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

    def update_tree_recursion(self):

        child_depth = self.depth + 1
        if (child_depth < Branch.max_depth):
            base_vector = self.base_vector + self.branch_vector

            # Calculate the child vectors.
            attenuated_vector = self.branch_vector * self.attenuation
            handed_vector = attenuated_vector.get_rotated(
                    self.handed * self.turn)
            second_vector = handed_vector.get_rotated(
                    -self.handed * self.split)

            # Children geometry variables
            attenuation = self.attenuation
            turn = self.turn
            split = self.split

            # Set or reset the children then recurse.
            if self.handed_child is not None:
                self.handed_child.set_branch(
                        base_vector, handed_vector,
                        attenuation, self.handed, turn, split)
                self.handed_child.update_tree_recursion()
            if self.second_child is not None:
                self.second_child.set_branch(
                        base_vector, second_vector,
                        attenuation, -self.handed, turn, split)
                self.second_child.update_tree_recursion()

    def draw_recursive(self, draw_line):
        x0, y0 = self.base_vector.get_tuple()
        x1, y1 = (self.base_vector + self.branch_vector).get_tuple()

        draw_line((x0, y0, x1, y1))

        if self.handed_child is not None:
            self.handed_child.draw_recursive(draw_line)
        if self.second_child is not None:
            self.second_child.draw_recursive(draw_line)

    def change_turn(self, turn):
        # Update the turn variable for all downstream branches
        self.turn = turn
        self.update_tree_recursion()

    def change_split(self, split):
        # Update the split variable for all downstream branches
        self.split = split
        self.update_tree_recursion()

    def change_attenuation(self, attenuation):
        # Update the attenuation variable for all downstream branches
        self.attenuation = attenuation
        self.update_tree_recursion()

    def change_branch_vector(self, branch_vector):
        # Update the attenuation variable for all downstream branches
        self.branch_vector = branch_vector
        self.update_tree_recursion()
    
    def change_depth_recursive(self, old_depth):
        child_depth = self.depth + 1
        if child_depth < Branch.max_depth:
            if self.depth + 1 == old_depth:
                # Was a leaf node, but is not now. Tree is expanding.
                self.procreate()
                self.update_tree_recursion()
            else:
                # A normal intermediate branch. Spread the word.
                if self.handed_child is not None:
                    self.handed_child.change_depth_recursive(old_depth)
                if self.second_child is not None:
                    self.second_child.change_depth_recursive(old_depth)
        else:
            # The children branches are no longer allowed. Delete them 
            # if they exist.
            
            self.handed_child = None
            self.second_child = None

