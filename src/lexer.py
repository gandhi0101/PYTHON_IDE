from optparse import OptionParser

class LexicalScaner:
	def __init__(self):
		print("")

	parser = OptionParser(version="%prog 1.0.3")
	parser.add_option(
		"-f",
		"--*file",
		action="store",
		dest="file",
		default="test.txt",
		type="string",
		help="",
	)

	# Diccionarios de tokens
	palabras_reservadas = {
		"main": "palabra reservada",
		"then": "palabra reservada",
		"if": "palabra reservada",
		"else": "palabra reservada",
		"end": "palabra reservada",
		"do": "palabra reservada",
		"while": "palabra reservada",
		"repeat": "palabra reservada",
		"until": "palabra reservada",
		"cin": "palabra reservada",
		"cout": "palabra reservada",
		"real": "palabra reservada",
		"int": "palabra reservada",
		"boolean": "palabra reservada",
		"true": "palabra reservada",
		"false": "palabra reservada",
		"float":"palabra reservada",
	}
	simbolos_especiales = {
		"(": "PAR_IZQ",
		")": "PAR_DER",
		"{": "LLAVE_IZQ",
		"}": "LLAVE_DER",
		";": "PUNTO_COMA",
		",": "COMA",
	}
	operadores_aritmeticos = {
		"+": "SUMA",
		"-": "RESTA",
		"*": "MULTIPLICACION",
		"/": "DIVISION",
		"=": "IGUALACION",
	}
	operadores_relacionales = {
		"==": "IGUALDAD",
		"!=": "DIFERENTE",
		"<>": "DIFERENTE2",
		"<": "MENOR_QUE",
		">": "MAYOR_QUE",
		"<=": "MENOR_IGUAL_QUE",
		">=": "MAYOR_IGUAL_QUE",
	}
	operadores_logicos = {"&&": "AND", 
						"||": "OR", 
						"!": "NOT"
	}
	operadores_dobles = {"++": "INCREMENTO",
						"--": "DECREMENTO"
	}
	
	linea = 1
	col = 1

	

	def Lexico(self,ruta):
		i = 0
		tokens = []
		errors = []
		with open(ruta, "r") as file:
			self.contenidodecodigo = file.read()
			file.close()
		while i < len(self.contenidodecodigo):
			# Ignorar espacios en blanco
			if self.contenidodecodigo[i].isspace():
				if self.contenidodecodigo[i] == "\n":
					self.linea += 1
					self.col = 1
				else:
					self.col += 1
				i += 1
				continue
			# Identificar comentarios de una línea
			if self.contenidodecodigo[i : i + 2] == "//":
				i = self.contenidodecodigo.index("\n", i)
				continue
			# Identificar comentarios multilinea
			if self.contenidodecodigo[i : i + 2] == "/*":
				aux = self.contenidodecodigo.index("*/", i) + 2
				j = i
				while j < aux:
					if self.contenidodecodigo[j] == "\n":
						self.linea += 1
					j += 1
				i = aux
				continue
			# Identificar palabras reservadas, identificadores y números
			if self.contenidodecodigo[i].isalpha():
				j = i + 1
				while j < len(self.contenidodecodigo) and (
					self.contenidodecodigo[j].isalnum() or self.contenidodecodigo[j] == "_"
				):
					j += 1
				token = self.contenidodecodigo[i:j]
				if token in self.palabras_reservadas:
					tokens.append(" " + token + "  --* " + self.palabras_reservadas[token] + " --* "+ str(self.linea))
				else:
					tokens.append(" " + token + "  --* identificador --*"+ str(self.linea))
				self.col += j - i
				i = j
				continue
			elif self.contenidodecodigo[i].isdigit():
				j = i + 1
				while j < len(self.contenidodecodigo) and self.contenidodecodigo[j].isdigit():
					j += 1
				if j < len(self.contenidodecodigo) and self.contenidodecodigo[j] == ".":
					j += 1
					while j < len(self.contenidodecodigo) and self.contenidodecodigo[j].isdigit():
						j += 1
					tokens.append(" " + self.contenidodecodigo[i:j] + " --* flotante --* "+ str(self.linea))
				else:
					tokens.append(" " + self.contenidodecodigo[i:j] + " --* entero --* "+ str(self.linea))
				self.col += j - i
				i = j
				continue
			# Identificar símbolos especiales
			if self.contenidodecodigo[i] in self.simbolos_especiales:
				tokens.append(" " + self.contenidodecodigo[i] + "  --* simbolo especial --*"+ str(self.linea))
				i += 1
				self.col += 1
				continue
			# Identificar operadores aritméticos y relacionales
			if self.contenidodecodigo[i : i + 2] in self.operadores_relacionales:
				tokens.append(" " + self.contenidodecodigo[i : i + 2] + " --* operador relacional --*"+ str(self.linea))
				i += 2
				self.col += 2
				continue
			elif self.contenidodecodigo[i] in self.operadores_relacionales:
				tokens.append(" " + self.contenidodecodigo[i] + " --* operador relacional --*"+ str(self.linea))
				i += 1
				continue
			if self.contenidodecodigo[i : i + 2] in self.operadores_logicos:
				tokens.append(" " + self.contenidodecodigo[i : i + 2] + " --* operador logico --*"+ str(self.linea))
				i += 2
				self.col += 2
				continue
			elif self.contenidodecodigo[i] in self.operadores_logicos:
				tokens.append(" " + self.contenidodecodigo[i] + " --* operador logico --*"+ str(self.linea))
				i += 1
				continue
			if self.contenidodecodigo[i : i + 2] in self.operadores_dobles:
				tokens.append(" " + self.contenidodecodigo[i : i + 2] + "--* operador aritmetico --*"+ str(self.linea))
				i += 2
				self.col += 1
				continue
			elif self.contenidodecodigo[i] in self.operadores_aritmeticos:
				tokens.append(" " + self.contenidodecodigo[i] + "  --* operador aritmetico --*"+ str(self.linea))
				i += 1
				self.col += 1
				continue
			else:
				errors.append(
					"error:'"
					+ self.contenidodecodigo[i]
					+ "'(linea:"
					+ str(self.linea)
					+ ", columna: "
					+ str(self.col)
					+ ")"
				)
				i += 1
				self.col += 1
				continue
		
		# Ingresa lo tokens a txt
		with open("src/assets/lexico.txt", "w") as f:
			for item in tokens:
				print(item)
				f.write(item + "\n")
			f.close()
		# Ingresa los errores a un txt
		with open("src/assets/errors.txt", "w") as f:
			for error in errors:
				print(error)
				f.write(error + "\n")
			f.close()

