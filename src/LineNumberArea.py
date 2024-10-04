from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QPainter, QTextFormat
from PyQt5.QtCore import QSize

class LineNumberArea(QWidget):
	def __init__(self, editor):
		super().__init__(editor)
		self.codeEditor = editor

	def sizeHint(self):
		return QSize(self.editor.lineNumberAreaWidth(), 500)

	def paintEvent(self, event):
		self.codeEditor.lineNumberAreaPaintEvent(event)
		