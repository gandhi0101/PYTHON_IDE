import contextlib
from io import StringIO
from PyQt5.QtWidgets import QMainWindow,QApplication, QVBoxLayout
from TreeViewSyntax import TreeViewSyntax
from lexer import LexicalScaner
import semantic
from sint import Syntax
from tabs_setup import setup_output_tabs, setup_bottom_widget
from code_execution import setup_editor
from PyQt5.QtGui import QIcon
import os
from menu import MenuHandler

class PythonIDE(QMainWindow):
	def __init__(self):
		super(PythonIDE, self).__init__()
		self.clipboard = QApplication.clipboard()
		self.current_file = ''
		self.initUI()

	def initUI(self):
		self.setup_window()
		self.setup_menu()
		setup_editor(self)
		setup_output_tabs(self)
		setup_bottom_widget(self)
	
	def setup_window(self):
		# Configuración de la ventana
		self.setGeometry(100, 100, 1750, 910)
		self.setWindowTitle('IDE Compiler Gandhi Armando Salvador')
		self.setWindowIcon(QIcon(os.path.join('src', 'assets', 'icons', 'principal.png')))
	
	def setup_menu(self):
		# Configuración del menú
		self.menu_handler = MenuHandler(self)
		menubar = self.menuBar()
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
		index = self.errors_widget.indexOf(self.results)
		self.errors_widget.setCurrentIndex(index)
  
	def run_lexical(self):
	 # Borrar contenido anterior
		self.text_lexicalOutput.clear()
		self.text_lexicalErrors.clear()
		
		if(self.current_file==''):
			self.menu_handler.confirm_save_changes()
		else:
			
			LexicalScaner().Lexico(self.current_file)
			#lexicalscanner.clearfiles()

			with open("src/assets/lexico.txt", "r") as file:
				self.output_lexical(file.read())
				file.close()
			with open("src/assets/errors.txt", "r") as file_error:
				self.output_lexical_error(  file_error.read())
				file_error.close()
	  
	def handleTextChanged(self):
		# Verificar si el texto actual es igual al placeholder
		if self.text_editor.toPlainText() == "Escribe aquí...":
			# Limpiar el texto cuando el usuario comienza a escribir
			self.text_editor.clear()
   
	def setupEditor(self):
		layout = QVBoxLayout(self)
		layout.addWidget(self.text_editor)



	def output_lexical(self,out):
		self.text_lexicalOutput.setPlainText(out)
		index = self.errors_widget.indexOf(self.text_lexicalOutput)
		self.errors_widget.setCurrentIndex(index)

	def output_lexical_error(self, out):
		self.text_lexicalErrors.setPlainText(out)
		index = self.errors_widget.indexOf(self.text_lexicalErrors)
		self.errors_widget.setCurrentIndex(index)
	
	
	def run_syntax(self):
		# Limpia el contenido del QTreeView
		self.text_syntaxErrors.clear()
			
		sintax = Syntax()
		sintax.sintaxis("src/assets/lexico.txt")
		#sintax.clearfiles(self)

		file = open("src/assets/arbolSintactico.txt", "r")
		self.output_syntax()
		file.close()
		file_error = open("src/assets/erroresSintactico.txt", "r")
		self.output_syntax_error(  file_error.read())
		file_error.close()

		print("run syntax")

	def output_syntax(self ):
		tree_view_syntax = TreeViewSyntax("src/assets/arbolSintactico.txt") 
		self.text_syntaxOutput.setModel(tree_view_syntax.model)

		self.text_syntaxOutput.expandAll()
		index = self.errors_widget.indexOf(self.text_syntaxOutput)
		self.errors_widget.setCurrentIndex(index)

	def output_syntax_error(self, out):
		self.text_syntaxErrors.setPlainText(out)
		index = self.errors_widget.indexOf(self.text_syntaxErrors)
		self.errors_widget.setCurrentIndex(index)
	
	def run_semantic(self):
		
		
	 	# Borrar contenido anterior
		self.text_semanticOutput.clear()
		self.text_semanticErrors.clear()

		print("run semantic")
		try:
			# Crear una instancia de SemanticProcessor
			processor = semantic.SemanticProcessor("src/assets/lexico.txt", "src/assets/errores_semanticos.txt")

			processor.semantic()
		except Exception as e:
			print(e)


		
	def update_line_column_info(self):
		current_line = self.text_editor.textCursor().blockNumber() + 1
		current_column = self.text_editor.textCursor().positionInBlock() + 1

		# Actualiza la información en el widget
		self.line_column_widget.update_info(current_line, current_column)
