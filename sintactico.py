from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
import json
import threading
from TokenType import TokenType
from TreeNode import TreeNode
from NodeType import NodeType
from ParseDeclaration import ParseDeclaration

class Syntaxs:
    
    parseDeclaration = ParseDeclaration()
    def __init__(self):
        # Ejemplo de lista de tokens predefinidos (este sería el output del tokenizador en un caso real)
        tokens = [
            (TokenType.MAIN, "main", 1, 1),
            (TokenType.LPAREN, "(", 1, 5),
            (TokenType.RPAREN, ")", 1, 6),
            (TokenType.LBRACE, "{", 1, 7),

                (TokenType.INTEGER, "int", 2, 1),
                (TokenType.ID, "x", 2, 5),
                (TokenType.SEMICOLON, ";", 2, 6),
                
                (TokenType.ID, "x", 3, 5),
                (TokenType.ASSIGN, "=", 3, 7),
                (TokenType.INTEGER, "0", 3, 9),
                (TokenType.SEMICOLON, ";", 3, 11),

                (TokenType.IF, "if", 4, 1),
                (TokenType.LPAREN, "(", 4, 4),
                (TokenType.ID, "x", 4, 5),
                (TokenType.EQ, "==", 4, 7),
                (TokenType.INTEGER, "0", 4, 10),
                (TokenType.RPAREN, ")", 4, 11),
                (TokenType.LBRACE, "{", 4, 13),
                    (TokenType.ID, "x", 5, 5),
                    (TokenType.ASSIGN, "=", 5, 7),
                    (TokenType.INTEGER, "10", 5, 9),
                    (TokenType.SEMICOLON, ";", 5, 11),
                (TokenType.RBRACE, "}", 6, 1),
            (TokenType.RBRACE, "}", 7, 1),
            (TokenType.ENDFILE, "", 7, 2),
        ]

        # Posición actual del token
        current_token = [0]
        # Lista para almacenar errores
        errors = []

        # Verificar tokens antes de comenzar el análisis sintáctico
        #print("Tokens antes del análisis sintáctico:")
        #print(tokens)

        # Llamar al analizador sintáctico con los tokens predefinidos
        syntax_tree  = self.parse_program(tokens, current_token, errors)

        # Verificar si se encontraron errores
        if errors:
            print("\nErrores de sintaxis encontrados: \t\t")
            for error in errors:
                print("\t\t"+str(error))
            print("\n")
       
        # Convertir el árbol sintáctico a un diccionario para facilitar la visualización
        tree_dict = self.tree_node_to_dict(syntax_tree)
        # print(json.dumps(tree_dict, indent=4))
        print("\n\n\tArbol")
        self.imprimir_arbol(tree_dict)


    
    def imprimir_arbol(self, nodo, nivel=0, prefijo=""):
        # Imprime el nodo actual con su nivel
        print("    " * nivel + prefijo + nodo["node_type"])
        
        # Recorre los hijos del nodo
        for hijo in nodo.get("children", []):
            nuevo_prefijo = "└──"
            self.imprimir_arbol(hijo, nivel + 1, nuevo_prefijo)



    # Serialización y deserialización con json
    def tree_node_to_dict(self ,tree_node: TreeNode) -> dict:
        return {
            "node_type": tree_node.node_type.value,
            "token_type": tree_node.token_type.value if tree_node.token_type else None,
            "value": tree_node.value,
            "children": [self.tree_node_to_dict(child) for child in tree_node.children]
        }

    def tree_node_from_dict(self,data: dict) -> TreeNode:
        node_type = NodeType(data["node_type"])
        token_type = TokenType(data["token_type"]) if data["token_type"] else None
        value = data["value"]
        children = [self.tree_node_from_dict(child) for child in data["children"]]
        return TreeNode(node_type=node_type, token_type=token_type, value=value, children=children)

    # Función para obtener el siguiente carácter no en blanco de la línea actual
    def get_next_char(self,line: str, linepos: list, bufsize: int) -> str:
        if linepos[0] >= bufsize:
            return '\0'  # Devuelve un carácter nulo al final de la línea
        else:
            c = line[linepos[0]] if linepos[0] < len(line) else '\0'  # Devuelve un carácter nulo si el índice está fuera de rango
            linepos[0] += 1
            return c

    # Función para retroceder un carácter en la línea actual
    def unget_next_char(self,linepos: list):
        if linepos[0] > 0:
            linepos[0] -= 1

    # Función para buscar palabras reservadas y devolver su TokenType correspondiente
    def reserved_lookup(self, s: str) -> TokenType:
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



    # Función para parsear el programa
    def parse_program(self,tokens: List[Tuple[TokenType, str, int, int]], current_token: List[int], errors: List[str]) -> Union[TreeNode, str]:
        root = TreeNode.new(NodeType.MainRoot)
        while current_token[0] < len(tokens) and tokens[current_token[0]][0] != TokenType.ENDFILE:
            print(tokens[current_token[0]])
            result = self.parseDeclaration.parse_statement( tokens,  current_token)
            if isinstance(result, TreeNode):
                root.children.append(result)
            else:
                errors.append(result)
                error_token = tokens[current_token[0]][0] if current_token[0] < len(tokens) else "EOF"
                errors.append(f"Error sintáctico: se esperaba {result} en la posición {error_token}")
                current_token[0] += 1

        return root

    # Función para parsear una declaración


    

   


    
sintaxis = Syntaxs() 