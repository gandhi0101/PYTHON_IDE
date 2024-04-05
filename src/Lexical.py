import sys
from enum import Enum, auto

class LexicalScanner:
    def __init__(self, python_ide_instance):
        
        self.source = None
        self.lineBuf = ""
        self.linepos = 0
        self.bufsize = 0
        self.EOF_flag = False
        self.lineno = 0
        self.python_ide = python_ide_instance
        self.text_lexicalOutput = python_ide_instance.text_lexicalOutput
        self.text_lexicalErrors = python_ide_instance.text_lexicalErrors
        self.source_file = python_ide_instance.current_file

    # Definición de tipos de tokens
    class TokenType(Enum):
        # Tokens de control
        ENDFILE = auto()
        ERROR = auto()

        # Palabras reservadas
        IF = auto()
        ELSE = auto()
        DO = auto()
        WHILE = auto()
        SWITCH = auto()
        CASE = auto()
        END = auto()
        REPEAT = auto()
        UNTIL = auto()
        READ = auto()
        WRITE = auto()
        INTEGER = auto()
        DOUBLE = auto()
        MAIN = auto()
        AND = auto()
        OR = auto()
        RETURN = auto()
        CIN = auto()  # Nueva palabra reservada cin
        COUT = auto()  # Nueva palabra reservada cout

        # Tokens de múltiples caracteres
        ID = auto()
        NUM_INT = auto()
        NUM_REAL = auto()

        # Operadores aritméticos
        PLUS = auto()
        MINUS = auto()
        TIMES = auto()
        DIVIDE = auto()
        MODULO = auto()
        POWER = auto()
        INCREMENT_OP = auto()  # Nuevo operador ++
        DECREMENT_OP = auto()  # Nuevo operador --

        # Operadores relacionales
        EQ = auto()   # igualdad
        NEQ = auto()  # diferente
        LT = auto()   # menor que
        LTE = auto()  # menor o igual que
        GT = auto()   # mayor que
        GTE = auto()  # mayor o igual que
        EQSAME = auto()  # igualdad estricta (==)

        # Operadores lógicos
        AND_LOGICAL = auto()  # &&
        OR_LOGICAL = auto()   # ||

        # Símbolos especiales
        LPAREN = auto()  # paréntesis izquierdo
        RPAREN = auto()  # paréntesis derecho
        LBRACE = auto()  # llave izquierda
        RBRACE = auto()  # llave derecha
        COMMA = auto()   # coma
        SEMICOLON = auto()  # punto y coma
        ASSIGN = auto()  # asignación

        # Símbolo de comentario múltiple no cerrado
        INMULTIPLECOMMENT = auto()

    # Tabla de búsqueda de palabras reservadas
    reservedWords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "do": TokenType.DO,
        "while": TokenType.WHILE,
        "switch": TokenType.SWITCH,
        "case": TokenType.CASE,
        "end": TokenType.END,
        "repeat": TokenType.REPEAT,
        "until": TokenType.UNTIL,
        "read": TokenType.READ,
        "write": TokenType.WRITE,
        "int": TokenType.INTEGER,
        "double": TokenType.DOUBLE,
        "main": TokenType.MAIN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "return": TokenType.RETURN,
        "cin": TokenType.CIN,  # Nueva palabra reservada cin
        "cout": TokenType.COUT,  # Nueva palabra reservada cout
    }

    # Tamaño máximo de un token
    MAXTOKENLEN = 256

    # Estados en el DFA del escáner
    class StateType(Enum):
        START = auto()
        INASSIGN = auto()
        INCOMMENT = auto()
        INNUM = auto()
        INREAL = auto()
        INID = auto()
        DONE = auto()
        INMULTICOMMENT = auto()

    def getNextChar(self):
        if not (self.linepos < self.bufsize):
            self.lineBuf = self.source.readline()
            if self.lineBuf:
                self.lineno += 1
                self.bufsize = len(self.lineBuf)
                self.linepos = 0
                return self.lineBuf[self.linepos - 1] if self.bufsize > 0 else ""
            else:
                self.EOF_flag = True
                return ""
        else:
            self.linepos += 1
            return self.lineBuf[self.linepos - 1] if self.bufsize > 0 else ""

    def ungetNextChar(self):
        if not self.EOF_flag:
            self.linepos -= 1

    def reservedLookup(self, s):
        return self.reservedWords.get(s, self.TokenType.ID)

    def getToken(self):
        tokenString = ""
        tokenStringIndex = 0
        currentToken = None
        state = self.StateType.START
        save = False
        column_number = 0

        while state != self.StateType.DONE:
            column_number = self.linepos + 1
            c = self.getNextChar()
            save = True
            if state == self.StateType.START:
                if c.isdigit():
                    state = self.StateType.INNUM
                elif c.isalpha():
                    state = self.StateType.INID
                elif c in [' ', '\t', '\n']:
                    save = False
                elif c == '/':
                    next_char = self.getNextChar()
                    if next_char == '/':
                        save = False
                        state = self.StateType.INCOMMENT
                    elif next_char == '*':
                        save = False
                        state = self.StateType.INMULTICOMMENT
                        currentToken = self.TokenType.INMULTIPLECOMMENT
                    else:
                        self.ungetNextChar()  # Retornamos el caracter leído
                        state = self.StateType.DONE
                        currentToken = self.TokenType.DIVIDE
                else:
                    state = self.StateType.DONE
                    if c == "":
                        save = False
                        currentToken = self.TokenType.ENDFILE
                    elif c == '=':
                        next_char = self.getNextChar()
                        if next_char == '=':
                            currentToken = self.TokenType.EQSAME
                            tokenString += next_char
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            currentToken = self.TokenType.EQ
                    elif c == '<':
                        next_char = self.getNextChar()
                        if next_char == '=':
                            tokenString += next_char
                            currentToken = self.TokenType.LTE
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            currentToken = self.TokenType.LT
                    elif c == '>':
                        next_char = self.getNextChar()
                        if next_char == '=':
                            tokenString += next_char
                            currentToken = self.TokenType.GTE
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            currentToken = self.TokenType.GT
                    elif c == '+':
                        next_char = self.getNextChar()
                        if next_char == '+':
                            currentToken = self.TokenType.INCREMENT_OP
                            tokenString += next_char
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            currentToken = self.TokenType.PLUS
                    elif c == '-':
                        next_char = self.getNextChar()
                        if next_char == '-':
                            currentToken = self.TokenType.DECREMENT_OP
                            tokenString += next_char
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            currentToken = self.TokenType.MINUS
                    elif c == '*':
                        next_char = self.getNextChar()
                        if next_char == '/':
                            self.text_lexicalErrors.append("Lexical error: */ Comment close without */ at line:", self.lineno)
                            state = self.StateType.DONE
                            currentToken = self.TokenType.ERROR
                        else:
                            self.ungetNextChar()
                            currentToken = self.TokenType.TIMES
                    elif c == '/':
                        currentToken = self.TokenType.DIVIDE
                    elif c == '%':
                        currentToken = self.TokenType.MODULO
                    elif c == '^':
                        currentToken = self.TokenType.POWER
                    elif c == '(':
                        currentToken = self.TokenType.LPAREN
                    elif c == ')':
                        currentToken = self.TokenType.RPAREN
                    elif c == '{':
                        currentToken = self.TokenType.LBRACE
                    elif c == '}':
                        currentToken = self.TokenType.RBRACE
                    elif c == ',':
                        currentToken = self.TokenType.COMMA
                    elif c == ';':
                        currentToken = self.TokenType.SEMICOLON
                    elif c == ':':
                        currentToken = self.TokenType.ASSIGN
                    elif c == '&':
                        next_char = self.getNextChar()
                        if next_char == '&':
                            currentToken = self.TokenType.AND_LOGICAL
                            tokenString += next_char
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            self.text_lexicalErrors.append(f"Lexical error: Expected '&&' at line {self.lineno} and column {column_number}\n", file=sys.stderr)
                            currentToken = self.TokenType.ERROR
                    elif c == '|':
                        next_char = self.getNextChar()
                        if next_char == '|':
                            currentToken = self.TokenType.OR_LOGICAL
                            tokenString += next_char
                        else:
                            self.ungetNextChar()  # Retornamos el caracter leído
                            self.text_lexicalErrors.append(f"Lexical error: Expected '||' at line {self.lineno} and column {column_number}\n", file=sys.stderr)
                            currentToken = self.TokenType.ERROR
                    else:
                        currentToken = self.TokenType.ERROR
            elif state == self.StateType.INCOMMENT:
                save = False
                if c == '\n' or c == "":
                    state = self.StateType.START
            elif state == self.StateType.INMULTICOMMENT:
                save = False
                if c == '*':
                    next_char = self.getNextChar()
                    if next_char == '/':
                        state = self.StateType.START
                    else:
                        self.ungetNextChar()  # Retornamos el caracter leído
                elif c == "":
                    self.text_lexicalErrors.append(f"Error: '/*' Multiline comment not closed.\n", file=sys.stderr)
                    state = self.StateType.START
                else:
                    pass
            elif state == self.StateType.INNUM:
                if not c.isdigit() and c != '.':
                    self.ungetNextChar()
                    save = False
                    state = self.StateType.DONE
                    currentToken = self.TokenType.NUM_INT
                elif c == '.':
                    state = self.StateType.INREAL
            elif state == self.StateType.INREAL:
                if not c.isdigit():
                    if tokenString[-1] == '.' and not c.isdigit():
                        self.text_lexicalErrors.append(f"Lexical error: Missing digits after decimal point at line:{ self.lineno}")
                        state = self.StateType.DONE
                        currentToken = self.TokenType.ERROR
                        self.ungetNextChar()  # Retornamos el caracter leído
                    else:
                        self.ungetNextChar()
                        save = False
                        state = self.StateType.DONE
                        currentToken = self.TokenType.NUM_REAL
            elif state == self.StateType.INID:
                if not c.isalnum() and c != '_':
                    self.ungetNextChar()
                    save = False
                    state = self.StateType.DONE
                    currentToken = self.reservedLookup(tokenString)

            if save and c != '\n':
                tokenString += c

            if state == self.StateType.DONE:
                if currentToken == self.TokenType.ID:
                    currentToken = self.reservedLookup(tokenString)
                return currentToken, tokenString, self.lineno, column_number

    def lexico(self):
        with open(self.source_file, "r") as self.source:
            while True:
                token, tokenString, lineno, column = self.getToken()
                if token == self.TokenType.ERROR:
                    error_message = f"Lexical error: {tokenString} is not a valid token in line: {lineno} and column: {column}\n"
                    self.text_lexicalErrors.append(error_message)
                    ##print(f"Lexical error: {tokenString} is not a valid token in line: {lineno} and column: {column}\n", file=sys.stderr)
                elif token != self.TokenType.ENDFILE:  # Evita imprimir ENDFILE
                    token_info = f"{token.name} ({tokenString})\n"
                    self.text_lexicalOutput.append(token_info)
                    ##print(f"{token.name} ({tokenString})\n")
                if token == self.TokenType.ENDFILE:
                    break


