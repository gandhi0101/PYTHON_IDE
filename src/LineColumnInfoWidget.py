from PyQt5.QtWidgets import QLabel

class LineColumnInfoWidget(QLabel):
	def __init__(self, parent=None):
		super(LineColumnInfoWidget, self).__init__(parent)
		#self.setText("Línea: 1, Columna: 1")

	def update_info(self, line, column):
		self.setText(f"Línea: {line}, Columna: {column}		  .")
		
	def resizeEvent(self, event):
		super().resizeEvent(event)
		# Obtén el ancho del texto y ajusta el ancho del widget
		text_width = self.fontMetrics().width(self.text())
		self.setFixedWidth(text_width + 900)  # Agrega un espacio adicional para mayor claridad



