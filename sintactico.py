from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
import json
import threading

# Enum para representar los tipos de tokens
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


# Enum para representar los estados en el DFA del escáner
class StateType(Enum):
    Start = "Start"
    InAssign = "InAssign"
    InComment = "InComment"
    InMultiComment = "InMultiComment"
    InNum = "InNum"
    InReal = "InReal"
    InId = "InId"
    Done = "Done"
    EndFile = "EndFile"

# Enum para representar los tipos de nodos
class NodeType(Enum):
    MainRoot = "MainRoot"
    IntStatement = "IntStatement"
    DoubleStatement = "DoubleStatement"
    Statement = "Statement"
    Expression = "Expression"
    Term = "Term"
    Factor = "Factor"
    Assignment = "Assignment"
    IfStatement = "IfStatement"
    ElseStatement = "ElseStatement"
    WhileStatement = "WhileStatement"
    WriteStatement = "WriteStatement"
    ReadStatement = "ReadStatement"
    DoWhileStatement = "DoWhileStatement"
    RepeatUntilStatement = "RepeatUntilStatement"
    SwitchStatement = "SwitchStatement"
    CaseStatement = "CaseStatement"
    MainFunction = "MainFunction"
    ReturnStatement = "ReturnStatement"
    CinStatement = "CinStatement"
    CoutStatement = "CoutStatement"
    Increment = "Increment"
    Decrement = "Decrement"
    Error = "Error"

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

# Serialización y deserialización con json
def tree_node_to_dict(tree_node: TreeNode) -> dict:
    return {
        "node_type": tree_node.node_type.value,
        "token_type": tree_node.token_type.value if tree_node.token_type else None,
        "value": tree_node.value,
        "children": [tree_node_to_dict(child) for child in tree_node.children]
    }

def tree_node_from_dict(data: dict) -> TreeNode:
    node_type = NodeType(data["node_type"])
    token_type = TokenType(data["token_type"]) if data["token_type"] else None
    value = data["value"]
    children = [tree_node_from_dict(child) for child in data["children"]]
    return TreeNode(node_type=node_type, token_type=token_type, value=value, children=children)


# Inicializar el contenedor de errores con un lock
errors_lock = threading.Lock()
errors = []

def log_error(error: str):
    with errors_lock:
        if error not in errors:
            errors.append(error)

# Función para obtener el siguiente carácter no en blanco de la línea actual
def get_next_char(line: str, linepos: list, bufsize: int) -> str:
    if linepos[0] >= bufsize:
        return '\0'  # Devuelve un carácter nulo al final de la línea
    else:
        c = line[linepos[0]] if linepos[0] < len(line) else '\0'  # Devuelve un carácter nulo si el índice está fuera de rango
        linepos[0] += 1
        return c

# Función para retroceder un carácter en la línea actual
def unget_next_char(linepos: list):
    if linepos[0] > 0:
        linepos[0] -= 1

# Función para buscar palabras reservadas y devolver su TokenType correspondiente
def reserved_lookup(s: str) -> TokenType:
    reserved = {
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
        "return": TokenType.RETURN,
        "/*": TokenType.InMultipleComment,
        "cin": TokenType.CIN,
        "cout": TokenType.COUT,
    }
    return reserved.get(s, TokenType.ID)

# Función para comparar el token actual con el esperado
def match_token(tokens: List[Tuple[TokenType, str, int, int]], expected: TokenType, current_token: List[int]) -> Union[None, str]:
    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == expected:
        current_token[0] += 1
        return None
    else:
        return f"Error de sintaxis: se esperaba {expected} en la posición {tokens[current_token[0]] if current_token[0] < len(tokens) else 'EOF'}"


# Función para parsear el programa
def parse_program(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int], errors: List[str]) -> Union[TreeNode, str]:
    root = TreeNode.new(NodeType.MainRoot)
    while current_token[0] < len(tokens) and tokens[current_token[0]][0] != TokenType.ENDFILE:
        result = parse_statement(tokens, current_token)
        if isinstance(result, TreeNode):
            root.children.append(result)
        else:
            errors.append(result)
            error_token = tokens[current_token[0]][0] if current_token[0] < len(tokens) else "EOF"
            errors.append(f"Error sintáctico: se esperaba {result} en la posición {error_token}")
            current_token[0] += 1

    return root

# Función para parsear una declaración
def parse_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    print(f"Current token index: {current_token[0]}")
    if current_token[0] >= len(tokens):
        return f"Error de sintaxis: token inesperado {'EOF'}"

    print(f"Current token: {tokens[current_token[0]]}")

    if tokens[current_token[0]][0] == TokenType.ID:
        if current_token[0] + 1 < len(tokens):
            if tokens[current_token[0] + 1][0] == TokenType.INCREMENT:
                return parse_increment_statement(tokens, current_token)
            elif tokens[current_token[0] + 1][0] == TokenType.DECREMENT:
                return parse_decrement_statement(tokens, current_token)

    if tokens[current_token[0]][0] == TokenType.COLON:
        current_token[0] += 1
        return "Error de sintaxis: token fuera de un case ':'"

    # Manejo de otros tipos de tokens directamente
    if tokens[current_token[0]][0] == TokenType.IF:
        return parse_if_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.WHILE:
        return parse_while_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.WRITE:
        return parse_write_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.READ:
        return parse_read_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.DO:
        return parse_do_while_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.REPEAT:
        return parse_repeat_until_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.SWITCH:
        return parse_switch_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.RETURN:
        return parse_return_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.CIN:
        return parse_cin_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.COUT:
        return parse_cout_statement(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.MAIN:
        return parse_main_function(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.INTEGER:
        return parse_int_variable_declaration(tokens, current_token)
    elif tokens[current_token[0]][0] == TokenType.DOUBLE:
        return parse_double_variable_declaration(tokens, current_token)

    # Manejo de asignación
    if tokens[current_token[0]][0] == TokenType.ID:
        assignment_node = parse_assignment(tokens, current_token)
        if isinstance(assignment_node, TreeNode):
            if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
                current_token[0] += 1
                return assignment_node
            else:
                return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"
        else:
            return assignment_node

    return f"Error de sintaxis: token inesperado {tokens[current_token[0]] if current_token[0] < len(tokens) else 'EOF'}"



# Función para parsear una declaración de variable entera
def parse_int_variable_declaration(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode.new(NodeType.IntStatement)

    # Parsear la palabra clave 'int'
    error = match_token(tokens, TokenType.INTEGER, current_token)
    if error:
        return error

    # Parsear los identificadores
    while True:
        if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.ID:
            id_value = tokens[current_token[0]][1]
            node.children.append(TreeNode(node_type=NodeType.Factor, token_type=TokenType.ID, value=id_value))
            current_token[0] += 1
            if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.COMMA:
                current_token[0] += 1  # Avanzar si hay una coma
            else:
                break  # Salir del bucle si no hay más identificadores
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {tokens[current_token[0]] if current_token[0] < len(tokens) else 'EOF'}"

    # Verificar si hay un punto y coma al final
    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
        current_token[0] += 1  # Avanzar si hay un punto y coma
        return node
    else:
        return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"


# Función para parsear una declaración de variable double
def parse_double_variable_declaration(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode.new(NodeType.DoubleStatement)

    error = match_token(tokens, TokenType.DOUBLE, current_token)
    if error:
        return error

    while True:
        if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.ID:
            id_value = tokens[current_token[0]][1]
            node.children.append(TreeNode(node_type=NodeType.Factor, token=TokenType.ID, value=id_value, children=[]))
            current_token[0] += 1
            if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.COMMA:
                current_token[0] += 1  # Avanzar si hay una coma
            else:
                break  # Salir del bucle si no hay más identificadores
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {tokens[current_token[0]] if current_token[0] < len(tokens) else 'EOF'}"

    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
        current_token[0] += 1  # Avanzar si hay un punto y coma
        return node
    else:
        return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"

# Función para parsear una declaración if
def parse_if_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.IfStatement)
    
    error = match_token(tokens, TokenType.IF, current_token)
    if error:
        return error
    
    error = match_token(tokens, TokenType.LPAREN, current_token)
    if error:
        return error
    
    condition_node = parse_expression(tokens, current_token)
    if isinstance(condition_node, str):
        return condition_node
    node.children.append(condition_node)
    
    error = match_token(tokens, TokenType.RPAREN, current_token)
    if error:
        return error
    
    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        return error

    while current_token[0] < len(tokens) and tokens[current_token[0]][0] != TokenType.RBRACE:
        statement_node = parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            return statement_node
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        return error

    return node


# Función para parsear una declaración else
def parse_else_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.ElseStatement)
    
    error = match_token(tokens, TokenType.ELSE, current_token)
    if error:
        return error
    
    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)

    statement_node = parse_statement(tokens, current_token)
    if isinstance(statement_node, TreeNode):
        node.children.append(statement_node)
    else:
        log_error(statement_node)

    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración do-while
def parse_do_while_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.DoWhileStatement)
    
    error = match_token(tokens, TokenType.DO, current_token)
    if error:
        return error

    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)
    
    statement_node = parse_statement(tokens, current_token)
    if isinstance(statement_node, TreeNode):
        node.children.append(statement_node)
    else:
        log_error(statement_node)
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        log_error(error)

    error = match_token(tokens, TokenType.WHILE, current_token)
    if error:
        return error
    
    condition_node = parse_expression(tokens, current_token)
    if isinstance(condition_node, str):
        return condition_node
    
    node.children.append(condition_node)

    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
        current_token[0] += 1
    else:
        return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"
    
    return node

# Función para parsear una declaración while
def parse_while_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.WhileStatement)
    
    error = match_token(tokens, TokenType.WHILE, current_token)
    if error:
        return error
    
    condition_node = parse_expression(tokens, current_token)
    if isinstance(condition_node, str):
        return condition_node
    
    node.children.append(condition_node)

    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)
    
    statement_node = parse_statement(tokens, current_token)
    if isinstance(statement_node, TreeNode):
        node.children.append(statement_node)
    else:
        log_error(statement_node)
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración repeat-until
def parse_repeat_until_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.RepeatUntilStatement)
    
    error = match_token(tokens, TokenType.REPEAT, current_token)
    if error:
        return error
    
    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)
    
    statement_node = parse_statement(tokens, current_token)
    if isinstance(statement_node, TreeNode):
        node.children.append(statement_node)
    else:
        log_error(statement_node)
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        log_error(error)

    error = match_token(tokens, TokenType.UNTIL, current_token)
    if error:
        return error
    
    condition_node = parse_expression(tokens, current_token)
    if isinstance(condition_node, str):
        return condition_node
    
    node.children.append(condition_node)

    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
        current_token[0] += 1
    else:
        return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"
    
    return node

# Función para parsear una declaración switch
def parse_switch_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.SwitchStatement)
    
    error = match_token(tokens, TokenType.SWITCH, current_token)
    if error:
        return error
    
    expression_node = parse_expression(tokens, current_token)
    if isinstance(expression_node, str):
        return expression_node
    
    node.children.append(expression_node)

    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)
    
    while current_token[0] < len(tokens):
        token_type, _, _, _ = tokens[current_token[0]]
        if token_type == TokenType.CASE:
            case_node = parse_case_statement(tokens, current_token)
            if isinstance(case_node, str):
                return case_node
            node.children.append(case_node)
        elif token_type == TokenType.END:
            current_token[0] += 1
            break
        else:
            return f"Error de sintaxis: token inesperado {tokens[current_token[0]]}"
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración case dentro de un switch
def parse_case_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.CaseStatement)
    
    error = match_token(tokens, TokenType.CASE, current_token)
    if error:
        return error
    
    value_node = parse_expression(tokens, current_token)
    if isinstance(value_node, str):
        return value_node
    
    node.children.append(value_node)

    error = match_token(tokens, TokenType.COLON, current_token)
    if error:
        log_error(error)
    
    while current_token[0] < len(tokens):
        token_type, _, _, _ = tokens[current_token[0]]
        if token_type == TokenType.END or token_type == TokenType.CASE:
            break
        else:
            statement_node = parse_statement(tokens, current_token)
            if isinstance(statement_node, TreeNode):
                node.children.append(statement_node)
            else:
                log_error(statement_node)
    
    return node

# Función para parsear la función principal (main)
def parse_main_function(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.MainFunction)
    
    error = match_token(tokens, TokenType.MAIN, current_token)
    if error:
        return error
    
    error = match_token(tokens, TokenType.LPAREN, current_token)
    if error:
        log_error(error)
    
    error = match_token(tokens, TokenType.RPAREN, current_token)
    if error:
        log_error(error)
    
    error = match_token(tokens, TokenType.LBRACE, current_token)
    if error:
        log_error(error)
    
    statement_node = parse_statement(tokens, current_token)
    if isinstance(statement_node, TreeNode):
        node.children.append(statement_node)
    else:
        log_error(statement_node)
    
    error = match_token(tokens, TokenType.RBRACE, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración de escritura (write)
def parse_write_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.WriteStatement)
    
    error = match_token(tokens, TokenType.WRITE, current_token)
    if error:
        return error
    
    if current_token[0] < len(tokens):
        token_type, id, _, _ = tokens[current_token[0]]
        if token_type == TokenType.ID:
            node.children.append(TreeNode(
                node_type=NodeType.Factor,
                token_type=TokenType.ID,
                value=id,
            ))
            current_token[0] += 1
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {tokens[current_token[0]]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración de lectura (read)
def parse_read_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.ReadStatement)
    
    error = match_token(tokens, TokenType.READ, current_token)
    if error:
        return error
    
    if current_token[0] < len(tokens):
        token_type, id, _, _ = tokens[current_token[0]]
        if token_type == TokenType.ID:
            node.children.append(TreeNode(
                node_type=NodeType.Factor,
                token_type=TokenType.ID,
                value=id,
            ))
            current_token[0] += 1
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {tokens[current_token[0]]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node


# Función para parsear una declaración de retorno (return)
def parse_return_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.ReturnStatement)
    
    error = match_token(tokens, TokenType.RETURN, current_token)
    if error:
        return error
    
    expression_node = parse_expression(tokens, current_token)
    if isinstance(expression_node, str):
        return expression_node
    
    node.children.append(expression_node)

    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

def parse_cin_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.CinStatement)
    
    error = match_token(tokens, TokenType.CIN, current_token)
    if error:
        return error
    
    if current_token[0] < len(tokens):
        token_type, id, _, _ = tokens[current_token[0]]
        if token_type == TokenType.ID:
            node.children.append(TreeNode(
                node_type=NodeType.Factor,
                token_type=TokenType.ID,
                value=id,
            ))
            current_token[0] += 1
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {tokens[current_token[0]][2]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración de salida (cout)
def parse_cout_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.CoutStatement)
    
    # Verificar y avanzar el token actual si es TokenType.COUT
    error = match_token(tokens, TokenType.COUT, current_token)
    if error:
        return error
    
    # Parsear la expresión que sigue a TokenType.COUT
    expression_node = parse_expression(tokens, current_token)
    if isinstance(expression_node, str):
        return expression_node
    
    # Agregar el nodo de expresión como hijo del nodo cout
    node.children.append(expression_node)
    
    # Verificar y avanzar el token actual si es TokenType.SEMICOLON
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración de incremento (++variable)
def parse_increment_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.Increment)
    
    if current_token[0] < len(tokens):
        token_type, id_value, _, _ = tokens[current_token[0]]
        if token_type == TokenType.ID:
            node.children.append(TreeNode(
                node_type=NodeType.Factor,
                token_type=TokenType.ID,
                value=id_value,
                children=[]
            ))
            current_token[0] += 2  # Saltar dos tokens para avanzar después del ID y el INCREMENT
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

# Función para parsear una declaración de decremento (--variable)
def parse_decrement_statement(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node = TreeNode(NodeType.Decrement)
    
    if current_token[0] < len(tokens):
        token_type, id_value, _, _ = tokens[current_token[0]]
        if token_type == TokenType.ID:
            node.children.append(TreeNode(
                node_type=NodeType.Factor,
                token_type=TokenType.ID,
                value=id_value,
                children=[]
            ))
            current_token[0] += 2  # Saltar dos tokens para avanzar después del ID y el DECREMENT
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    
    error = match_token(tokens, TokenType.SEMICOLON, current_token)
    if error:
        return error
    
    return node

# Función para parsear una expresión
def parse_expression(tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    node, error = parse_term(tokens, current_token)
    if error:
        return error

    while current_token[0] < len(tokens):
        token, value, _, _ = tokens[current_token[0]]
        if token in [TokenType.PLUS, TokenType.MINUS, TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ, TokenType.AND, TokenType.OR]:
            current_token[0] += 1

            term_node, term_error = parse_term(tokens, current_token)
            if term_error:
                return term_error

            expression_node = TreeNode(NodeType.Expression)
            expression_node.children.append(node)
            expression_node.children.append(TreeNode(
                node_type=NodeType.Expression,
                token=token,
                value=value,
                children=[]
            ))
            expression_node.children.append(term_node)

            node = expression_node
        else:
            break

    return node


# Función para parsear un término
def parse_term(tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[Tuple[TreeNode, str], TreeNode]:
    node, error = parse_factor(tokens, current_token)
    if error:
        return None, error
    
    while current_token[0] < len(tokens):
        token, value, _, _ = tokens[current_token[0]]
        if token in ['TIMES', 'DIVIDE', 'MODULO', 'POWER']:
            current_token[0] += 1
            
            factor_node, factor_error = parse_factor(tokens, current_token)
            if factor_error:
                return None, factor_error
            
            term_node = TreeNode(node_type='Term')
            term_node.children.append(node)
            term_node.children.append(TreeNode(
                node_type='Factor',
                token=token,
                value=value,
                children=[]
            ))
            term_node.children.append(factor_node)
            
            node = term_node
        else:
            break
    
    return node, None

# Función para parsear un factor
def parse_factor(tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    if current_token[0] < len(tokens):
        token, value, _, _ = tokens[current_token[0]]
        current_token[0] += 1
        
        if token in ['NumInt', 'NumReal', 'ID']:
            node = TreeNode(node_type='Factor', token=token, value=value, children=[])
            return node, None
        elif token == 'LPAREN':
            expression_node, error = parse_expression(tokens, current_token)
            if error:
                return None, error
            
            if current_token[0] < len(tokens):
                token, _, _, _ = tokens[current_token[0]]
                if token == 'RPAREN':
                    current_token[0] += 1
                else:
                    return None, f"Error de sintaxis: se esperaba ')' en la posición {current_token[0]}"
            else:
                return None, f"Error de sintaxis: se esperaba ')' al final de la expresión"
            
            node = TreeNode(node_type='Factor', children=[expression_node])
            return node, None
        else:
            return None, f"Error de sintaxis: token inesperado {token} en la posición {current_token[0]}"
    else:
        return None, f"Error de sintaxis: se esperaba un factor matemático en la posición {current_token[0]}"

# Función para parsear una asignación
def parse_assignment(tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
    if current_token[0] < len(tokens):
        token, id, _, _ = tokens[current_token[0]]
        if token == TokenType.ID:
            current_token[0] += 1
            
            error = match_token(tokens, TokenType.ASSIGN, current_token)
            if error:
                return f"Error de sintaxis: se esperaba '=' en la posición {current_token[0]}"
            
            expression_node, error = parse_expression(tokens, current_token)
            if isinstance(expression_node, str):
                return expression_node
            
            node = TreeNode(node_type='Assignment', children=[
                TreeNode(node_type='Factor', token=TokenType.ID, value=id, children=[]),
                expression_node
            ])
            return node
        else:
            return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"
    else:
        return f"Error de sintaxis: se esperaba un identificador en la posición {current_token[0]}"


def main():
    # Ejemplo de lista de tokens predefinidos (este sería el output del tokenizador en un caso real)
    tokens = [
    #   (TokenType.MAIN, "main", 1, 1),
    #    (TokenType.LPAREN, "(", 1, 5),
    #    (TokenType.RPAREN, ")", 1, 6),
    #    (TokenType.LBRACE, "{", 1, 7),
    #    (TokenType.INTEGER, "int", 2, 1),
    #    (TokenType.ID, "x", 2, 5),
    #    (TokenType.SEMICOLON, ";", 2, 6),
        (TokenType.IF, "if", 3, 1),
        (TokenType.LPAREN, "(", 3, 4),
        (TokenType.ID, "x", 3, 5),
        (TokenType.EQ, "==", 3, 7),
        (TokenType.INTEGER, "0", 3, 10),
        (TokenType.RPAREN, ")", 3, 11),
        (TokenType.LBRACE, "{", 3, 13),
    #    (TokenType.WRITE, "write", 4, 3),
    #    (TokenType.ID, "x", 4, 9),
    #   (TokenType.SEMICOLON, ";", 4, 10),
        (TokenType.RBRACE, "}", 5, 1),
    #    (TokenType.RBRACE, "}", 6, 1),
        (TokenType.ENDFILE, "", 7, 1),
    ]

    # Posición actual del token
    current_token = [0]
    # Lista para almacenar errores
    errors = []

    # Verificar tokens antes de comenzar el análisis sintáctico
    #print("Tokens antes del análisis sintáctico:")
    #for token in tokens:
    #    print(token)

    # Llamar al analizador sintáctico con los tokens predefinidos
    syntax_tree = parse_program(tokens, current_token, errors)

    # Verificar si se encontraron errores
    if errors:
        print("Errores de sintaxis encontrados:")
        for error in errors:
            print(error)
    else:
        # Convertir el árbol sintáctico a un diccionario para facilitar la visualización
      tree_dict = tree_node_to_dict(syntax_tree)
      print(json.dumps(tree_dict, indent=4))
      print("arbol")

if __name__ == "__main__":
    main()
