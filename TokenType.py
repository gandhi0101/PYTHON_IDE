from enum import Enum

class TokenType(Enum):
    # Tokens de control
    ENDFILE = "ENDFILE"  # cierre de archivo
    ERROR = "ERROR"  # error - no hay tokens que coincidan

    # Palabras reservadas
    IF = "IF"
    ELSE = "ELSE"
    DO = "DO"
    WHILE = "WHILE"
    SWITCH = "SWITCH"
    CASE = "CASE"
    END = "END"
    REPEAT = "REPEAT"
    UNTIL = "UNTIL"
    READ = "READ"
    WRITE = "WRITE"
    INTEGER = "INTEGER"
    DOUBLE = "DOUBLE"
    MAIN = "MAIN"
    AND = "AND"
    OR = "OR"
    RETURN = "RETURN"
    CIN = "CIN"
    COUT = "COUT"

    # Tokens de múltiples caracteres
    ID = "ID"
    NumInt = "NumInt"
    NumReal = "NumReal"

    # Operadores aritméticos
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"

    # Operadores relacionales
    EQ = "EQ"  # igualdad
    NEQ = "NEQ"  # diferente
    LT = "LT"  # menor que
    LTE = "LTE"  # menor o igual que
    GT = "GT"  # mayor que
    GTE = "GTE"  # mayor o igual que

    # Símbolos especiales
    LPAREN = "LPAREN"  # paréntesis izquierdo
    RPAREN = "RPAREN"  # paréntesis derecho
    LBRACE = "LBRACE"  # llave izquierda
    RBRACE = "RBRACE"  # llave derecha
    COMMA = "COMMA"  # coma
    COLON = "COLON"  # dos puntos
    SEMICOLON = "SEMICOLON"  # punto y coma
    ASSIGN = "ASSIGN"  # asignación

    # Incrementador
    INCREMENT = "INCREMENT"
    
    # Decrementador
    DECREMENT = "DECREMENT"

    # Símbolo de comentario múltiple no cerrado
    InMultipleComment = "InMultipleComment"

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: '{self.value}'>"

