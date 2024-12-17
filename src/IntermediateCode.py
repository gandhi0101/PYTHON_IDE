import os
import re

class Node:
    def __init__(self, value, children=None, line_no=None, type=None, identificator=False, val=None):
        self.value = value
        self.children = children or []
        self.line_no = line_no
        self.type = type
        self.identificator = identificator
        self.val = val

class TreeDeserializer:
    @staticmethod
    def parse_tree_from_text(text):
        lines = text.strip().split("\n")

        root = None
        stack = []

        for line in lines:
            depth = line.count("| ")
            node_data = line.replace("| ", "").strip()

            if not node_data:
                continue

            # Extract value and notes (e.g., [Tipo: int], [Valor: 45])
            match = re.match(r"(.*?)(\[.*\]|\( Linea \d+\))?$", node_data)
            value = match.group(1).strip()
            notes = match.group(2)

            # Parse notes
            line_no, type_, val, identificator = None, None, None, False
            if notes:
                line_no_match = re.search(r"\( Linea (\d+)\)", notes)
                type_match = re.search(r"Tipo: (\w+)", notes)
                val_match = re.search(r"Valor: ([\d\.\-]+)", notes)

                if line_no_match:
                    line_no = int(line_no_match.group(1))
                if type_match and type_match.group(1) != "None":
                    type_ = type_match.group(1)
                if val_match:
                    try:
                        val = float(val_match.group(1)) if '.' in val_match.group(1) else int(val_match.group(1))
                    except ValueError:
                        val = None

            # Determine if the node is an identifier based on its value
            identificator = value.isidentifier() and not value.isnumeric()

            # Create the node and attach it to the tree
            node = Node(value=value, line_no=line_no, type=type_, val=val, identificator=identificator)

            if depth == 0:
                root = node
                stack = [node]
            else:
                while len(stack) > depth:
                    stack.pop()

                if stack:
                    stack[-1].children.append(node)
                stack.append(node)

        # Clean the tree: remove notes from node values
        TreeDeserializer.clean_tree(root)

        print("\n\nÁrbol sintáctico procesado:")
        #TreeDeserializer.print_tree(root)
        return root

    @staticmethod
    def clean_tree(node):
        if node:
            # Strip any remaining notes from the node value
            node.value = re.sub(r"\[.*\]|\( Linea \d+\)", "", node.value).strip()
            for child in node.children:
                TreeDeserializer.clean_tree(child)

    @staticmethod
    def print_tree(node, depth=0):
        if node:
            #print("  " * depth + f"{node.value}")
            for child in node.children:
                TreeDeserializer.print_tree(child, depth + 1)




class InputReader:
    @staticmethod
    def read_inputs(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo de entrada '{file_path}' no se encuentra.")

        inputs = {}
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    var_name, value = parts
                    try:
                        inputs[var_name] = float(value)
                    except ValueError:
                        print(f"Error: valor no numérico para la variable '{var_name}'.")
                        return None
        return inputs

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def get_temp(self):
        self.temp_count += 1
        return f"{self.temp_count}"

    def generate_code(self, node):
        handler = getattr(self, f"_handle_{node.value.lower()}", self._default_handler)
        handler(node)

    def _handle_programa(self, node):
        for child in node.children:
            self.generate_code(child)

    def _handle_sentencias(self, node):
        for child in node.children:
            self.generate_code(child)

    def _handle_bloque(self, node):
        for child in node.children:
            self.generate_code(child)

    def _handle_declaracionint(self, node):
        for child in node.children:
            self.code.append(f"int {child.value}")

    def _handle_declaracionfloat(self, node):
        for child in node.children:
            self.code.append(f"float {child.value}")


    def _handle_sentenciaif(self, node):
        condition_code = self.generate_expression_code(node.children[0])  
        else_label = self.new_label() 
        end_label = self.new_label()
        self.code.append(f"FJP {else_label}")
        self.generate_code(node.children[1])
        self.code.append(f"JMP {end_label}")

        # Bloque else (si existe)
        self.code.append(f"{else_label}")
        if len(node.children) > 2:  
            self.generate_code(node.children[2])
        self.code.append(f"{end_label}")


    def _handle_sentenciawhile(self, node):
        start_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"{start_label}")
        condition_code = self.generate_expression_code(node.children[0])
        self.code.append(f"FJP {end_label}")

        if len(node.children) > 1:
            self.generate_code(node.children[1])
        self.code.append(f"JMP {start_label}")
        self.code.append(f"{end_label}")


    def _handle_sentenciado(self, node):
        start_label = self.new_label()  
        condition_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"{start_label}")
        self.generate_code(node.children[0])

        self.code.append(f"{condition_label}")
        condition_code = self.generate_expression_code(node.children[1])
        self.code.append(f"FJP {end_label}")
        self.code.append(f"JMP {start_label}")

        if len(node.children) > 2:
            next_node = node.children[2]
            if next_node.value.lower() == "sentenciawhile":
                if len(next_node.children) > 0:
                    self._handle_sentenciawhile(next_node)
                else:
                    self.generate_code(next_node)
        self.code.append(f"{end_label}")



    def _handle_sentenciaoutput(self, node):
        expr_code = self.generate_expression_code(node.children[0])
        
        # Handle output for any type of value (text, number, or identifier)
        if node.children[0].type == 'id':
            self.code.append(f"LOD {node.children[0].value}")
            if '.' in str(node.children[0].val):
                node.children[0].type = 'float'
            else:
                node.children[0].type = 'int'
            
        else:
            self.code.append(f"LOD {node.children[0].value}")  # Load top of stack if not an identifier
        self.code.append("WRI")

    def _handle_sentenciainput(self, node):
        if node.children[0].value == 'IdList':
            # Recorre la lista de variables 
            for var in node.children[0].children:
                if var.type == 'id':
                    self.code.append(f"LDA {var.value}")
                    self.code.append("RDI")
                    self.code.append(f"STO {self.get_temp()}")
                
                
                

        

    def generate_expression_code(self, node):
        if node.value in ["+", "-", "*", "/"]:
            left_code = self.generate_expression_code(node.children[0])
            right_code = self.generate_expression_code(node.children[1])
            op_map = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD",}
            
            temp = self.get_temp()

            if left_code is not None:
                self.code.append(f"{op_map[node.value]} {temp} {right_code} {left_code}")
            else:
                expr_code = self.generate_expression_code(node.children[1])
                if right_code is not None:
                    self.code.append(f"{op_map[node.value]} {temp} {right_code} {expr_code}")
                else:
                    expr_code = self.generate_expression_code(node.children[0])
                    self.code.append(f"{op_map[node.value]} {temp} {expr_code} {right_code}")
            return temp
        elif node.value  in [">","<","<=",">=", "==", "!=" ]:
            left_code = self.generate_expression_code(node.children[0])
            right_code = self.generate_expression_code(node.children[1])
            op_map = {">": "JGT", "<": "JLT", "<=": "JLE", ">=": "JGE", "==": "JEQ", "!=": "JNE"}
            temp = self.get_temp()
            if left_code is not None:
                self.code.append(f"{op_map[node.value]} {temp} {right_code} {left_code}")
            else:
                expr_code = self.generate_expression_code(node.children[1])
                
                self.code.append(f"{op_map[node.value]} {temp} {right_code} {expr_code}")
            return temp
        elif node.value in ["True", "False"]:
            temp = self.get_temp()
            self.code.append(f"LDC {int(node.value == 'True')}")
            return temp
        
        elif self.is_number(node.value):
            temp = self.get_temp()
            self.code.append(f"LDC {node.value}")
            return temp
        elif node.identificator:
            temp = self.get_temp()
            self.code.append(f"LOD {node.value}")
            return temp
        elif node.type == 'id':
            temp = self.get_temp()
            self.code.append(f"LOD {node.value}")
            return temp

    
    def _handle_asignacion(self, node):
        temp = self.get_temp()
        dest = node.children[0].value
        self.code.append(f"LDA {dest}")

        if len(node.children[1].children) > 1:
            
            expr_code = self.generate_expression_code(node.children[1])
            
            
           
            self.code.append(f"STO {expr_code}")
        else: 
            expr_value = node.children[1].value
            # si la cadena es numerica es un LDC 
            try:
                expr_value = float(expr_value)
                #si el flotante es .0 convertiur a entero 
                if expr_value % 1 == 0:
                    expr_value = int(expr_value)
            except ValueError:
                self.code.append(f"LOD {dest} {node.children[1].val}")

            if isinstance(expr_value, (int, float)):
                self.code.append(f"LDC {expr_value}")
                

            self.code.append(f"STO {temp}")
        

    def _default_handler(self, node):
        print(f"Advertencia: Nodo no manejado: {node.value.lower()}")
        for child in node.children:
            self.generate_code(child)

    @staticmethod
    def is_number(value):
        #validar si es entero o flotante
        if value.isdigit():
            return True
        elif "." in value:
            try:
                float(value)
                return True
            except ValueError:
                return False
        else:
            return False


class Compiler:
    def __init__(self, syntax_tree_text, output_file="src/assets/codigo_intermedio.txt"):
        self.syntax_tree_text = syntax_tree_text
        self.output_file = output_file

    def compile(self):
        root_node = TreeDeserializer.parse_tree_from_text(self.syntax_tree_text)

        code_generator = CodeGenerator()
        code_generator.generate_code(root_node)

        print("\n\nCódigo intermedio generado:")
        # for line in code_generator.code:
        #     if line is not None:
        #       print(line)
       #print("HALT")
        with open(self.output_file, "w") as file:
            for line in code_generator.code:
                if line is not None:
                    file.write(line + "\n")
            file.write("HALT")

if __name__ == "__main__":
    #leer desde el file src/assets/arbol_sintactico_anotado.txt
    with open("src/assets/arbol_sintactico_anotado.txt", "r") as file:
        syntax_tree_text = file.read()
    compiler = Compiler(syntax_tree_text=syntax_tree_text)
    compiler.compile()
    print("Compilación completada. Código intermedio generado en 'codigo_intermedio.txt'.")
