def imprimir_arbol(nodo, nivel=0, prefijo=""):
    # Imprime el nodo actual con su nivel
    print("    " * nivel + prefijo + nodo["node_type"])
    
    # Recorre los hijos del nodo
    for hijo in nodo.get("children", []):
        nuevo_prefijo = "└──"
        imprimir_arbol(hijo, nivel + 1, nuevo_prefijo)

# Tu JSON
mi_json = {
    "node_type": "MainRoot",
    "token_type": None,
    "value": None,
    "children": [
        {
            "node_type": "MainFunction",
            "token_type": None,
            "value": None,
            "children": [
                {
                    "node_type": "IntStatement",
                    "token_type": None,
                    "value": None,
                    "children": [
                        {
                            "node_type": "Factor",
                            "token_type": "ID",
                            "value": "x",
                            "children": []
                        },
                        {
                            "node_type": "Assignment",
                            "token_type": "ASSIGN",
                            "value": "=",
                            "children": [
                                {
                                    "node_type": "Factor",
                                    "token_type": "INTEGER",
                                    "value": "0",
                                    "children": []
                                }
                            ]
                        },
                        {
                            "node_type": "IfStatement",
                            "token_type": "IF",
                            "value": None,
                            "children": [
                                {
                                    "node_type": "Comparison",
                                    "token_type": "EQ",
                                    "value": "==",
                                    "children": [
                                        {
                                            "node_type": "Factor",
                                            "token_type": "ID",
                                            "value": "x",
                                            "children": []
                                        },
                                        {
                                            "node_type": "Factor",
                                            "token_type": "INTEGER",
                                            "value": "0",
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "node_type": "Block",
                                    "token_type": None,
                                    "value": None,
                                    "children": [
                                        {
                                            "node_type": "Assignment",
                                            "token_type": "ASSIGN",
                                            "value": "=",
                                            "children": [
                                                {
                                                    "node_type": "Factor",
                                                    "token_type": "ID",
                                                    "value": "x",
                                                    "children": []
                                                },
                                                {
                                                    "node_type": "Factor",
                                                    "token_type": "INTEGER",
                                                    "value": "10",
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}


# Imprime el árbol
imprimir_arbol(mi_json)
