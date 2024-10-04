from PyQt5.QtWidgets import QTextEdit,QSizePolicy
from LineNumberArea import LineNumberArea
from CodeEditor import CodeEditor
from LineColumnInfoWidget import LineColumnInfoWidget

def setup_editor(ide):
    try:
        ide.text_editor = CodeEditor(ide)
        ide.text_editor.setGeometry(5, 30, 900, 500)
    except Exception as e:
        print(f"Error al configurar el editor de código: {e}")

    try:
        ide.text_editor.setPlainText("Escribe aquí...")
    except Exception as e:
        print(f"Error al establecer el texto inicial del editor: {e}")

    try:
        ide.text_editor.textChanged.connect(ide.handleTextChanged)
        ide.text_editor.cursorPositionChanged.connect(ide.update_line_column_info)
    except Exception as e:
        print(f"Error al conectar las señales del editor de código: {e}")

    try:
        ide.line_column_widget = LineColumnInfoWidget(ide)
        ide.line_column_widget.move(20, ide.height() - ide.line_column_widget.height() - 2)
    except Exception as e:
        print(f"Error al configurar el widget de información de línea y columna: {e}")
