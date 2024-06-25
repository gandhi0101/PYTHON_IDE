import threading
from  TokenType import TokenType
from TreeNode import TreeNode
from typing import List, Tuple, Union

class Analyzer:

       # Inicializar el contenedor de errores con un lock
    errors_lock = threading.Lock()
    errors = []
     # Función para comparar el token actual con el esperado
    def match_token(self, tokens: List[Tuple[TokenType, str, int, int]], expected: TokenType, current_token: List[int]) -> Union[None, str]:
        if current_token[0] < len(tokens) and tokens[current_token[0]][0] == expected:
            current_token[0] += 1
            return None
        else:
            return f"Error de sintaxis: se esperaba {expected} en la posición {tokens[current_token[0]] if current_token[0] < len(tokens) else 'EOF'}"
        
    def log_error(self, error: str):
        with self.errors_lock:
            if error not in self.errors:
                self.errors.append(error)

    # Función para parsear un término
    
    
    
    