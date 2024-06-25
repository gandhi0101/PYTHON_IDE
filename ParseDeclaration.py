from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
from  TokenType import TokenType
from TreeNode import TreeNode
from NodeType import NodeType
from StateType import StateType
from Analyzer import Analyzer

class ParseDeclaration:


    analyzer = Analyzer()

    def parse_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:

        print(f"Current token index: {current_token[0]}")
        if current_token[0] >= len(tokens):
            return f"Error de sintaxis: token inesperado {'EOF'}"

        print(f"Current token: {tokens[current_token[0]]}")

        if tokens[current_token[0]][0] == TokenType.ID:
            if current_token[0] + 1 < len(tokens):
                if tokens[current_token[0] + 1][0] == TokenType.INCREMENT:
                    return self.parse_increment_statement(tokens, current_token)
                elif tokens[current_token[0] + 1][0] == TokenType.DECREMENT:
                    return self.parse_decrement_statement(tokens, current_token)

        if tokens[current_token[0]][0] == TokenType.COLON:
            current_token[0] += 1
            return "Error de sintaxis: token fuera de un case ':'"

        # Manejo de otros tipos de tokens directamente
        if tokens[current_token[0]][0] == TokenType.IF:
            return self.parse_if_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.WHILE:
            return self.parse_while_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.WRITE:
            return self.parse_write_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.READ:
            return self.parse_read_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.DO:
            return self.parse_do_while_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.REPEAT:
            return self.parse_repeat_until_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.SWITCH:
            return self.parse_switch_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.RETURN:
            return self.parse_return_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.CIN:
            return self.parse_cin_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.COUT:
            return self.parse_cout_statement(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.MAIN:
            return self.parse_main_function(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.INTEGER:
            return self.parse_int_variable_declaration(tokens, current_token)
        elif tokens[current_token[0]][0] == TokenType.DOUBLE:
            return self.parse_double_variable_declaration(tokens, current_token)

        # Manejo de asignación
        if tokens[current_token[0]][0] == TokenType.ID:
            assignment_node = self.parse_assignment(tokens, current_token)
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
    def parse_int_variable_declaration(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode.new(NodeType.IntStatement)

        # Parsear la palabra clave 'int'
        error = self.analyzer.match_token(tokens, TokenType.INTEGER, current_token)
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
    def parse_double_variable_declaration(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode.new(NodeType.DoubleStatement)

        error = self.analyzer.match_token(tokens, TokenType.DOUBLE, current_token)
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
    def parse_if_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.IfStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.IF, current_token)
        if error:
            return error
        
        error = self.analyzer.match_token(tokens, TokenType.LPAREN, current_token)
        if error:
            return error
        
        condition_node = self.parse_expression(tokens, current_token)
        if isinstance(condition_node, str):
            return condition_node
        node.children.append(condition_node)
        
        error = self.analyzer.match_token(tokens, TokenType.RPAREN, current_token)
        if error:
            return error
        
        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            return error

        while current_token[0] < len(tokens) and tokens[current_token[0]][0] != TokenType.RBRACE:
            statement_node = self.parse_statement(tokens, current_token)
            if isinstance(statement_node, TreeNode):
                node.children.append(statement_node)
            else:
                return statement_node
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            return error

        return node


    # Función para parsear una declaración else
    def parse_else_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.ElseStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.ELSE, current_token)
        if error:
            return error
        
        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)

        statement_node = self.parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            self.analyzer.log_error(statement_node)

        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración do-while
    def parse_do_while_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.DoWhileStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.DO, current_token)
        if error:
            return error

        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)
        
        statement_node = self.parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            self.analyzer.log_error(statement_node)
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            self.analyzer.log_error(error)

        error = self.analyzer.match_token(tokens, TokenType.WHILE, current_token)
        if error:
            return error
        
        condition_node = self.parse_expression(tokens, current_token)
        if isinstance(condition_node, str):
            return condition_node
        
        node.children.append(condition_node)

        if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
            current_token[0] += 1
        else:
            return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"
        
        return node

    # Función para parsear una declaración while
    def parse_while_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.WhileStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.WHILE, current_token)
        if error:
            return error
        
        condition_node = self.parse_expression(tokens, current_token)
        if isinstance(condition_node, str):
            return condition_node
        
        node.children.append(condition_node)

        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)
        
        statement_node = self.parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            self.analyzer.log_error(statement_node)
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración repeat-until
    def parse_repeat_until_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.RepeatUntilStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.REPEAT, current_token)
        if error:
            return error
        
        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)
        
        statement_node = self.parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            self.analyzer.log_error(statement_node)
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            self.analyzer.log_error(error)

        error = self.analyzer.match_token(tokens, TokenType.UNTIL, current_token)
        if error:
            return error
        
        condition_node = self.parse_expression(tokens, current_token)
        if isinstance(condition_node, str):
            return condition_node
        
        node.children.append(condition_node)

        if current_token[0] < len(tokens) and tokens[current_token[0]][0] == TokenType.SEMICOLON:
            current_token[0] += 1
        else:
            return f"Error de sintaxis: se esperaba ';' en la posición {current_token[0]}"
        
        return node

    # Función para parsear una declaración switch
    def parse_switch_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.SwitchStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.SWITCH, current_token)
        if error:
            return error
        
        expression_node = self.parse_expression(tokens, current_token)
        if isinstance(expression_node, str):
            return expression_node
        
        node.children.append(expression_node)

        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)
        
        while current_token[0] < len(tokens):
            token_type, _, _, _ = tokens[current_token[0]]
            if token_type == TokenType.CASE:
                case_node = self.parse_case_statement(tokens, current_token)
                if isinstance(case_node, str):
                    return case_node
                node.children.append(case_node)
            elif token_type == TokenType.END:
                current_token[0] += 1
                break
            else:
                return f"Error de sintaxis: token inesperado {tokens[current_token[0]]}"
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración case dentro de un switch
    def parse_case_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.CaseStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.CASE, current_token)
        if error:
            return error
        
        value_node = self.parse_expression(tokens, current_token)
        if isinstance(value_node, str):
            return value_node
        
        node.children.append(value_node)

        error = self.analyzer.match_token(tokens, TokenType.COLON, current_token)
        if error:
            self.analyzer.log_error(error)
        
        while current_token[0] < len(tokens):
            token_type, _, _, _ = tokens[current_token[0]]
            if token_type == TokenType.END or token_type == TokenType.CASE:
                break
            else:
                statement_node = self.parse_statement(tokens, current_token)
                if isinstance(statement_node, TreeNode):
                    node.children.append(statement_node)
                else:
                    self.analyzer.log_error(statement_node)
        
        return node

    # Función para parsear la función principal (main)
    def parse_main_function(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.MainFunction)
        
        error = self.analyzer.match_token(tokens, TokenType.MAIN, current_token)
        if error:
            return error
        
        error = self.analyzer.match_token(tokens, TokenType.LPAREN, current_token)
        if error:
            self.analyzer.log_error(error)
        
        error = self.analyzer.match_token(tokens, TokenType.RPAREN, current_token)
        if error:
            self.analyzer.log_error(error)
        
        error = self.analyzer.match_token(tokens, TokenType.LBRACE, current_token)
        if error:
            self.analyzer.log_error(error)
        
        statement_node = self.parse_statement(tokens, current_token)
        if isinstance(statement_node, TreeNode):
            node.children.append(statement_node)
        else:
            self.analyzer.log_error(statement_node)
        
        error = self.analyzer.match_token(tokens, TokenType.RBRACE, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración de escritura (write)
    def parse_write_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.WriteStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.WRITE, current_token)
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
        
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración de lectura (read)
    def parse_read_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.ReadStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.READ, current_token)
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
        
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node


    # Función para parsear una declaración de retorno (return)
    def parse_return_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.ReturnStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.RETURN, current_token)
        if error:
            return error
        
        expression_node = self.parse_expression(tokens, current_token)
        if isinstance(expression_node, str):
            return expression_node
        
        node.children.append(expression_node)

        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    def parse_cin_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.CinStatement)
        
        error = self.analyzer.match_token(tokens, TokenType.CIN, current_token)
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
        
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración de salida (cout)
    def parse_cout_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node = TreeNode(NodeType.CoutStatement)
        
        # Verificar y avanzar el token actual si es TokenType.COUT
        error = self.analyzer.match_token(tokens, TokenType.COUT, current_token)
        if error:
            return error
        
        # Parsear la expresión que sigue a TokenType.COUT
        expression_node = self.parse_expression(tokens, current_token)
        if isinstance(expression_node, str):
            return expression_node
        
        # Agregar el nodo de expresión como hijo del nodo cout
        node.children.append(expression_node)
        
        # Verificar y avanzar el token actual si es TokenType.SEMICOLON
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración de incremento (++variable)
    def parse_increment_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
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
        
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una declaración de decremento (--variable)
    def parse_decrement_statement(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
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
        
        error = self.analyzer.match_token(tokens, TokenType.SEMICOLON, current_token)
        if error:
            return error
        
        return node

    # Función para parsear una expresión
    def parse_expression(self, tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        node, error = self.parse_term(tokens, current_token)
        if error:
            print("error: \t\t" +error)
            return error

        while current_token[0] < len(tokens):
            token, value, _, _ = tokens[current_token[0]]
            if token in [TokenType.PLUS, TokenType.MINUS, TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ, TokenType.AND, TokenType.OR]:
                current_token[0] += 1

                term_node, term_error = self.parse_term(tokens, current_token)
                if term_error:
                    print("error Term")
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
    
   

    # Función para parsear una asignación
    def parse_assignment(self, tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        if current_token[0] < len(tokens):
            token, id, _, _ = tokens[current_token[0]]
            if token == TokenType.ID:
                current_token[0] += 1
                
                error = self.analyzer.match_token(tokens, TokenType.ASSIGN, current_token)
                if error:
                    return f"Error de sintaxis: se esperaba '=' en la posición {current_token[0]}"
                
                expression_node, error, *resto= self.parse_expression(tokens, current_token)
                print(resto)
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
        
     # Función para parsear un factor
    def parse_factor(self, tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[TreeNode, str]:
        if current_token[0] < len(tokens):
            token, value, _, _ = tokens[current_token[0]]
            current_token[0] += 1
            
            if token in ['NumInt', 'NumReal', 'ID']:
                node = TreeNode(node_type='Factor', token=token, value=value, children=[])
                return node, None
            elif token == 'LPAREN':
                expression_node, error = self.parse_expression(tokens, current_token)
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


    def parse_term(self, tokens: List[Tuple[str, str, int, int]], current_token: List[int]) -> Union[Tuple[TreeNode, str], TreeNode]:
        node, error = self.parse_factor(tokens, current_token)
        if error:
            return None, error
        
        while current_token[0] < len(tokens):
            token, value, _, _ = tokens[current_token[0]]
            if token in ['TIMES', 'DIVIDE', 'MODULO', 'POWER']:
                current_token[0] += 1
                
                factor_node, factor_error = self.parse_factor(tokens, current_token)
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