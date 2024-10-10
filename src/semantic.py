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
		self.parent = None  # Atributo para rastrear el padre del nodo en el árbol
		self.children = children or []

	def add_child(self, node):
		node.parent = self
		self.children.append(node)

	def __repr__(self):
		return f"Node(value={self.value}, type={self.type}, val={self.val}, line_no={self.line_no})"
		

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
			id_node = Node(self.current_token.value, line_no=self.current_token.line_no, type = self.current_token.token_type, val = 0)
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
				root.val = self.current_token.value
				#en el hijo (lista hijo ) hacer un recoriddo de la lista para asignar los valores
				if(len(root.children)== 1):
					root.children[0].val = root.val
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
		elif self.current_token and self.current_token.token_type == "num":
			root = Node(self.current_token.value, line_no=self.current_token.line_no, val=self.current_token.value, type=self.current_token.token_type)
			self.match(self.current_token.token_type)

		elif self.current_token and self.current_token.token_type == "id":

			root = Node(self.current_token.value, 
			   line_no=self.current_token.line_no, 
			   type = self.current_token.token_type
			   ) 
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
	def __init__(self, ast):
		self.ast = ast
		self.errors = []
		self.symbol_table = {}
		self.memoria = []

	def analyze(self, ast):
		self.visit_node(ast)

	def visit_node(self, node):
		
		if node.value == "DeclaraciónInt":
			self.handle_int_declaration(node)
		elif node.value == "DeclaraciónFloat":
			self.handle_float_declaration(node)
		elif node.value == "Asignación":
			self.handle_assignment(node, current_node = node.children)

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

	def handle_assignment(self, node, current_node):
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
				
	def evaluate_expression(self, parentnode):
		# Recursivamente recorrer el árbol para obtener los valores actuales
		i = 0
		
		if isinstance(parentnode, Node):
			#print(f"Visitando nodo: {parentnode.value}")
			for child in parentnode.children:
				if(child.value == "DeclaracionInt"):
					self.memoria.append(child.children[0].value)
				# elif(child.parent.value == 'Asignación' and child.type == 'id'):
				# 	lista = self.memoria
				# 	self.memoria = [{child.value: child.childre} if v in valores_objetivo else {v: None} for v in valores]
					
				# self.evaluate_expression(child)
		else:
			#print(f"Visitando nodo: {parentnode[0].value}")
			self.evaluate_expression(parentnode[0])
				



class SemanticProcessor:
	def __init__(self):
		# Código principal
		self.memoria = []
		with open("src/assets/lexico.txt", "r") as file:
				lines = file.readlines()

		# Crear la lista de objetos Token
		token_list = []

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
				token_list.append(token)

	
		parser = Parser(token_list)
		ast = parser.parse()
		#mostar en un archivo el ast 

		# Crear instancia del SemanticAnalyzer y analizar el árbol sintáctico
		semantic_analyzer = SemanticAnalyzer(ast)
		semantic_analyzer.analyze(ast)
		#semantic_analyzer.evaluate_expression( parentnode = ast.children)

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
		
	def check_memoria(self, node ):
		for item in self.memoria:  #comparando cada uno de los valores que tengan info
			if node.type != "id" and node.type != 'num': break
			if( node.value == item['value'] ):
				
				if node.val == None :
					node.val = item['val']
					break
	def update_Node_memoria(self, node):
		for item in self.memoria:  #comparando cada uno de los valores que tengan info
			if node.type!= "id" and node.type!= 'num': break
			if( node.value == item['value'] ):
				node.val = item['val'] 
				break
	def update_memoria(self, node):
		for item in self.memoria:  #comparando cada uno de los valores que tengan info
			if node.type!= "id" and node.type!= 'num': break
			if( node.value == item['value'] ):
				item['val'] = node.val
				break
			
	def detectar_operacion(self, node):
		
		if node.value == '*':

			multiplicado = 1
			for child in node.children:
				self.check_memoria(child)
				multiplicado *= int(child.val)
						
			node.val = multiplicado
			node.parent.val = multiplicado
			node.children[0].val = multiplicado
			self.update_memoria(node.children[0])

		if node.value == '/':
			
			
			dividendo = None
			for child in node.children:
				try:
					self.update_Node_memoria(child)
					valor_hijo = int(child.val)
					if valor_hijo == 0:
						raise ZeroDivisionError(f"División por cero en la línea {node.line_no}")
					if dividendo is None:
						dividendo = valor_hijo
					else:
						dividendo /= valor_hijo
				except ValueError:
					print(f"Error: El valor del hijo '{child.val}' no es un número entero válido en la línea {node.line_no}")
					return None
				except ZeroDivisionError as e:
					print(e)
            
			
			node.val = dividendo
			node.parent.val = dividendo
			node.children[0].val = dividendo
			self.update_memoria(node.children[0])

		if node.value == '+':
			suma = 0
			for child in node.children:
				self.check_memoria(child)
				suma += int(child.val)
			node.val = suma
			node.parent.val = suma
			node.children[0].val = multiplicado
			self.update_memoria(node.children[0])
		
		if node.value == '-':
			resta = 0
			for child in node.children:
				self.check_memoria(child)
				resta += int(child.val)
			node.val = resta
			node.parent.val = resta
			node.children[0].val = multiplicado
			self.update_memoria(node.children[0])
		# si es operacion exponencial ^
		if node.value == '^':
				exponente = 1
				base = 1
				for child in node.children:
					self.check_memoria(child)
					if child.value == '^':
						exponente = int(child.val)
					else:
						base = int(child.val)
				node.val = base ** exponente
				node.parent.val = base ** exponente
				node.children[0].val = multiplicado
				self.update_memoria(node.children[0])
		# si es operacion modulo %
		if node.value == '%':
			modulo = 1
			dividendo = 1
			for child in node.children:
				self.check_memoria(child)
				if child.value == '%':
					modulo = int(child.val)
				else:
					dividendo = int(child.val)
			if modulo == 0:
				print(f"Error: División por cero en la línea {node.line_no}")
				exit()
			
			node.val = dividendo % modulo
			node.parent.val = dividendo % modulo
			node.children[0].val = multiplicado
			self.update_memoria(node.children[0])


	# Función para anotar el árbol sintáctico
	def annotate_tree(self, node, level=0, output=None):
		indent = " | " * level

				
		if node.parent is not None:
			if node.parent.value == 'Asignación' :
				if self.memoria != []:
					for item in self.memoria:  #comparando cada uno de los valores que tengan info
							if( node.value != item['value'] and node.type == "id"):
								
								self.memoria.append({ 'value':node.value, 'val':node.val})
							else:
								break
							if node.val == None :
								node.val = item['val']
								
				else:
					self.memoria.append({'value':node.value, 'val':node.val})

		#self.detectar_operacion(node)

		if output:
			

			if (node.line_no != None):				
				value_str = f"{node.value} ( Línea {node.line_no})"
				if hasattr(node, "type"):
					value_str += f" [Tipo: {node.type}]"
				if hasattr(node, "val"):
					self.update_Node_memoria(node)
					if (node.val == node.value and node.type == 'id'):
						value_str 
					else:
						value_str += f" [Valor: {node.val}]"
				output.write(f"{indent}{value_str}\n")
			else:
				value_str = f"{node.value}"
				if hasattr(node, "type"):
					value_str 
				if hasattr(node, "val"):
					#asignacion cambia
					if node.value == 'Asignación':
						node.val = node.children[1].val

						if  node.val == None:
							
							self.detectar_operacion(node.children[1])

						value_str += f" [Valor: {node.val}]"
					else:
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