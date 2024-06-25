from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextFormat, QPainter
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtGui import QTextOption, QTextCharFormat, QColor, QFont
import re
import lexer
from LineNumberArea import LineNumberArea


class CodeEditor(QPlainTextEdit):
    textChangedCustom = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        # Configuración del editor de código
        self.setupEditor()
        self.textChanged.connect(self.highlightSyntax)
        # self.detectErrors()

    def setupEditor(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self)
        # Desactivar la envoltura de texto
        self.setWordWrapMode(QTextOption.NoWrap)
        scroll_bar = self.verticalScrollBar()
        scroll_bar.rangeChanged.connect(self.updateLineNumberAreaWidth)
        scroll_bar.valueChanged.connect(self.updateLineNumberArea)

        # Configuración de la barra de desplazamiento horizontal
        h_scrollbar = QScrollBar(Qt.Horizontal, self)
        layout.addWidget(h_scrollbar)

        # Establecer la barra de desplazamiento horizontal
        self.setHorizontalScrollBar(h_scrollbar)

        # Conectar las señales relevantes
        h_scrollbar.valueChanged.connect(self.updateLineNumberAreaWidth)
        h_scrollbar.rangeChanged.connect(self.updateLineNumberArea)

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
        # self.updateLineNumberAreaWidth()

    def updateLineNumberAreaWidth(self):
        width = self.lineNumberAreaWidth()
        self.setViewportMargins(width, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        bottom_right = self.cursorRect(cursor).bottomRight()

        # Ajusta el ancho del CodeEditor al contenido más ancho
        self.setMinimumWidth(bottom_right.x() + self.lineNumberAreaWidth() + 5)

        # Ajusta la geometría de la barra de desplazamiento horizontal
        # self.horizontalScrollBar().setGeometry(self.contentsRect().left(), self.contentsRect().bottom(), self.contentsRect().width(), 2)

        # Ajusta la geometría del área de texto
        self.lineNumberArea.setGeometry(
            QRect(
                self.contentsRect().left(),
                self.contentsRect().top(),
                self.lineNumberAreaWidth(),
                self.contentsRect().height(),
            )
        )

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

    def current_line_number(self):
        cursor = self.textCursor()
        return cursor.blockNumber() + 1

    def current_column_number(self):
        cursor = self.textCursor()
        return cursor.columnNumber() + 1

    def highlightSyntax(self):
        self.textChanged.disconnect(self.highlightSyntax)

        cursor = self.textCursor()
        # cursor.select(QTextCursor.document)
        # cursor.setCharFormat(QTextCharFormat())

        text = self.toPlainText()
        color_palette = {
            "color1": QColor(Qt.gray),  # Números enteros y reales
            "color2": QColor(Qt.black),  # Identificadores
            "color3": QColor(Qt.green),  # Comentarios de una línea y de múltiples líneas
            "color4": QColor(Qt.darkBlue),  # Palabras reservadas
            "color5": QColor(Qt.magenta),  # Operadores aritméticos y de asignación
            "color6": QColor(Qt.cyan),  # Operadores relacionales
            "color7": QColor(Qt.darkCyan),  # Operadores lógicos
            "color8": QColor(Qt.darkGray),  # Símbolos
        }
        # Definición de patrones para cada token y su color correspondiente
        patterns = [
            (r"\b(\d+(\.\d+)?)\b", "color1", ),  # Números enteros y reales
            (r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "color2",),  # Identificadores
            (r"(\+|\-|\*|\/|%|\^|\+\+|\-\-|=)","color5",),  # Operadores aritméticos y de asignación
            (r"(<=|>=|!=|==|<|>)", "color6", ),  # Operadores relacionales
            (r"(and|or)", "color7", ),  # Operadores lógicos
            (r"\b(for|if|else|do|while|switch|case|integer|double|main|cin|cout)\b","color4",),  # Palabras reservadas
            (r"(\(|\)|\{|\}|\,|\;)", "color8", ),  # Símbolos
            (r"\/\*(.*?)\*/","color3", re.DOTALL),  # Comentario de múltiples líneas
            (r"(//.*)", "color3", )  # Coment de una línea 
        ]

        # Aplicar patrones y colores al texto
        # Aplicar formato de texto a cada token
        for pattern, color, *modifiers in patterns:
            format = QTextCharFormat()
            format.setForeground(color_palette[color])
            regex = re.compile(pattern, *modifiers)
            
            matches = regex.finditer(text)
            for match in matches:
                start, end = match.span()
                if color == "color3":  # Si es un comentario de múltiples líneas
                    # Aplicar formato solo al comentario
                    cursor.setPosition(start)
                    cursor.movePosition(
                        QTextCursor.Right,
                        QTextCursor.KeepAnchor,
                        end - start,
                    )
                    cursor.setCharFormat(format)
                else:
                    # Aplicar formato a todos los matches
                    cursor.setPosition(start)
                    cursor.movePosition(
                        QTextCursor.Right,
                        QTextCursor.KeepAnchor,
                        end - start,
                    )
                    cursor.setCharFormat(format)
        # Volver a conectar la señal textChanged
        self.textChanged.connect(self.highlightSyntax)
        # Emitir la señal custom para indicar que el texto ha cambiado (útil para otras actualizaciones)
        self.textChangedCustom.emit()
