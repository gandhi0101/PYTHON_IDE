from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class TreeViewSemantic (QMainWindow):
	def __init__(self, file_path):
		
		# Crear un modelo de datos personalizado
		self.model = QStandardItemModel()
		root_item = self.model.invisibleRootItem()

		# Leer el árbol sintáctico desde el archivo
		self.ast = self.read_ast_from_file(file_path)

		# Crear el modelo a partir del AST
		self.create_model_from_ast( root_item,self.model)

		# Crear el árbol
		

		# Agregar el árbol a la ventana
	def get_tree_view(self):
		return self.tree_view

	
	def read_ast_from_file(self, file_path):
		ast = []  # Aquí debes procesar las líneas y construir la estructura del árbol
		with open(file_path, "r", encoding="utf-8") as f:
			lines = f.readlines()
			for line in lines:
				depth = line.count("|")  # Contar el número de caracteres "|" al principio para determinar la profundidad
				ast.append((line.strip(), depth))  # Agregar la línea y su profundidad
		return ast

	def create_model_from_ast(self,  parent_item, model):
		stack = []  # Usaremos una pila para rastrear los elementos padres
		for node, depth in self.ast:
			node = node.replace("| ", "").strip()
			item = QStandardItem(node)  # Crea un QStandardItem con el valor del nodo
			if depth == 0:
				# Si la pila está vacía, este es el primer elemento (raíz)
				parent_item.appendRow(item)
				stack.append(item)
			else:
				# Si la pila no está vacía, ajusta la jerarquía según la profundidad
				while len(stack) > depth:
					stack.pop()  # Retrocede en la jerarquía
				stack[-1].appendRow(item)  # Agrega el item al padre actual
				stack.append(item)  # Empuja este elemento a la pila

