from enum import Enum, auto
from typing import List, Tuple, Union

# Definición de tipos de tokens
class TokenType(Enum):
    ID = auto()
    INTEGER = auto()
    DOUBLE = auto()
    IF = auto()
    ELSE=auto()
    WHILE = auto()
    WRITE = auto()
    READ = auto()
    DO = auto()
    REPEAT = auto()
    SWITCH = auto()
    RETURN = auto()
    CIN = auto()
    COUT = auto()
    MAIN = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    COLON = auto()
    SEMICOLON = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    NUMINT = auto()
    NUMREAL = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    EQ = auto()
    NEQ = auto()
    AND = auto()
    OR = auto()
    END = auto()
    CASE = auto()
    DEFAULT = auto()
    UNTIL = auto()
    EOF = auto()

# Nodo del árbol sintáctico abstracto (AST)
class TreeNode:
    def __init__(self, node_type: str, token: TokenType = None, value: str = None):
        self.node_type = node_type
        self.token = token
        self.value = value
        self.children = []

    def __repr__(self):
        return f"{self.node_type}: {self.children}"

# Función auxiliar para tokenizar el código (se asume implementada)
def tokenize(content: str) -> List[Tuple[TokenType, str]]:
    pass

# Funciones de análisis sintáctico
def match_token(tokens: List[Tuple[TokenType, str]], expected: TokenType, current_token: List[int]) -> None:
    if current_token[0] < len(tokens) and tokens[current_token[0]][0] == expected:
        current_token[0] += 1
    else:
        raise Exception(f"Error de sintaxis: se esperaba {expected} en la posición {current_token[0]} pero se encontró {tokens[current_token[0]]}")


def parse_program(tokens: List[Tuple[TokenType, str]], current_token: List[int], errors: List[str]) -> TreeNode:
    root = TreeNode("MainRoot")
    while current_token[0] < len(tokens) and tokens[current_token[0]][0] != TokenType.EOF:
        try:
            statement_node = parse_statement(tokens, current_token)
            root.children.append(statement_node)
        except Exception as e:
            errors.append(str(e))
            # Avanza al siguiente token en caso de error para intentar continuar el análisis
            current_token[0] += 1
    return root


def parse_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    token_type = tokens[current_token[0]][0]
    print(f"Parsing statement: {token_type}")

    if token_type == TokenType.ID:
        if tokens[current_token[0] + 1][0] == TokenType.INCREMENT:
            return parse_increment_statement(tokens, current_token)
        elif tokens[current_token[0] + 1][0] == TokenType.DECREMENT:
            return parse_decrement_statement(tokens, current_token)
        else:
            return parse_assignment(tokens, current_token)
    elif token_type == TokenType.COLON:
        current_token[0] += 1
        return TreeNode("Error")
    elif token_type == TokenType.IF:
        return parse_if_statement(tokens, current_token)
    elif token_type == TokenType.WHILE:
        return parse_while_statement(tokens, current_token)
    elif token_type == TokenType.WRITE:
        return parse_write_statement(tokens, current_token)
    elif token_type == TokenType.READ:
        return parse_read_statement(tokens, current_token)
    elif token_type == TokenType.DO:
        return parse_do_while_statement(tokens, current_token)
    elif token_type == TokenType.REPEAT:
        return parse_repeat_until_statement(tokens, current_token)
    elif token_type == TokenType.SWITCH:
        return parse_switch_statement(tokens, current_token)
    elif token_type == TokenType.RETURN:
        return parse_return_statement(tokens, current_token)
    elif token_type == TokenType.CIN:
        return parse_cin_statement(tokens, current_token)
    elif token_type == TokenType.COUT:
        return parse_cout_statement(tokens, current_token)
    elif token_type == TokenType.MAIN:
        return parse_main_function(tokens, current_token)
    elif token_type == TokenType.INTEGER:
        return parse_int_variable_declaration(tokens, current_token)
    elif token_type == TokenType.DOUBLE:
        return parse_double_variable_declaration(tokens, current_token)
    elif token_type == TokenType.LBRACE:
        current_token[0] += 1
        statement_list_node = TreeNode("Statement")
        while tokens[current_token[0]][0] != TokenType.RBRACE:
            try:
                statement_node = parse_statement(tokens, current_token)
                statement_list_node.children.append(statement_node)
            except Exception as e:
                current_token[0] += 1
                raise e
        current_token[0] += 1
        return statement_list_node
    else:
        raise Exception(f"Error de sintaxis: token inesperado {tokens[current_token[0]]}")

def parse_main_function(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("MainFunction")
    match_token(tokens, TokenType.MAIN, current_token)
    match_token(tokens, TokenType.LPAREN, current_token)
    match_token(tokens, TokenType.RPAREN, current_token)
    match_token(tokens, TokenType.LBRACE, current_token)
    while tokens[current_token[0]][0] != TokenType.RBRACE:
        statement_node = parse_statement(tokens, current_token)
        node.children.append(statement_node)
    match_token(tokens, TokenType.RBRACE, current_token)
    return node

def parse_int_variable_declaration(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("IntStatement")
    match_token(tokens, TokenType.INTEGER, current_token)
    while tokens[current_token[0]][0] == TokenType.ID:
        node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
        current_token[0] += 1
        if tokens[current_token[0]][0] == TokenType.COMMA:
            current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_double_variable_declaration(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("DoubleStatement")
    match_token(tokens, TokenType.DOUBLE, current_token)
    while tokens[current_token[0]][0] == TokenType.ID:
        node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
        current_token[0] += 1
        if tokens[current_token[0]][0] == TokenType.COMMA:
            current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_if_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("IfStatement")
    match_token(tokens, TokenType.IF, current_token)
    condition_node = parse_expression(tokens, current_token)
    node.children.append(condition_node)
    match_token(tokens, TokenType.RPAREN, current_token)

    if tokens[current_token[0]][0] == TokenType.LBRACE:
        match_token(tokens, TokenType.LBRACE, current_token)
        while tokens[current_token[0]][0] != TokenType.RBRACE:
            try:
                statement_node = parse_statement(tokens, current_token)
                node.children.append(statement_node)
            except Exception as e:
                current_token[0] += 1
                raise e
        match_token(tokens, TokenType.RBRACE, current_token)
    else:
        statement_node = parse_statement(tokens, current_token)
        node.children.append(statement_node)

    return node




def parse_do_while_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("DoWhileStatement")
    match_token(tokens, TokenType.DO, current_token)
    
    # Parsear las declaraciones dentro del do { ... }
    if tokens[current_token[0]][0] == TokenType.LBRACE:
        current_token[0] += 1
        statement_list_node = TreeNode("StatementList")
        while tokens[current_token[0]][0] != TokenType.RBRACE:
            try:
                statement_node = parse_statement(tokens, current_token)
                statement_list_node.children.append(statement_node)
            except Exception as e:
                current_token[0] += 1
                raise e
        current_token[0] += 1
        node.children.append(statement_list_node)
    else:
        raise Exception(f"Error de sintaxis: se esperaba '{{' después de 'do' en la posición {current_token[0]}")
    
    # Parsear la condición de terminación con la expresión while
    match_token(tokens, TokenType.WHILE, current_token)
    condition_node = parse_expression(tokens, current_token)
    node.children.append(condition_node)
    
    # Se espera un punto y coma para finalizar la declaración do-while
    match_token(tokens, TokenType.SEMICOLON, current_token)
    
    return node

def parse_while_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("WhileStatement")
    match_token(tokens, TokenType.WHILE, current_token)
    condition_node = parse_expression(tokens, current_token)
    node.children.append(condition_node)
    statement_node = parse_statement(tokens, current_token)
    node.children.append(statement_node)
    return node

def parse_write_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("WriteStatement")
    match_token(tokens, TokenType.WRITE, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_read_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("ReadStatement")
    match_token(tokens, TokenType.READ, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_cin_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("CinStatement")
    match_token(tokens, TokenType.CIN, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_cout_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("CoutStatement")
    match_token(tokens, TokenType.COUT, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_assignment(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("AssignmentStatement")
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.EQ, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_increment_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("IncrementStatement")
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.INCREMENT, current_token)
    return node

def parse_decrement_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("DecrementStatement")
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.DECREMENT, current_token)
    return node

def parse_return_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("ReturnStatement")
    match_token(tokens, TokenType.RETURN, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_repeat_until_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("RepeatUntilStatement")
    match_token(tokens, TokenType.REPEAT, current_token)
    statement_node = parse_statement(tokens, current_token)
    node.children.append(statement_node)
    match_token(tokens, TokenType.UNTIL, current_token)
    condition_node = parse_expression(tokens, current_token)
    node.children.append(condition_node)
    match_token(tokens, TokenType.SEMICOLON, current_token)
    return node

def parse_switch_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("SwitchStatement")
    match_token(tokens, TokenType.SWITCH, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.LBRACE, current_token)
    while tokens[current_token[0]][0] != TokenType.RBRACE:
        case_node = parse_case_statement(tokens, current_token)
        node.children.append(case_node)
    match_token(tokens, TokenType.RBRACE, current_token)
    return node

def parse_case_statement(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("CaseStatement")
    match_token(tokens, TokenType.CASE, current_token)
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    match_token(tokens, TokenType.COLON, current_token)
    while tokens[current_token[0]][0] not in [TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE]:
        statement_node = parse_statement(tokens, current_token)
        node.children.append(statement_node)
    return node

def parse_expression(tokens: List[Tuple[TokenType, str]], current_token: List[int]) -> TreeNode:
    node = TreeNode("Expression")
    node.children.append(TreeNode("Factor", token=tokens[current_token[0]][0], value=tokens[current_token[0]][1]))
    current_token[0] += 1
    return node


# Ejemplo de uso:
if __name__ == "__main__":
    # Ejemplo de tokens (solo para demostración, debes implementar la función tokenize):
    tokens = [
       (TokenType.IF, "if"),
    (TokenType.LPAREN, "("),
    (TokenType.ID, "x"),
    (TokenType.LT, "<"),
    (TokenType.NUMINT, "10"),
    (TokenType.RPAREN, ")"),
    (TokenType.LBRACE, "{"),
    (TokenType.ID, "x"),
    (TokenType.PLUS, "+"),
    (TokenType.NUMINT, "5"),
    (TokenType.SEMICOLON, ";"),
    (TokenType.RBRACE, "}"),
    (TokenType.ELSE, "else"),
    (TokenType.LBRACE, "{"),
    (TokenType.ID, "x"),
    (TokenType.EQ, "="),
    (TokenType.NUMINT, "0"),
    (TokenType.SEMICOLON, ";"),
    (TokenType.RBRACE, "}"),
    (TokenType.EOF, "")
]

    errors = []
    current_token = [0]  # Lista mutable para mantener el índice del token actual
    try:
        ast = parse_program(tokens, current_token, errors)
        if errors:
            for error in errors:
                print(error)
        else:
            print("Análisis sintáctico exitoso.")
            # Aquí puedes realizar acciones adicionales con el árbol sintáctico abstracto (AST)
            print(ast)
    except Exception as e:
        print(f"Error de análisis sintáctico: {str(e)}")
