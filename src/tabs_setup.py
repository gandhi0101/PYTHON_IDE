from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QTextEdit, QTreeView, QSizePolicy

def setup_output_tabs(ide):
	ide.special_output_widget = QWidget(ide)
	
	ide.special_output_widget.setGeometry(900, 0, 550, 800)
	ide.special_output_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
	layout_special_output = QVBoxLayout(ide.special_output_widget)

	ide.special_output_tab = QTabWidget(ide)
	add_tab(ide, ide.special_output_tab, 'Lexico', QTextEdit(ide), 'text_lexicalOutput')
	add_tab(ide, ide.special_output_tab, 'Sintactico', QTreeView(), 'text_syntaxOutput')
	add_tab(ide, ide.special_output_tab, 'Semantico', QTextEdit(ide), 'text_semanticOutput')
	add_tab(ide, ide.special_output_tab, 'Hash Table', QTextEdit(ide), 'text_hashTabOutput')
	add_tab(ide, ide.special_output_tab, 'Codigo Intermedio', QTextEdit(ide), 'text_intermediateCodeOutput')

	layout_special_output.addWidget(ide.special_output_tab)

def setup_bottom_widget(ide):
	bottom_widget = QWidget(ide)
	bottom_widget.setGeometry(-15, 500, 950, 300)
	layout_errors = QVBoxLayout(bottom_widget)

	ide.errors_widget = QTabWidget(ide)
	add_error_tab(ide, 'Errores Lexicos', QTextEdit(ide), 'text_lexicalErrors')
	add_error_tab(ide, 'Errores Sintacticos', QTextEdit(ide), 'text_syntaxErrors')
	add_error_tab(ide, 'Errores Semanticos', QTextEdit(ide), 'text_semanticErrors')
	add_error_tab(ide, 'Resultados', QTextEdit(ide), 'text_results')

	layout_errors.addWidget(ide.errors_widget)

def add_tab(ide, tab_widget, title, widget, attr_name):
	setattr(ide, attr_name, widget)
	widget.setReadOnly(True) if isinstance(widget, QTextEdit) else None
	layout = QVBoxLayout()
	layout.addWidget(widget)
	container = QWidget(ide)
	container.setLayout(layout)
	tab_widget.addTab(container, title)

def add_error_tab(ide, title, widget, attr_name):
	setattr(ide, attr_name, widget)
	widget.setReadOnly(True)
	layout = QVBoxLayout()
	layout.addWidget(widget)
	container = QWidget(ide)
	container.setLayout(layout)
	ide.errors_widget.addTab(container, title)
