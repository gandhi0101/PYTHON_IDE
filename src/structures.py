class Token:
	def __init__(self, token_type, value, line_no = None):
		self.token_type = token_type
		self.value = value
		self.line_no = line_no


class Node:
	def __init__(self, value, line_no=None, children=None, val = None , type = None):
		#value es el token
		self.value = value
		self.line_no = line_no
		self.type = type
		self.val = val
		self.parent = None  # Atributo para rastrear el padre del nodo en el arbol
		self.children = children or []

	def add_child(self, node):
		node.parent = self
		self.children.append(node)

	def __repr__(self):
		return f"Node(value={self.value}, type={self.type}, val={self.val}, line_no={self.line_no})"
		
