from PyQt5.QtWidgets import QLabel

class LineColumnInfoWidget(QLabel):
    def __init__(self, parent=None):
        super(LineColumnInfoWidget, self).__init__(parent)
        #self.setText("Línea: 1, Columna: 1")

    def update_info(self, line, column):
        self.setText(f"Línea: {line}, Columna: {column}")
