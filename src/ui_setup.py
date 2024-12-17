import contextlib
from io import StringIO
import platform
from tkinter import messagebox
from PyQt5.QtWidgets import QMainWindow,QApplication, QVBoxLayout,  QLineEdit
from IntermediateCode import Compiler
from IntermediateCodeInterpreter import TMVirtualMachine
from TreeViewSyntax import TreeViewSyntax
from lexer import LexicalScaner
import semantic
import HashTable
from sint import Syntax
from tabs_setup import setup_output_tabs, setup_bottom_widget
from code_execution import setup_editor
from PyQt5.QtGui import QIcon
import os
from menu import MenuHandler
from PyQt5.QtCore import QProcess

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
		is_mac = platform.system() == 'Darwin'
		# Configuración de la ventana
		self.setGeometry(100, 100, 1750, 910)
		self.setWindowTitle('IDE Compiler Gandhi Armando Salvador')
		if is_mac:
			 # Nombre en el Dock
			
			self.setWindowIcon(QIcon('src/assets/icons/principal.png')) 
		else: 
			self.setWindowIcon(QIcon(os.path.join('src', 'assets', 'icons', 'principal.png')))
	
	def setup_menu(self):
		# Configuración del menú
		self.menu_handler = MenuHandler(self)
		menubar = self.menuBar()
	def run_code(self):
		if(self.current_file==''):
		#si ya esta abirto el archivo pero no se guardaron los cambios
			try:
				if self.parent.text_editor.document().isModified():
				#preguntar por la ubicación para guardar
					reply = self.menu_handler.confirm_save_changes()
				if reply == messagebox.Cancel:
					return
				elif reply == messagebox.Yes:
					self.menu_handler.save_file()
				elif(self.current_file==''):
					print('No hay un archivo abierto')
					#abrir un documento
					self.menu_handler.open_file()
			except Exception:
				print('Error al abrir el archivo')
			except ValueError:
				print('No hay un archivo abierto')
				
			
		else:
			try:
				print('Running code')
				self.run_lexical()
				self.run_syntax()
				self.run_semantic()
				with open("src/assets/arbol_sintactico_anotado.txt", "r") as file:
					syntax_tree_text = file.read()
				compiler = Compiler(syntax_tree_text=syntax_tree_text)
				compiler.compile()
				
				
				
			except Exception as e:
				print(e)
			except ValueError as e:
				print(f'No hay un archivo abierto {e}')
			self.output_middle_code()
			self.output_terminal()
	
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
	
	def run_semantic(self):
		# Borrar contenido anterior
		

		#print("run semantic")
		
		# if(self.current_file==''):
		# 	self.menu_handler.confirm_save_changes()
		# else:
			
			try:
			# Crear una instancia de SemanticProcessor
				self.text_semanticErrors.clear()
				print("semantic")
				processor = semantic.SemanticProcessor()
				
		
			except Exception as e:
				print(e)

			try:
				self.output_semamtic()
				self.output_hash_table()
				with open("src/assets/errores_semanticos.txt", "r") as file_error:
					self.output_semantic_error(file_error.read())
					file_error.close()
			except Exception as e:
				print(e)

				
		
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
	
	

	def output_syntax(self ):
		try:

			tree_view_syntax = TreeViewSyntax("src/assets/arbolSintactico.txt") 
			self.text_syntaxOutput.setModel(tree_view_syntax.model)

			self.text_syntaxOutput.expandAll()
			index = self.errors_widget.indexOf(self.text_syntaxOutput)
			self.errors_widget.setCurrentIndex(index)
		except Exception as e:
			print(f"Error while displaying syntax tree: {e}")

	def output_syntax_error(self, out):
		try:
			self.text_syntaxErrors.setPlainText(out)
			index = self.errors_widget.indexOf(self.text_syntaxErrors)
			self.errors_widget.setCurrentIndex(index)
		except Exception as e:
			print(f"Error while displaying syntax errors: {e}")
	

	def output_semamtic(self):
		# Clear the widget before displaying new results
		
		self.text_semanticOutput.setModel(None)

		print("output semamtic")
		tree_view_semantic = TreeViewSyntax("src/assets/arbol_sintactico_anotado.txt") 
		self.text_semanticOutput.setModel(tree_view_semantic.model)
		self.text_semanticOutput.expandAll()
		# # Enable horizontal scrolling
		# self.tree_view_semantic.header().setSectionResizeMode(QHeaderView.Interactive)
		# self.tree_view_semantic.header().setSectionResizeMode(0, QHeaderView.Interactive)
		# self.tree_view_semantic.setColumnWidth(0, 200)  # Ancho máximo de 200 píxeles para la columna 0


		
		index = self.errors_widget.indexOf(self.text_semanticOutput)
		self.errors_widget.setCurrentIndex(index)
		


	def output_semantic_error(self, out):
		print("output semamtic error")
		self.text_semanticErrors.setPlainText(out)
		index = self.errors_widget.indexOf(self.text_semanticErrors)
		self.errors_widget.setCurrentIndex(index)

		

	
	def output_hash_table(self):
		"""AI is creating summary for output_hash_table
		creear un instancia de la clase hashtable en el widget text_hashTabOutput ambos son QTableWidget
		"""
		HashTable.SymbolTableWidget(file_path="src/assets/tabla_simbolos.txt", table_widget=self.text_hashTabOutput)
	

	def output_middle_code(self):
		# Clear the widget before displaying new results
		self.text_intermediateCodeOutput.clear()

		try:
			with open("src/assets/codigo_intermedio.txt", "r") as file:
				self.text_intermediateCodeOutput.setPlainText(file.read())
				file.close()

			index = self.errors_widget.indexOf(self.text_intermediateCodeOutput)
			self.errors_widget.setCurrentIndex(index)
		except Exception as e:
			print(f"Error while displaying middle code: {e}")


	def output_terminal(self):
		"""
		Abre una terminal externa ejecutando el comando deseado.
		"""
		self.terminal_process = QProcess(self)

		working_dir = os.path.abspath(os.path.dirname(__file__))
		# Detectar el sistema operativo y seleccionar la terminal
		system = platform.system()
		if system == "Windows":
			shell = "cmd.exe"
			args = ["/k", "python src/IntermediateCodeInterpreter.py"]
		elif system == "Darwin":  # macOS
			        # Usar AppleScript para abrir el Terminal y ejecutar el comando
			shell = "osascript"
			args = [
				"-e",
				f"""tell application "Terminal" 
					do script "cd {working_dir} && python IntermediateCodeInterpreter.py"
                	activate
            	end tell
				"""
			]
		elif system == "Linux":
			shell = "x-terminal-emulator"  # Cambia a tu emulador preferido como gnome-terminal o xterm
			args = ["-e", "python IntermediateCodeInterpreter.py"]
		else:
			raise RuntimeError(f"Sistema operativo no soportado: {system}")

		# Iniciar la terminal externa con el comando configurado
		self.terminal_process.start(shell, args)

		print(f"Terminal externa abierta usando {shell} en {system}")
	
	def update_line_column_info(self):
		current_line = self.text_editor.textCursor().blockNumber() + 1
		current_column = self.text_editor.textCursor().positionInBlock() + 1

		# Actualiza la información en el widget
		self.line_column_widget.update_info(current_line, current_column)
