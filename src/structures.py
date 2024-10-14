class Node:
        def __init__(self, value, line_no=None, type=None, val=None, num_type=None):
            self.value = value
            self.line_no = line_no
            self.type = type
            self.val = val
            self.num_type = num_type
            self.children = []
            self.parent = None
            self.siblings = []

        def add_child(self, child):
            child.parent = self
            self.children.append(child)
            if len(self.children) > 1:
                self.children[-1].siblings = self.children[:-1]

class Token:
        def __init__(self, token_type, value, line_no, num_type=None):
            self.token_type = token_type
            self.value = value
            self.line_no = line_no
            self.num_type = num_type
