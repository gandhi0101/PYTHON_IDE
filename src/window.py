import sys
from Lexical import LexicalScanner
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMenu, QAction, QTabWidget
from PyQt5.QtGui import QIcon, QTextCursor
from io import StringIO
import contextlib
import os

from LineNumberArea import LineNumberArea
from CodeEditor import CodeEditor
from menu import MenuHandler
from LineColumnInfoWidget import LineColumnInfoWidget

class PythonIDE(QMainWindow):
	def __init__(self):
		super(PythonIDE, self).__init__()

		self.initUI()
		
		self.clipboard = QApplication.clipboard()
		self.current_file = ''


	def initUI(self):
    
		self.setGeometry(100, 100, 1600, 810)
		self.setWindowTitle('IDE Compiler Gandhi Armando Salvador')
		self.setWindowIcon(QIcon(os.path.join('src','assets', 'icons', 'principal.png')))
		
  		#self.statusBar().addPermanentWidget(self.line_column_widget)
  
		self.menu_handler = MenuHandler(self)
  
		menubar = self.menuBar()# Crear la barra de menú
		
		#entrada de texto a la izquierda
		self.text_editor = CodeEditor(self)
		self.text_editor.setGeometry(30, 30, 1100, 560) #tamaño por defeto
		self.setupEditor()
		# Establecer un texto predeterminado (placeholder)
		placeholder_text = "Escribe aquí..."
		self.text_editor.setPlainText(placeholder_text)
		self.text_editor.textChanged.connect(self.handleTextChanged)



		# "terminal" de salida a la derecha
		specialOutput_widget = QWidget(self)
		specialOutput_widget.setGeometry(1100, 15, 500, 600)

		layuotSpecialOutput = QVBoxLayout(specialOutput_widget)

		self.specialOuputTab = QTabWidget(self)

		self.lexicalOutput = QWidget(self)
		self.syntaxOutput = QWidget(self)
		self.semanticOutput = QWidget(self)
		self.hashTabOutput = QWidget(self)
		self.intermediateCodeOutput = QWidget(self)	

		self.specialOuputTab.addTab(self.lexicalOutput,'Lexico')
		self.specialOuputTab.addTab(self.syntaxOutput,'Sintactico')
		self.specialOuputTab.addTab(self.semanticOutput,'Semantico')
		self.specialOuputTab.addTab(self.hashTabOutput,'Hash Table')
		self.specialOuputTab.addTab(self.intermediateCodeOutput,'Codigo Intermedio')

		self.text_lexicalOutput = QTextEdit(self)
		self.text_lexicalOutput.setReadOnly(True)
		self.text_syntaxOutput = QTextEdit(self)
		self.text_syntaxOutput.setReadOnly(True)
		self.text_semanticOutput = QTextEdit(self)
		self.text_semanticOutput.setReadOnly(True)
		self.text_hashTabOutput = QTextEdit(self)
		self.text_hashTabOutput.setReadOnly(True)
		self.text_intermediateCodeOutput = QTextEdit(self)
		#self.text_intermediateCodeOutput.setReadOnly(True)
  
		lexicalOutput_layout = QVBoxLayout(self.lexicalOutput)
		lexicalOutput_layout.addWidget(self.text_lexicalOutput)
		syntaxOutput_layout = QVBoxLayout(self.syntaxOutput)
		syntaxOutput_layout.addWidget(self.text_syntaxOutput)
		semanticOutput_layout = QVBoxLayout(self.semanticOutput)
		semanticOutput_layout.addWidget(self.text_semanticOutput)
		hashTabOutput_layout = QVBoxLayout(self.hashTabOutput)
		hashTabOutput_layout.addWidget(self.text_hashTabOutput)
		intermediatecodeOutput_layout = QVBoxLayout(self.intermediateCodeOutput)
		intermediatecodeOutput_layout.addWidget(self.text_intermediateCodeOutput)
		
		layuotSpecialOutput.addWidget(self.specialOuputTab)
		#boton provicional de ejecutar
		# self.run_button = QPushButton('Run', self)
		# self.run_button.setGeometry(200, 560, 780, 30)
		# self.run_button.clicked.connect(self.run_code)
		# Crear el widget de abajo (buttom)
		buttom_widget = QWidget(self)
		buttom_widget.setGeometry(0,580,1600,230)
        # Crear un layout vertical para el widget buttom
		layoutErros = QVBoxLayout(buttom_widget)


        # Crear un QTabWidget para gestionar las pestañas
		self.erros_widget = QTabWidget(self)
		

        # Crear widgets para cada pestaña
		self.lexicalErrors = QWidget(self)
		self.syntaxErrors = QWidget(self)
		self.semanticErrors = QWidget(self)
		self.results = QWidget(self)

        # Agregar widgets a las pestañas
		self.erros_widget.addTab(self.lexicalErrors, 'Errores Lexicos')
		self.erros_widget.addTab(self.syntaxErrors, 'Errorres Sintacticos')
		self.erros_widget.addTab(self.semanticErrors, 'Errores Semanticos')
		self.erros_widget.addTab(self.results, 'Resultados')

        # Agregar QTextEdit a cada pestaña (puedes personalizar esto según tus necesidades)
		self.text_lexicalErrors = QTextEdit(self)
		self.text_lexicalErrors.setReadOnly(True)
		self.text_syntaxErrors = QTextEdit(self)
		self.text_syntaxErrors.setReadOnly(True)
		self.text_semanticErrors = QTextEdit(self)
		self.text_semanticErrors.setReadOnly(True)
		self.text_results = QTextEdit(self)
		self.text_results.setReadOnly(True)

		lexicalErrors_layout = QVBoxLayout(self.lexicalErrors)
		lexicalErrors_layout.addWidget(self.text_lexicalErrors)

		syntaxErrors_layout = QVBoxLayout(self.syntaxErrors)
		syntaxErrors_layout.addWidget(self.text_syntaxErrors)

		semanticErrors_layout = QVBoxLayout(self.semanticErrors)
		semanticErrors_layout.addWidget(self.text_semanticErrors)

		results_layout = QVBoxLayout(self.results)
		results_layout.addWidget(self.text_results)

        # Agregar el QTabWidget al layout principal
		layoutErros.addWidget(self.erros_widget)
		self.line_column_widget = LineColumnInfoWidget(self)
		self.line_column_widget.move(20, self.height() - self.line_column_widget.height()-2 )
		self.text_editor.cursorPositionChanged.connect(self.update_line_column_info)

  
	def handleTextChanged(self):
        # Verificar si el texto actual es igual al placeholder
		if self.text_editor.toPlainText() == "Escribe aquí...":
            # Limpiar el texto cuando el usuario comienza a escribir
			self.text_editor.clear()
   
	def setupEditor(self):
		layout = QVBoxLayout(self)
		layout.addWidget(self.text_editor)



	def run_code(self):
		code = self.text_editor.toPlainText()
		output_stream = StringIO()
		
		with contextlib.redirect_stdout(output_stream):
			try:
				exec(code)
			except Exception as e:
				print(e)

		output = output_stream.getvalue()
		self.text_results.setPlainText(output)
		# Seleccionar y mostrar la pestaña de resultados
		index = self.erros_widget.indexOf(self.results)
		self.erros_widget.setCurrentIndex(index)
  
	def run_lexical(self):
     # Borrar contenido anterior
		self.text_lexicalOutput.clear()
		self.text_lexicalErrors.clear()
		if(self.current_file==''):
			self.menu_handler.confirm_save_changes()
		else:
			lexicalscanner = LexicalScanner(self)
			lexicalscanner.lexico()

	# def output_lexical(self,out):
		
	# 	self.text_lexicalOutput.setPlainText(out)
	# 	index = self.erros_widget.indexOf(self.lexicalOutput)
	# 	self.erros_widget.setCurrentIndex(index)
	# 	print("run lexical")
	def run_syntax(self):
		print("run syntax")
	def run_semantic(self):
		print("run semantic")
	def update_line_column_info(self):
		current_line = self.text_editor.textCursor().blockNumber() + 1
		current_column = self.text_editor.textCursor().positionInBlock() + 1

	    # Actualiza la información en el widget
		self.line_column_widget.update_info(current_line, current_column)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ide = PythonIDE()
	ide.show()
	sys.exit(app.exec_())
