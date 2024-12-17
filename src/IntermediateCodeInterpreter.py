class TMVirtualMachine:
    def __init__(self):
        self.memory = {}  # Almacena las variables
        self.stack = []  # Simula la pila de operaciones
        self.pc = 0  # Contador de programa (instrucción actual)
        self.instructions = []  # Lista de instrucciones cargadas
        self.label_map = {}  # Mapeo de etiquetas a índices de instrucciones
        self.running = True  # Estado de la máquina virtual

    def load_program(self, instructions):
        """Carga las instrucciones del programa."""
        self.instructions = instructions
        self._build_label_map()

    def _build_label_map(self):
        """Construye el mapeo de etiquetas a índices."""
        for idx, instruction in enumerate(self.instructions):
            #instruccon que tenga una L y numero L1 o L2 etc
            if instruction.startswith("L") and instruction[1:].isnumeric():
                label = instruction
                self.label_map[label] = idx
                

    def execute(self):
        """Ejecuta las instrucciones del programa."""
        while self.running and self.pc < len(self.instructions):
            instruction = self.instructions[self.pc].strip()
            self.pc += 1
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        """Ejecuta una instrucción específica."""


        parts = instruction.split()
        opcode = parts[0]

        if opcode in ["int", "float"]:
            # Ignorar declaraciones de variables
            return

        if opcode == "LDC":
            # Cargar constante
            if len(parts) < 2:
                print(f"Error: Falta argumento en LDC: {instruction}")
                self.running = False
                return
            value = float(parts[1]) if '.' in parts[1] else int(parts[1])
            self.stack.append(value)

        elif opcode == "LDA":
            # Cargar dirección de variable
            if len(parts) < 2:
                print(f"Error: Falta argumento en LDA: {instruction}")
                self.running = False
                return
            var_name = parts[1]
            if var_name not in self.memory:
                self.memory[var_name] = 0
            self.stack.append(var_name)

        elif opcode == "LOD":
            # Cargar valor de variable
            if len(parts) < 2:
                print(f"Error: Falta argumento en LOD: {instruction}")
                self.running = False
                return
            var_name = parts[1]
            self.stack.append(self.memory.get(var_name, 0))

        elif opcode == "STO":
            # Almacenar valor en variable
            #en caso de la instruccion anterior ser un RDI nno hacer nada
            if self.instructions[self.pc-2] == "RDI":
                return
            
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para STO: {instruction}")
                self.running = False
                return
            value = self.stack.pop()
            var_name = self.stack.pop()
            self.memory[var_name] = value

        elif opcode == "ADD":
            # Sumar los dos valores superiores de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para ADD: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)

        elif opcode == "SUB":
            # Restar los dos valores superiores de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para SUB: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)

        elif opcode == "MUL":
            # Multiplicar los dos valores superiores de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para MUL: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)

        elif opcode == "DIV":
            # Dividir los dos valores superiores de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para DIV: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise ZeroDivisionError("Error: División por cero.")
            self.stack.append(a / b)
        #MOD %
        elif opcode == "MOD":
            # Modulo de los dos valores superiores de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para MOD: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a % b)
            
        elif opcode == "RDI":
            # Leer entrada del usuario
            if len(self.stack) < 1:
                print(f"Error: Pila insuficiente para RDI: {instruction}")
                self.running = False
                return
            var_name = self.stack.pop()
            try:
                value = float(input(f"Ingrese el valor de '{var_name}': "))
                #si el valor es x.0 hacer un entero
                if value % 1 == 0:
                    value = int(value)
                self.memory[var_name] = value
            except (ValueError):
                print(f"Error: Valor no numérico para la variable '{var_name}'.")
                self.running = False
                return

            self.memory[var_name] = value

        elif opcode == "WRI":
            # Escribir salida
            if len(self.stack) < 1:
                print(f"Error: Pila insuficiente para WRI: {instruction}")
                self.running = False
                return
            value = self.stack.pop()
            print(f"Salida: {value}")

        elif opcode == "JMP":
            # Salto incondicional
            if len(parts) < 2:
                print(f"Error: Falta argumento en JMP: {instruction}")
                self.running = False
                return
            label = parts[1]
            # validar si esta en una parte mas adelnate del codigo (recorrer el resto de instruucines)
            

            if label not in self.label_map:
                print(f"Error: Etiqueta no encontrada: {label}")
                self.running = False
                return
            self.pc = self.label_map[label]

        elif opcode == "FJP":
            # Salto condicional falso
            if len(parts) < 2:
                print(f"Error: Falta argumento en FJP: {instruction}")
                self.running = False
                return
            label = parts[1]
            if(len(self.stack) > 0):
                condition = self.stack.pop()
                if not condition:
                    if label not in self.label_map:
                        print(f"Error: Etiqueta no encontrada: {label}")
                        self.running = False
                        return
                    self.pc = self.label_map[label]
        elif instruction.startswith("L") and instruction[1:].isnumeric():
            
            pass

        elif opcode in ["JGT","JLT","JLE","JGE","JEQ","JNE"]:
            # solo retorna logicamente un verdaro o falso de los 2 ultimos de la pila
            if len(self.stack) < 2:
                print(f"Error: Pila insuficiente para {opcode}: {instruction}")
                self.running = False
                return
            b = self.stack.pop()
            a = self.stack.pop()
            condition = False
            if opcode == "JGT":
                condition = a > b
            elif opcode == "JLT":
                condition = a < b
            elif opcode == "JLE":
                condition = a <= b
            elif opcode == "JGE":
                condition = a >= b
            elif opcode == "JEQ":
                condition = a == b
            elif opcode == "JNE":
                condition = a!= b
            self.stack.append(condition)
            if condition:
                self.pc +=1
            

        elif opcode == "HALT":
            # Detener la ejecución
            self.running = False

        else:
            print(f"Instrucción desconocida: {instruction}")

    def print_state(self):
        """Imprime el estado actual de la memoria y la pila."""
        print("\nEstado de la Máquina Virtual:")
        print("Memoria:", self.memory)
        print("Pila:", self.stack)

# Ejemplo de uso
if __name__ == "__main__":
    #estraer las instrucciones de src/assets/codigo_intermedio.txt
    with open("assets/codigo_intermedio.txt", "r") as file:
        instructions = file.readlines()
        file.close()

    program = [instruction.strip() for instruction in instructions]


    try:
        vm = TMVirtualMachine()
        vm.load_program(program)
        vm.execute()
        vm.print_state()
        #keyinterrupted
    except KeyboardInterrupt:
        print("\n")
    except ZeroDivisionError as e:
        print(f"\nError: {str(e)}")
