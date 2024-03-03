import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMenu, QAction, QTabWidget
from PyQt5.QtGui import QIcon
from io import StringIO
import contextlib

class PythonIDE(QMainWindow):
	def __init__(self):
		super(PythonIDE, self).__init__()

		self.initUI()

	def initUI(self):
    
		self.setGeometry(100, 100, 1600, 810)
		self.setWindowTitle('IDE Compiler GSA')
  
		menubar = self.menuBar()# Crear la barra de menú
		fileMenu = menubar.addMenu('File')
		editMenu = menubar.addMenu('Edit')
		buldigDegug = menubar.addMenu('Buld and Debug') #falta ver su menu desplegable
        
        # Crear acciones para el menú "File"
		newAct = QAction('New', self)
		openAct = QAction('Open', self)
		saveAct = QAction('Save', self)
        # Agregar acciones al menú "File"
		fileMenu.addAction(newAct)
		fileMenu.addAction(openAct)
		fileMenu.addAction(saveAct)
        
        # Crear acciones para el menú "Edit"
		cutAct = QAction('Cut', self)
		copyAct = QAction('Copy', self)
		pasteAct = QAction('Paste', self)

        # Agregar acciones al menú "Edit"
		editMenu.addAction(cutAct)
		editMenu.addAction(copyAct)
		editMenu.addAction(pasteAct)
  
		menubar.addSeparator()
  
		newfileicon = QAction(QIcon('assets\icons\\nuevo-documento.png'),"     ",self)
		menubar.addAction(newfileicon)
		openfileicon = QAction(QIcon('assets\icons\\nuevo-documento.png'),"     ",self)
		menubar.addAction(openfileicon)
		savefileicon = QAction(QIcon('assets\icons\\nuevo-documento.png'),"     ",self)
		menubar.addAction(savefileicon)
  
		closeMenu = menubar.addMenu('Close')
  
		separatorAction = QAction(self)
		separatorAction.setSeparator(True)
		menubar.addAction(separatorAction)
  
		lexicoMenu = menubar.addMenu('Lexico')
		sintacticoMenu = menubar.addMenu('Sintactico')
		semanticoMenu = menubar.addMenu('Semantico')
		compilerMenu = menubar.addMenu('Compilar')
		
		#entrada de texto a la izquierda
		self.text_editor = QTextEdit(self)
		self.text_editor.setGeometry(10, 30, 1100, 520) #tamaño por defeto
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
		self.run_button = QPushButton('Run', self)
		self.run_button.setGeometry(200, 560, 780, 30)
		self.run_button.clicked.connect(self.run_code)
		# Crear el widget de abajo buttom
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
  
	def handleTextChanged(self):
        # Verificar si el texto actual es igual al placeholder
		if self.text_editor.toPlainText() == "Escribe aquí...":
            # Limpiar el texto cuando el usuario comienza a escribir
			self.text_editor.clear()

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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ide = PythonIDE()
	ide.show()
	sys.exit(app.exec_())
