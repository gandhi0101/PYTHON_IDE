class Token:
	def __init__(self, token_type, value, line_no = None):
		self.token_type = token_type
		self.value = value
		self.line_no = line_no


class Node:
	def __init__(self, value, line_no=None, children=None):
		self.value = value
		self.line_no = line_no
		self.type = None
		self.val = None
		self.children = children or []

	def add_child(self, node):
		self.children.append(node)
class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.current_token = None
		self.token_index = -1
		self.errors = []
		self.advance()

	def advance(self):
		self.token_index += 1
		if self.token_index < len(self.tokens):
			self.current_token = self.tokens[self.token_index]
		else:
			self.current_token = None

	def match(self, token_type):
		if self.current_token and self.current_token.token_type == token_type:
			self.advance()
		else:
			expected_token = token_type if token_type else "fin de entrada"
			found_token = (
				self.current_token.token_type
				if self.current_token
				else "fin de entrada"
			)
			self.errors.append(
				f"Se esperaba {expected_token}, se encontró {found_token}"
			)
			self.advance()

	def program(self):
		root = Node("Programa")
		self.match("main")
		self.match("{")
		root.add_child(self.stmts())
		self.match("}")
		return root

	def stmts(self):
		root = Node("Sentencias")
		if self.current_token and self.current_token.token_type in [
			"int",
			"float",
			"id",
			"if",
			"while",
			"{",
			"cin",
			"cout",
			]:

			root.add_child(self.stmt())
		while self.current_token and self.current_token.token_type != "}" and self.current_token.token_type != "end":
			if self.current_token.token_type == "do":
				root.add_child(self.do_while_stmt())
			elif self.current_token.value == "end" or self.current_token.token_type == "else":
				return root
			else:
				root.add_child(self.stmt())
		return root

	def do_while_stmt(self):
		root = Node("SentenciaDo")
		self.match("do")
		root.add_child(self.stmt())  
		while self.current_token and self.current_token.token_type != "until":
			root.add_child(self.stmt())
		self.match("until")
		self.match("(")
		root.add_child(self.expr())
		self.match(")")
		self.match(";")
		return root

	def stmt(self):
		if self.current_token and self.current_token.token_type == "int":
			#root = Node("DeclaraciónInt")
			#self.match("int")

			#root.add_child(self.idList())
			root = self.idListInt()
			#self.match(";")
		elif self.current_token and self.current_token.token_type == "do":
			root = self.do_while_stmt()
		elif self.current_token and self.current_token.token_type == "float":
			#root = Node("DeclaraciónFloat")
			#self.match("float")
			
			#root.add_child(self.idList())
			root = self.idListFloat()
			#self.match(";")
		elif self.current_token and self.current_token.token_type == "id":
			root = Node("Asignación")
			id_node = Node(self.current_token.value, line_no=self.current_token.line_no)
			self.match("id")
			root.add_child(id_node)
			if self.current_token and self.current_token.token_type in ["++", "--"]:
				op_node = None
				if(self.current_token.token_type =="++"):
					op_node = Node("++")
				else:   op_node = Node("--")
				id_node.add_child(op_node)
				self.match(self.current_token.token_type)
				op_node.add_child(Node("1"))
			elif self.current_token and self.current_token.token_type in [
				"<",
				">",
				"<=",
				">=",
				"==",
				"!=",
			]:
				op_node = Node(self.current_token.value)
				self.match(self.current_token.token_type)
				if self.current_token and self.current_token.token_type in [
					"id",
					"num",
				]:
					operand_node = Node(self.current_token.value, line_no=self.current_token.line_no)
					id_node.add_child(operand_node)
					self.match(self.current_token.token_type)
			else:
				self.match("=")
				expr_node = self.expr()
				root.add_child(expr_node)
			self.match(";")
		elif self.current_token and self.current_token.token_type == "if":
			root = Node("SentenciaIf")
			self.match("if")
			if self.current_token and self.current_token.token_type == "(":
				self.match("(")
				expr_node = self.expr()
				root.add_child(expr_node)
				self.match(")")
			stmt_node = self.stmts()
			if self.current_token and self.current_token.token_type == "{":
				self.match("{")
				root.add_child(stmt_node)
				self.match("}")
			else:
				root.add_child(stmt_node)
			if self.current_token and self.current_token.token_type == "else":
				self.match("else")
				else_stmt_node = self.stmts()
				root.add_child(else_stmt_node)
			self.match("end")

		elif self.current_token and self.current_token.token_type == "while":
			root = Node("SentenciaWhile")
			self.match("while")
			self.match("(")
			expr_node = self.expr()
			root.add_child(expr_node)
			self.match(")")
			stmt_node = self.stmt()
			root.add_child(stmt_node)
		elif self.current_token and self.current_token.token_type == "{":
			root = Node("Bloque")
			self.match("{")
			root.add_child(self.stmts())
			self.match("}")
		elif self.current_token and self.current_token.token_type == "cin":
			root = Node("SentenciaInput")
			self.match("cin")
			root.add_child(self.idList())
			self.match(";")
		elif self.current_token and self.current_token.token_type == "cout":
			root = Node("SentenciaOutput")
			self.match("cout")
			root.add_child(self.expr())
			self.match(";")
		else:
			root = Node("Error")
			error_token = self.current_token.value if self.current_token else None
			if error_token:
				self.errors.append(f"Sentencia inválida: {error_token}")
			self.advance()
		return root

	def idListInt(self):
		root = Node("DeclaracionInt")
		self.advance()
		while self.current_token  and  self.current_token.value !=";":
			#self.match("id")
			id_node = Node(self.current_token.value)
			root.add_child(id_node)
			self.advance()
			if self.current_token and self.current_token.value == ",":
				self.advance()
			else:
				self.advance()
				break
	   
		return root
	
	def idListFloat(self):
		root = Node("DeclaracionFloat")
		self.advance()
		while self.current_token  and  self.current_token.value !=";":
			#self.match("id")
			id_node = Node(self.current_token.value)
			root.add_child(id_node)
			self.advance()
			if self.current_token and self.current_token.value == ",":
				self.advance()
			else:
				self.advance()
				break
	   
		return root
	

	def idList(self):
		root = Node("IdList")
		id_node = Node(self.current_token.value, line_no=self.current_token.line_no)
		root.add_child(id_node)
		self.match("id")
		while self.current_token and self.current_token.value == "," and self.current_token.value != ";":
			self.match(",")
			id_node = Node(self.current_token.value, line_no=self.current_token.line_no)
			root.add_child(id_node)
			self.match("id")

		return root

	def expr(self):
		root = self.term()
		while self.current_token and self.current_token.token_type in ["+", "-"]:
			op_node = Node(self.current_token.value)
			self.match(self.current_token.token_type)
			op_node.add_child(root)
			root = op_node
			root.add_child(self.term())

		return root

	def term(self):
		root = self.factor()
		while self.current_token and self.current_token.token_type in ["*", "/"]:
			op_node = Node(self.current_token.value)
			self.match(self.current_token.token_type)
			op_node.add_child(root)
			root = op_node
			root.add_child(self.factor())

		return root

	def factor(self):
		root = self.primary()
		while self.current_token and self.current_token.token_type in [
			"<",
			">",
			"<=",
			">=",
			"==",
			"!=",
		]:
			op_node = Node(self.current_token.value)
			self.match(self.current_token.token_type)
			op_node.add_child(root)
			root = op_node
			root.add_child(self.primary())

		return root

	def primary(self):
		if self.current_token and self.current_token.token_type == "(":
			self.match("(")
			root = self.expr()
			self.match(")")
		elif self.current_token and self.current_token.token_type in ["id", "num"]:
			root = Node(self.current_token.value, line_no=self.current_token.line_no)
			self.match(self.current_token.token_type)
		else:
			root = Node("Error")
			error_token = self.current_token.value if self.current_token else None
			self.errors.append(f"Factor inválido: {error_token}")
			self.advance()
		return root

	def parse(self):
		ast = self.program()
		if self.errors:
			print("Se encontraron errores de sintaxis. La compilación ha fallado.")
		else:
			print("La sintaxis es correcta. La compilación ha sido exitosa.")
		return ast


class SemanticAnalyzer:
	def __init__(self):
		self.errors = []
		self.symbol_table = {}

	def analyze(self, ast):
		self.visit_node(ast)

	def visit_node(self, node):
		if node.value == "DeclaraciónInt":
			self.handle_int_declaration(node)
		elif node.value == "DeclaraciónFloat":
			self.handle_float_declaration(node)
		elif node.value == "Asignación":
			self.handle_assignment(node)

		for child in node.children:
			self.visit_node(child)

	def handle_int_declaration(self, node):
		variable_name = node.children[0].value
		if variable_name in self.symbol_table:
			self.errors.append(f"Duplicado: Variable {variable_name} ya declarada")
		else:
			self.symbol_table[variable_name] = {
				"type": "int",
				"val": node.value,
				"loc":"default_location" ,
				"line_numbers": [node.children[0].line_no],
			}

	def handle_float_declaration(self, node):
		variable_name = node.children[0].value
		if variable_name in self.symbol_table:
			self.errors.append(f"Duplicado: Variable {variable_name} ya declarada")
		else:
			self.symbol_table[variable_name] = {
				"type": "float",
				"val": node.value,
				"loc":"default_location" ,
				"line_numbers": [node.children[0].line_no],
			}

	def handle_assignment(self, node):
		variable_name = node.children[0].value
		if variable_name not in self.symbol_table:
			self.errors.append(f"No declarado: Variable {variable_name} no se ha declarado")
		else:
			# Proceso de asignación
			variable_info = self.symbol_table[variable_name]
			node.children.type = variable_info['type']
			print( variable_info['type'])

			node.children.val = variable_info['value']
			print( variable_info['value'])
			# Aquí puedes agregar más lógica para manejar la asignación de valores
			# Por ejemplo, si el nodo tiene un hijo que representa una expresión, puedes evaluar esa expresión y asignar el valor
			if len(node.children) > 1:
				expr_node = node.children
				# Supongamos que tienes una función para evaluar expresiones
				value = self.evaluate_expression(expr_node)
				node.children.val = value
				variable_info['value'] = value
			




class SemanticProcessor:
	def __init__(self):
		# Código principal
		with open("src/assets/lexico.txt", "r") as file:
				lines = file.readlines()

		# Crear la lista de objetos Token
		self.token_list = []

		for line in lines:
			line = line.strip()
			if line:
				token_parts = line.split("--*")
				if token_parts[1].strip() == "identificador":
					token_type = "id"
					value = token_parts[0].strip()
				elif token_parts[1].strip() == "flotante":
					token_type = "num"
					value = token_parts[0].strip()
				elif token_parts[1].strip() == "entero":
					token_type = "num"
					value = token_parts[0].strip()
				else:
					token_type = token_parts[0].strip()
					value = token_parts[0].strip()
				line_no = token_parts[2].strip()
				token = Token(token_type, value, line_no)
				self.token_list.append(token)

	
		parser = Parser(self.token_list)
		ast = parser.parse()
		#mostar en un archivo el ast 

		# Crear instancia del SemanticAnalyzer y analizar el árbol sintáctico
		semantic_analyzer = SemanticAnalyzer()
		semantic_analyzer.analyze(ast)

		# Guardar errores semánticos en un archivo
		with open("src/assets/errores_semanticos.txt", "w", encoding="utf-8") as error_file:
			for error in semantic_analyzer.errors:
				error_file.write(error + "\n")

		# Anotar el árbol sintáctico
		with open("src/assets/arbol_sintactico_anotado.txt", "w", encoding="utf-8") as annotated_tree_file:
			annotated_tree_file.write("Árbol Sintáctico Anotado:\n")
			self.annotate_tree(ast, output=annotated_tree_file)

		# Crear un archivo de texto para la tabla de símbolos
		self.create_symbol_table_text(semantic_analyzer.symbol_table, "src/assets/tabla_simbolos.txt")
		
		
	# Función para anotar el árbol sintáctico
	def annotate_tree(self, node, level=0, output=None):
		indent = " | " * level
		if output:
			if (node.line_no != None):
				value_str = f"{node.value} ( Línea {node.line_no})"
				if hasattr(node, "type"):
					value_str += f" [Tipo: {node.type}]"
				if hasattr(node, "val"):
					value_str += f" [Valor: {node.val}]"
				output.write(f"{indent}{value_str}\n")
			else:
				value_str = f"{node.value}"
				if hasattr(node, "type"):
					value_str 
				if hasattr(node, "val"):
					value_str
				output.write(f"{indent}{value_str}\n")
		for child in node.children:
			self.annotate_tree(child, level + 1, output)

	# Función para imprimir el árbol anotado y guardarlo en un archivo
	def print_ast(self, node, level=0, is_last_child=False, output=None):
		indent = " | " * level
		if output:
			value_str = f"{node.value} (Línea {node.line_no})"
			if hasattr(node, "type"):
				value_str += f" [Tipo: {node.type}]"
			if hasattr(node, "val"):
				value_str += f" [Valor: {node.val}]"
			output.write(f"{indent}{value_str}\n")
		for i, child in node.children:
			is_last = i == len(node.children) - 1
			self.print_ast(child, level + 1, is_last, output)

	# Función para crear un archivo de texto para la tabla de símbolos
	def create_symbol_table_text(self, symbol_table, filename):
		try:
			with open(filename, "w") as file:
				file.write("Nombre Variable\tTipo\tValor\tRegistro (loc)\tNúmeros de línea\n")
				for variable, data in symbol_table.items():
					line_no_numbers = ", ".join(map(str, data['line_numbers']))
					file.write(f"{variable}\t{data['type']}\t{data['value']}\t{data['loc']}\t{line_no_numbers}\n")
		except Exception as e:
			print(f"Error al crear el archivo de tabla de símbolos: {e}")
	



if __name__ == "__main__":
	SemanticProcessor()