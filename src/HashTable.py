from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
import os

class SymbolTableWidget(QMainWindow):
    def __init__(self, file_path, table_widget):
        super().__init__()
        self.table_widget = table_widget
        self.file_path = file_path
        self.load_symbol_table()

    def load_symbol_table(self):
        if not os.path.exists(self.file_path):
            print(f"El archivo {self.file_path} no existe.")
            return

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        data_lines = [line for line in lines[2:] if '|' in line and not line.startswith('+')]
        self.table_widget.setRowCount(len(data_lines))
        self.table_widget.setColumnCount(5)

        headers = ["Nombre Variable", "Tipo", "Valor", "Registro (loc)", "Números de líneas"]
        self.table_widget.setHorizontalHeaderLabels(headers)

        for row_idx, line in enumerate(data_lines):
            data = line.strip().split('|')
            data = [item.strip() for item in data if item.strip()]  # Eliminar elementos vacíos

            for col_idx, item in enumerate(data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))

        self.table_widget.resizeColumnsToContents()
##divicion trunca