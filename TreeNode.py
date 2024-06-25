# Clase para representar un nodo del árbol
# Nodo del árbol sintáctico
class TreeNode:
    def __init__(self, node_type, token_type=None, value=None, children=None):
        self.node_type = node_type
        self.token_type = token_type
        self.value = value
        self.children = children if children is not None else []

    @staticmethod
    def new(node_type, token_type=None, value=None):
        return TreeNode(node_type, token_type, value)