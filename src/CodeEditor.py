from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextFormat, QPainter
from PyQt5.QtCore import Qt, QRect
from LineNumberArea import LineNumberArea


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        # Configuración del editor de código
        self.setupEditor()

    def setupEditor(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self)
        # Configuración de la barra de desplazamiento
        scroll_bar = self.verticalScrollBar()
        scroll_bar.rangeChanged.connect(self.updateLineNumberAreaWidth)
        scroll_bar.valueChanged.connect(self.updateLineNumberArea)

        
        self.textChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width("9") * digits
        return space

    def updateLineNumberArea(self):
        rect = QRect(0, 0, self.lineNumberArea.width(), self.lineNumberArea.height())
        self.lineNumberArea.update(rect)
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
        self.updateLineNumberAreaWidth()

    def updateLineNumberAreaWidth(self):
        width = self.lineNumberAreaWidth()
        self.setViewportMargins(width, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )
        self.updateLineNumberAreaWidth()

    def highlightCurrentLine(self):
        extraSelections = []

        selection = QTextEdit.ExtraSelection()
        # lineColor = Qt.yellow.lighter(160)
        # selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        # print("estos numeros corresponden a \n top:"+str(top)+"ancho del numberr area: "+str(self.lineNumberArea.width())+"el alto del area: "+str(self.fontMetrics().height()))
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                # esta linea permite mostrar 1 solo cuadro a la hora de creear las lineas
                # painter.drawText(0, 1*blockNumber, 5, 520,Qt.AlignRight, number)
                painter.drawText(
                    0,
                    int(top),
                    self.lineNumberArea.width(),
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number,
                )
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
