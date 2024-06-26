# -*- coding: utf-8 -*-
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def add_child(self, node):
        self.children.append(node)

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
                f"Se esperaba {expected_token}, se encontro {found_token}"
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
            elif  self.current_token.value == "end" or self.current_token.token_type == "else":
                return root
            else:
                root.add_child(self.stmt())
        return root

    def do_while_stmt(self):
        root = Node("SentenciaDo")
        self.match("do")
        root.add_child(self.stmt())  # Agregar la primera expresion dentro del do-while
        while self.current_token and self.current_token.token_type != "until":
            root.add_child(self.stmt())  # Agregar mas expresiones dentro del do-while
        self.match("until")
        self.match("(")
        root.add_child(self.expr())
        self.match(")")
        self.match(";")
        return root

    def stmt(self):
        
        if self.current_token and self.current_token.token_type == "int":
            #root = Node("DeclaracionInt")
            #self.match("int")
            root = self.idListInt()
            #self.match(";")
        elif self.current_token and self.current_token.token_type == "do":
            root = self.do_while_stmt()
        elif self.current_token and self.current_token.token_type == "float":
            #root = Node("DeclaracionFloat")
            #self.match("float")
            root = self.idListFloat()
           # self.match(";")
        elif self.current_token and self.current_token.token_type == "id":
            root = Node("Asignacion")
            id_node = Node(self.current_token.value)
            self.match("id")
            root.add_child(id_node)
            if self.current_token and self.current_token.token_type in ["++", "--"]:
                op_node = None
                if(self.current_token.token_type =="++"):
                    op_node = Node("++")
                else:     op_node = Node("--")
                op_node.add_child(id_node)
                self.match(self.current_token.token_type)
                op_node.add_child(Node("1"))
                root.add_child(op_node)
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
                    operand_node = Node(self.current_token.value)
                    root.add_child(operand_node)
                    self.match(self.current_token.token_type)
            else:
                self.match("=")
                expr_node = self.expr()
                root.add_child(expr_node)
            self.match(";")
      #      root.add_child(id_node)
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
                self.errors.append(f"Sentencia invalida: {error_token}")
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
        id_node = Node(self.current_token.value)
        root.add_child(id_node)
        self.match("id")
        while self.current_token and  self.current_token.value =="+"  and  self.current_token.value !=";":
            self.match("+")
            id_node = Node(self.current_token.value)
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
            "&&",
            "||"
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
        elif self.current_token and self.current_token.token_type in ["id", "num"]:
            root = Node(self.current_token.value)
            self.match(self.current_token.token_type)
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append(f"Factor invalido: {error_token}")
            self.advance()
        
        return root
    

    def relational_expr(self):
        root = self.term()
        if self.current_token and self.current_token.token_type in [
            "<",
            ">",
            "<=",
            ">=",
            "==",
            "!=",
        ]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            root.add_child(op_node)
            if self.current_token and self.current_token.token_type in ["id", "num"]:
                operand_node = Node(self.current_token.value)
                root.add_child(operand_node)
                self.match(self.current_token.token_type)
        return root

    

    def parse(self):
        ast = self.program()

        if self.errors:
            print("Se encontraron errores de sintaxis. La compilacion ha fallado.")
        else:
            print("La sintaxis es correcta. La compilacion ha sido exitosa.")

        return ast

class Syntax:
    def __init__(self):
        print("\n\n")

    def sintaxis(self, ruta):  # "src/assets/lexico.txt"
        with open(ruta, "r") as file:
            lines = file.readlines()
            file.close()

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

                token = Token(token_type, value)
                token_list.append(token)

        parser = Parser(token_list)
        ast = parser.parse()

        # Imprimir errores
        with open("src/assets/erroresSintactico.txt", "w", encoding="utf-8") as f:
            if parser.errors:
                print("Errores de sintaxis:")
                for error in parser.errors:
                    f.write(error + "\n")
                    print(error)
            f.close()

        # Imprimir AST
        with open("src/assets/arbolSintactico.txt", "w", encoding="utf-8") as f:
            print("Arbol Sintactico:")
            f.write("Arbol Sintactico\n")

            def print_ast(node, level=0, is_last_child=False):
                indent = " | " * level
                print(f"{indent}{node.value}")
                if node.value != "Error":
                    f.write(f"{indent}{node.value}\n")
                for i, child in enumerate(node.children):
                    is_last = i == len(node.children) - 1
                    print_ast(child, level + 1, is_last)

            print_ast(ast)

            f.close()