from math import pow  # Import pow function for exponentiation
from tabulate import tabulate
import structures


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
		"""
		Checks if the current token matches the expected token type. If they match,
		advances to the next token. If they don't match, adds an error message to the
		errors list and advances to the next token.

		Parameters:
		token_type (str): The expected token type.

		Returns:
		None
		"""
		if self.current_token and self.current_token.token_type == token_type:
			self.advance()
		else:
			expected_token = token_type if token_type else "end of input"
			found_token = (
				self.current_token.token_type
				if self.current_token
				else "end of input"
			)
			self.errors.append(
				f"Expected {expected_token}, found {found_token}"
			)
			self.advance()

	def program(self):
		root = structures.Node("Programa")
		self.match("main")
		self.match("{")
		root.add_child(self.stmts())
		self.match("}")
		return root

	def stmts(self):
		root = structures.Node("Sentencias")
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
		root = structures.Node("SentenciaDo")
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
		

		if  self.current_token.token_type == "int":
			#root = structures.Node("DeclaracionInt")
			#self.match("int")

			#root.add_child(self.idList())
			root = self.idListInt()
			#self.match(";")
		elif  self.current_token.token_type == "do":
			root = self.do_while_stmt()
		elif  self.current_token.token_type == "float":
			#root = structures.Node("DeclaracionFloat")
			#self.match("float")
			
			#root.add_child(self.idList())
			root = self.idListFloat()
			#self.match(";")
		elif  self.current_token.token_type == "id":

			root = structures.Node("Asignacion", self.current_token.line_no)
			id_node =structures.Node(self.current_token.value, self.current_token.line_no)
			id_node.identificator = True
			self.match("id")
			root.add_child(id_node)
			if self.current_token.token_type in ["++", "--"]:
				op_node = None
				if self.current_token.token_type == "++":
					op_node =structures.Node("+")
				else:
					op_node =structures.Node("-")
				op_node.add_child(id_node)
				self.match(self.current_token.token_type)
				op_node.add_child(Node("1"))
				root.add_child(op_node)
			elif  self.current_token.token_type in [
				"<",
				">",
				"<=",
				">=",
				"==",
				"!=",
			]:
				op_node =structures.Node(self.current_token.value, self.current_token.line_no)
				self.match(self.current_token.token_type)
				if self.current_token and self.current_token.token_type in [
					"id",
					"num",
				]:
					operand_node = structures.Node(
						self.current_token.value, self.current_token.line_no
					)
					if self.current_token and self.current_token.token_type == "id":
						operand_node.identificator = True
					root.add_child(operand_node)
					self.match(self.current_token.token_type)
			else:
				self.match("=")
				expr_node = self.expr()
				root.add_child(expr_node)
			self.match(";")
		elif  self.current_token.token_type == "if":
			root = structures.Node("SentenciaIf")
			self.match("if")
			if   self.current_token.token_type == "(":
				self.match("(")
				expr_node = self.expr()
				root.add_child(expr_node)
				self.match(")")
			stmt_node = self.stmts()
			if   self.current_token.token_type == "{":
				self.match("{")
				root.add_child(stmt_node)
				self.match("}")
			else:
				root.add_child(stmt_node)
			if   self.current_token.token_type == "else":
				self.match("else")
				else_stmt_node = self.stmts()
				root.add_child(else_stmt_node)
			self.match("end")

		elif   self.current_token.token_type == "while":
			root = structures.Node("SentenciaWhile")
			self.match("while")
			self.match("(")
			expr_node = self.expr()
			root.add_child(expr_node)
			self.match(")")
			stmt_node = self.stmt()
			root.add_child(stmt_node)
		elif self.current_token.token_type == "{":
			root = structures.Node("Bloque")
			self.match("{")
			root.add_child(self.stmts())
			self.match("}")
		elif self.current_token and self.current_token.token_type == "cin":
			root = structures.Node("SentenciaInput")
			self.match("cin")
			root.add_child(self.idList())
			self.match(";")
		elif self.current_token and self.current_token.token_type == "cout":
			root = structures.Node("SentenciaOutput")
			self.match("cout")
			root.add_child(self.expr())
			self.match(";")
		else:
			root = structures.Node("Error")
			error_token = self.current_token.value if self.current_token else None
			if error_token:
				self.errors.append(f"Sentencia invalida: {error_token}")
			self.advance()
		return root

	def idListInt(self):
		root = structures.Node("DeclaracionInt", type="int")
		self.advance()
		self.current_token.token_type = "int"
		while self.current_token  and  self.current_token.value !=";":
			#self.match("int")
			id_node = structures.Node(self.current_token.value, type= 'int', line_no= self.current_token.line_no)
			root.add_child(id_node)
			self.advance()
			if self.current_token and self.current_token.value == ",":
				self.advance()
			else:
				self.advance()
				break
	   
		return root
	
	def idListFloat(self):
		root = structures.Node("DeclaracionFloat")
		self.advance()
		while self.current_token  and  self.current_token.value !=";":
			#self.match("id")
			id_node = structures.Node(self.current_token.value , type = "float", line_no= self.current_token.line_no)
			root.add_child(id_node)
			self.advance()
			if self.current_token and self.current_token.value == ",":
				self.advance()
			else:
				self.advance()
				break
	   
		return root
	

	def idList(self):
		root = structures.Node("IdList")
		id_node = structures.Node(self.current_token.value, line_no=self.current_token.line_no)
		root.add_child(id_node)
		self.match("id")
		while self.current_token and self.current_token.value == "," and self.current_token.value != ";":
			self.match(",")
			id_node = structures.Node(self.current_token.value, line_no=self.current_token.line_no)
			root.add_child(id_node)
			self.match("id")

		return root

	def expr(self):
		root = self.term()
		while self.current_token and self.current_token.token_type in ["+", "-"]:
			op_node = structures.Node(self.current_token.value)
			self.match(self.current_token.token_type)
			op_node.add_child(root)
			root = op_node
			root.add_child(self.term())

		return root

	def term(self):
		root = self.factor()
		while self.current_token and self.current_token.token_type in ["*", "/"]:
			op_node = structures.Node(self.current_token.value)
			self.match(self.current_token.token_type)
			op_node.add_child(root)
			root = op_node
			root.add_child(self.factor())

		return root

	def factor(self):
		root = self.primary()
		while self.current_token and self.current_token.token_type in ["<",
			">",
			"<=",
			">=",
			"==",
			"!=",
		]:
			op_node = structures.Node(self.current_token.value)
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
			root = structures.Node(self.current_token.value, line_no=self.current_token.line_no, val=self.current_token.value, type=self.current_token.token_type, num_type= self.current_token.num_type)
			self.match(self.current_token.token_type)

		elif self.current_token and self.current_token.token_type == "id":

			root = structures.Node(self.current_token.value, 
			   line_no=self.current_token.line_no, 
			   type = self.current_token.token_type
			   ) 
			self.match(self.current_token.token_type)

		else:
			root = structures.Node("Error", line_no=self.current_token.line_no, val= self.current_token.value)
			error_token = self.current_token.value if self.current_token else None
			self.errors.append(f"Factor invalido: {error_token}")
			self.advance()
		return root

	def parse(self):
		ast = self.program()
		if self.errors:
			print("Se encontraron errores de sintaxis. La compilacion ha fallado.")
		else:
			print("La sintaxis es correcta. La compilacion ha sido exitosa.")
		return ast


class SemanticAnalyzer:

	def __init__(self, ast):
		self.loc = -1
		self.ast = ast
		self.errors = []
		self.symbol_table = {}
		self.memoria = []
	
	def analyze(self, ast):
		self.visit_node(ast)

	def visit_node(self, node):
		if node.parent is not None:
		
			if node.value == "DeclaracionInt":
				self.handle_int_declaration(node)
			elif node.value == "DeclaracionFloat":
				self.handle_float_declaration(node)
			elif node.value == "Asignacion":
				self.handle_assignment(node, current_node = node.children)
			#print(f": {node.value}, valor: {node.val},type:{node.type} , parent: {node.parent.value}")

		for child in node.children:
			self.visit_node(child)

	def handle_int_declaration(self, node):
		for var_node in node.children:  # Puede haber múltiples variables declaradas en la misma linea
			self.loc+=1
			variable_name = var_node.value
			if variable_name in self.symbol_table:
				self.errors.append(f"Duplicado: Variable '{variable_name}' ya declarada")
				self.symbol_table[variable_name+" Duplicado"] = {
					"type": "int...",
					"value": None,
					"loc": self.loc,
					"line_numbers":[self.symbol_table[variable_name]['line_numbers'],var_node.line_no],
				}
			else:
				# Guardar la variable en la tabla de simbolos
				self.symbol_table[variable_name] = {
					"type": "int",
					"value": None,
					"loc": self.loc,
					"line_numbers": [var_node.line_no],
				}
	

	def handle_float_declaration(self, node):
		for var_node in node.children:
			self.loc+=1
			variable_name = var_node.value
			if variable_name in self.symbol_table:
				self.errors.append(f"Duplicado: Variable '{variable_name}' ya declarada")
				self.symbol_table[variable_name+" Duplicado"] = {
					"type": "Float...Error",
					"value": None,
					"loc": self.loc,
					"line_numbers":[self.symbol_table[variable_name]['line_numbers'],var_node.line_no],
				}
			else:
				# Guardar la variable en la tabla de simbolos
				self.symbol_table[variable_name] = {
					"type": "float",
					"value": None,
					"loc": self.loc,
					"line_numbers": [var_node.line_no],
				}

	def handle_assignment(self, node, current_node):
	
		variable_name = node.children[0].value
		
		if variable_name not in self.symbol_table:
			self.errors.append(
				f"Error en la línea {node.line_no}: Variable '{variable_name}' no declarada."
			)
		else:
			
			
			node.children[0].type = self.symbol_table[variable_name]['type']
			if node.children[0].type != node.children[0].type:
					self.errors.append(
						f"Error en la línea {node.line_no}: Tipos de datos incompatibles en la operación de igualdad."
			   			 )
			#si el hijo 1 tiene mas hijos recurrir a hacer las expreciones de igual manera  recurrir y asignarle el valor del hijo 1 al 0 y de esta manera hacerlo recursivo

			self.evaluate_expression(node)

			self.symbol_table[variable_name]["value"] = node.children[0].val


	def evaluate_expression(self, node):
		if node.type == 'id':
			if node.val is None  :
				node.val = self.symbol_table[node.value]["value"]
				return
		if node.children[0].type == 'id':
			if node.children[0].val is None:
				node.children[0].val = self.symbol_table[node.children[0].value]["value"]
		
		if node.children[1].type == 'id':
			if node.children[1].val is None:
				node.children[1].val = self.symbol_table[node.children[1].value]["value"]
		operators = {
			'*',
			'/',
			'+',
			'-',
			'^',
			'%',
		}
		# if len(node.children) == 0:
		# 	self.errors.append(f"Error en la línea {node.line_no}: asignacion incorrecta")
		# 	return
			
		if len (node.children[0].children) != 0:
			self.evaluate_expression(node.children[0])

		if len (node.children[1].children) != 0:
			self.evaluate_expression(node.children[1])
			
		#validar si se declaro en self.memory y asignar el type en num_type 
		if node.children[0].type == 'id':
				node.children[0].num_type = self.symbol_table[node.children[0].value]['type']
		if node.children[1].type == 'id' :	
				node.children[1].num_type = self.symbol_table[node.children[1].value]['type']
		
		if node.value in operators:
			self.calculate(node.children, node.value, node)
		else: # lo mas seguro es que sea un igual  por lo tanto solo se pasa el valor 
			node.val = node.children[1].val
			node.children[0].val= node.val
			



	

	def calculate(self, children, operation, node):
		#conver to str to num 
		if children[0].num_type == 'float':
			children[0].val = float(children[0].val)
		elif children[0].num_type == 'int':
			children[0].val = int(children[0].val)
		if children[1].num_type == 'float':
			children[1].val = float(children[1].val)
		elif children[1].num_type == 'int':
			children[1].val = int(children[1].val)

		if operation == '*':
			node.val = children[0].val * children[1].val
		elif operation == '/':
			if children[1].val == 0:
				self.errors.append("Error en la línea: Division por cero")
				return 
			node.val = children[0].val / children[1].val
		elif operation == '+':
			node.val = children[0].val + children[1].val
		elif operation == '-':
			node.val = children[0].val - children[1].val
		elif operation == '^':
			node.val = children[0].val ** children[1].val
		elif operation == '%':
			if children[1].val == 0:
				self.errors.append("Error en la línea: Division por cero")
				return None
			node.val = children[0].val % children[1].val


		
				



class SemanticProcessor:
	def __init__(self):
		# Codigo principal
		self.memoria = []
		with open("src/assets/lexico.txt", "r") as file:
				lines = file.readlines()

		# Crear la lista de objetos Token
		token_list = []

		for line in lines:
			num_type = None
			line = line.strip()
			if line:
				token_parts = line.split("--*")
				if token_parts[1].strip() == "identificador":
					token_type = "id"
					value = token_parts[0].strip()

				elif token_parts[1].strip() == "flotante":
					token_type = "num"
					num_type =  "float"
					value = token_parts[0].strip()
				elif token_parts[1].strip() == "entero":
					token_type = "num"
					num_type =  "int"
					value = token_parts[0].strip()
				else:
					token_type = token_parts[0].strip()
					value = token_parts[0].strip()
					
				line_no = token_parts[2].strip()

				token = structures.Token(token_type, value, line_no, num_type=num_type)
				token_list.append(token)

	
		parser = Parser(token_list)
		ast = parser.parse()
		#mostar en un archivo el ast 

		# Crear instancia del SemanticAnalyzer y analizar el arbol sintactico
		semantic_analyzer = SemanticAnalyzer(ast)
		semantic_analyzer.analyze(ast)
		#semantic_analyzer.evaluate_expression( parentnode = ast.children)

		# Guardar errores semanticos en un archivo
		with open("src/assets/errores_semanticos.txt", "w", encoding="utf-8") as error_file:
			for error in semantic_analyzer.errors:
				error_file.write(error + "\n")

		# Anotar el arbol sintactico
		with open("src/assets/arbol_sintactico_anotado.txt", "w", encoding="utf-8") as annotated_tree_file:
			annotated_tree_file.write("arbol Sintactico Anotado:\n")
			self.annotate_tree(ast, output=annotated_tree_file)

		# Crear un archivo de texto para la tabla de sambolos
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
		"""
		Detects the operation of a node and performs the calculation recursively.

		Args:
			node (object): The node object representing the operation.

		Returns:
			None: If an error occurs (e.g., division by zero).
		""" 
		operators = {
			'*': lambda x, y: x * y,
			'/': lambda x, y: x / y,
			'+': lambda x, y: x + y,
			'-': lambda x, y: x - y,
			'^': lambda x, y: x ** y,
			'%': lambda x, y: x % y,
		}

		if node.value in operators:
			# Recursively evaluate child nodes
			for child in node.children:
				result = self.detectar_operacion(child)
				 
				if child.val is None:
					return None

			# Perform the operation on the results of child nodes
			node.val = self._calculate(node.children, operators[node.value])

			# Update parent and sibling nodes if necessary
			if node.parent:
				node.parent.val = self._calculate(node.parent.children, operators[node.parent.value])
			for sibling in node.siblings:
				sibling.val = self._calculate(sibling.children, operators[sibling.value])

		return node.val

	def _calculate(self, children, operation):
		"""
		Performs the provided operation on the values of child nodes.

		Args:
			children (list): List of child nodes.
			operation (function): The operation to perform (e.g., addition, multiplication).

		Returns:
			float or int: The result of the operation.
			None: If an error occurs (e.g., division by zero, value conversion error).
		"""

		try:
			result = operation(*[child.val for child in children])
			return result
		except (ValueError, ZeroDivisionError) as e:
			print(f"Error: {e}")
			return None


	def _convert_to_number(self, value):
		"""
		Converts the value to a float or int, handling potential errors.

		Args:
			value (str): The value to convert.

		Returns:
			float or int: The converted value.
		"""

		try:
			if value is not None and value.isdigit():
				return float(value)
		except ValueError:
			try:
				return int(value)
			except ValueError:
				# If neither float nor int conversion succeeds, handle the error as needed
				print(f"Error: Invalid numeric value '{value}'")
				return None
		# Funcion para anotar el arbol sintactico
	def annotate_tree(self, node, level=0, output=None):
		indent = " | " * level

				
		if node.parent is not None:
			if node.parent.value == 'Asignacion' :
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
				value_str = f"{node.value} ( Linea {node.line_no})"
				if hasattr(node, "type"):
					
					value_str += f" [Tipo: {node.type}]"

				if hasattr(node, "val"):

					self.update_Node_memoria(node)
					if node.val!=None:
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
					
					if node.value == 'Asignacion':
						node.val = node.children[1].val

						if  node.val == None:
							
							self.detectar_operacion(node.children[1])

						value_str += f" [Valor: {node.val}]"
					else:
						value_str
				output.write(f"{indent}{value_str}\n")
		
						
		for child in node.children:
			self.annotate_tree(child, level + 1, output)

	# Funcion para imprimir el arbol anotado y guardarlo en un archivo
	def print_ast(self, node, level=0, is_last_child=False, output=None):
		indent = " | " * level
		if output:
			value_str = f"{node.value} (Lanea {node.line_no})"
			if hasattr(node, "type"):
				value_str += f" [Tipo: {node.type}]"
			if hasattr(node, "val"):
				value_str += f" [Valor: {node.val}]"
			output.write(f"{indent}{value_str}\n")
		for i, child in node.children:
			is_last = i == len(node.children) - 1
			self.print_ast(child, level + 1, is_last, output)

	# Funcion para crear un archivo de texto para la tabla de sambolos
	def create_symbol_table_text(self, symbol_table, filename):
		stock_data = []
		try:
			with open(filename, "w") as file:
				headers = ["Nombre Variable","Tipo","Valor","Registro (loc)","Numeros de lines" ]
				
				for variable, data in symbol_table.items():
					line_no_numbers = ", ".join(map(str, data['line_numbers']))
					stock_data.append([variable, data['type'], data['value'], data['loc'],line_no_numbers])
					#file.write(f"		{variable} 			| 	{data['type']}	 |  {data['value']}		  |{data['loc']}		|{line_no_numbers}\n")
				table = tabulate(stock_data, headers, tablefmt="grid")
				file.write(table)
		except Exception as e:
			print(f"Error al crear el archivo de tabla de simbolos: {e}")
	



if __name__ == "__main__":
	SemanticProcessor()