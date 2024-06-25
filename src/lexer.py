from optparse import OptionParser


class LexicalScaner:
    def __init__(self):
        print("")

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
    operadores_logicos = {"&&": "AND", "||": "OR", "!": "NOT"}
    operadores_dobles = {"++": "INCREMENTO", "--": "DECREMENTO"}
    tokens = []
    errors = []
    linea = 1
    col = 1

    def Lexico(self,ruta):
        self.file = open(ruta, "r")
        contenidodecodigo = self.file.read()
        i = 0
        while i < len(contenidodecodigo):
            # Ignorar espacios en blanco
            if contenidodecodigo[i].isspace():
                if contenidodecodigo[i] == "\n":
                    self.linea += 1
                    self.col = 1
                else:
                    self.col += 1
                i += 1
                continue
            # Identificar comentarios de una línea
            if contenidodecodigo[i : i + 2] == "//":
                i = contenidodecodigo.index("\n", i)
                continue
            # Identificar comentarios multilinea
            if contenidodecodigo[i : i + 2] == "/*":
                aux = contenidodecodigo.index("*/", i) + 2
                j = i
                while j < aux:
                    if contenidodecodigo[j] == "\n":
                        self.linea += 1
                    j += 1
                i = aux
                continue
            # Identificar palabras reservadas, identificadores y números
            if contenidodecodigo[i].isalpha():
                j = i + 1
                while j < len(contenidodecodigo) and (
                    contenidodecodigo[j].isalnum() or contenidodecodigo[j] == "_"
                ):
                    j += 1
                token = contenidodecodigo[i:j]
                if token in self.palabras_reservadas:
                    self.tokens.append(" " + token + "  --* " + self.palabras_reservadas[token] + " --* ")
                else:
                    self.tokens.append(" " + token + "  --* identificador --*")
                self.col += j - i
                i = j
                continue
            elif contenidodecodigo[i].isdigit():
                j = i + 1
                while j < len(contenidodecodigo) and contenidodecodigo[j].isdigit():
                    j += 1
                if j < len(contenidodecodigo) and contenidodecodigo[j] == ".":
                    j += 1
                    while j < len(contenidodecodigo) and contenidodecodigo[j].isdigit():
                        j += 1
                    self.tokens.append(" " + contenidodecodigo[i:j] + " --* flotante --* ")
                else:
                    self.tokens.append(" " + contenidodecodigo[i:j] + " --* entero --* ")
                self.col += j - i
                i = j
                continue
            # Identificar símbolos especiales
            if contenidodecodigo[i] in self.simbolos_especiales:
                self.tokens.append(" " + contenidodecodigo[i] + "  --* simbolo especial --*")
                i += 1
                self.col += 1
                continue
            # Identificar operadores aritméticos y relacionales
            if contenidodecodigo[i : i + 2] in self.operadores_relacionales:
                self.tokens.append(" " + contenidodecodigo[i : i + 2] + " --* operador relacional --*")
                i += 2
                self.col += 2
                continue
            elif contenidodecodigo[i] in self.operadores_relacionales:
                self.tokens.append(" " + contenidodecodigo[i] + " --* operador relacional --*")
                i += 1
                continue
            if contenidodecodigo[i : i + 2] in self.operadores_dobles:
                self.tokens.append(" " + contenidodecodigo[i : i + 2] + "--* operador aritmetico --*")
                i += 2
                self.col += 1
                continue
            elif contenidodecodigo[i] in self.operadores_aritmeticos:
                self.tokens.append(" " + contenidodecodigo[i] + "  --* operador aritmetico --*")
                i += 1
                self.col += 1
                continue
            else:
                self.errors.append(
                    "error:'"
                    + contenidodecodigo[i]
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
        f = open("src/assets/lexico.txt", "w")
        for item in self.tokens:
            print(item)
            f.write(item + "\n")
        f.close()
        # Ingresa los errores a un txt
        f = open("src/assets/errors.txt", "w")
        for error in self.errors:
            print(error)
            f.write(error + "\n")
        f.close()