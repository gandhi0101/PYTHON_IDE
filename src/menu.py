from PyQt5.QtWidgets import QApplication, QFileDialog,QMessageBox, QAction, QMenu
from PyQt5.QtGui import QIcon
import os

class MenuHandler:
    def __init__(self, parent):
        self.parent = parent

        # Crear menú "File"
        self.fileMenu = parent.menuBar().addMenu('File')
        self.editMenu = parent.menuBar().addMenu('Edit')
        self.buldigDegug = parent.menuBar().addMenu('Buld and Debug') #falta ver su menu desplegable
        
        # Crear acciones para el menú "File"
        self.newAct = QAction('New',parent)
        self.openAct = QAction('Open',parent)
        self.saveAsAct = QAction('Save as',parent)
        self.saveAct = QAction('Save',parent)
        
        # Conectar acciones a funciones específicas
        self.newAct.triggered.connect(self.new_file)
        self.openAct.triggered.connect(self.open_file)
        self.saveAsAct.triggered.connect(self.saveAs_file)
        self.saveAct.triggered.connect(self.save_file)
        
        # Agregar acciones al menú "File"
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.saveAct)
        
        # Crear acciones para el menú "Edit"
        self.cutAct = QAction('Cut',parent)
        self.copyAct = QAction('Copy',parent)
        self.pasteAct = QAction('Paste',parent)
        
        self.cutAct.triggered.connect(self.cut_Act)
        self.copyAct.triggered.connect(self.copy_Act)
        self.pasteAct.triggered.connect(self.paste_Act)

        # Agregar acciones al menú "Edit"
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
  
        parent.menuBar().addSeparator()
  
        self.newfileicon = QAction(QIcon(os.path.join('src','assets', 'icons', 'nuevo-documento.png')),"   ND  ",parent)
        self.openfileicon = QAction(QIcon(os.path.join('src','assets','icons','esquemacarpeta.png')),"  ABr   ",parent)
        self.savefileicon = QAction(QIcon(os.path.join('src','assets','icons','disquete.png')),"  Guar   ",parent)

        self.newfileicon.triggered.connect(self.new_fileicon)
        self.openfileicon.triggered.connect(self.open_fileicon)
        self.savefileicon.triggered.connect(self.save_fileicon)
        
        parent.menuBar().addAction(self.newfileicon)     
        parent.menuBar().addAction(self.openfileicon)
        parent.menuBar().addAction(self.savefileicon)
  ##############################
        #self.closeMenu = parent.menuBar().addMenu('Close')
        self.closeMenu = QAction("Close", parent)
        self.closeMenu.triggered.connect(self.close_Menu)
        parent.menuBar().addAction(self.closeMenu)
  
        separatorAction = QAction(parent)
        separatorAction.setSeparator(True)
        parent.menuBar().addAction(separatorAction)
  
        self.lexicalMenu = QAction('lexico',parent)
        self.syntaxMenu = QAction('sintactico',parent)
        self.semanticMenu = QAction('semantico',parent)
        self.compilerMenu = QAction("compiler",parent)
        
        self.lexicalMenu.triggered.connect(self.parent.run_lexical)
        self.syntaxMenu.triggered.connect(self.parent.run_syntax)
        self.semanticMenu.triggered.connect(self.parent.run_semantic)
        self.compilerMenu.triggered.connect(self.parent.run_code)
        
        parent.menuBar().addAction(self.lexicalMenu)
        parent.menuBar().addAction(self.syntaxMenu)
        parent.menuBar().addAction(self.semanticMenu)
        parent.menuBar().addAction(self.compilerMenu)
		


    # Definir las funciones asociadas a las acciones
    def new_file(self):
        # Implementar lógica para un nuevo archivo
        if not self.confirm_save_changes():
            return

        # Borrar el contenido del editor
        self.parent.text_editor.clear()

        # Solicitar un nuevo nombre de archivo
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save as", os.path.expanduser("~"), "Todos los archivos (*);;Archivos Python (*.py)", options=options)

        if file_name:
            # Guardar el nuevo archivo
            with open(file_name, 'w') as file:
                file.write(self.parent.text_editor.toPlainText())
            
            self.parent.current_file = file_name  # Asignar el nombre del archivo guardado
            self.parent.setWindowTitle(file_name +'- IDE Compiler GSA')  # Actualizar el título de la ventana
            self.parent.text_editor.document().setModified(False)  # Marcar como no modificado
        print("New file action")
        # *guada el archivo
        

    def open_file(self):
        # Implementar lógica para abrir un archivo
        if not self.confirm_save_changes():
            return
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open File", os.path.expanduser("~"), "All Files (*);;Python Files (*.py)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.parent.text_editor.setPlainText(content)
            self.parent.current_file = file_name  # Asignar el nombre del archivo guardado
            self.parent.setWindowTitle(file_name +'- IDE Compiler GSA')  # Actualizar el título de la ventana
            self.parent.text_editor.document().setModified(False)  # Marcar como no modificado
        print("Open file action")

    def saveAs_file(self):
        # Implementar lógica para guardar un archivo 
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save File", os.path.expanduser("~"), "All Files (*);;Python Files (*.py)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.parent.text_editor.toPlainText())
            self.parent.current_file = file_name  # Asignar el nombre del archivo guardado
            self.parent.setWindowTitle(file_name +'- IDE Compiler GSA')  # Actualizar el título de la ventana
            self.parent.text_editor.document().setModified(False)  # Marcar como no modificado
            return True
        #print("Save file action")
        return False
        
        
    def save_file(self):
        # Si ya tiene un nombre de archivo, simplemente guarda, de lo contrario, usa la lógica de "Guardar como..."
        if hasattr(self.parent, 'current_file') and self.parent.current_file:
            with open(self.parent.current_file, 'w') as file:
             file.write(self.parent.text_editor.toPlainText())
        else:
            self.saveAs_file()
        print("Save file action")
    def cut_Act(self):
        

        cursor = self.parent.text_editor.textCursor()
        selected_text = cursor.selectedText()

        if not selected_text:
            QMessageBox.information(self.parent, "Información", "No hay texto seleccionado para cortar.")
        else:
            self.parent.clipboard.setText(selected_text)
            cursor.removeSelectedText()
        
        print("Cut file action")
    def copy_Act(self):

        cursor = self.parent.text_editor.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            self.parent.clipboard.setText(selected_text)
        print("Copy action")

    def paste_Act(self):
        
        cursor = self.parent.text_editor.textCursor()
        cursor.insertText(self.parent.clipboard.text())
        print("Paste action")
    def new_fileicon(self):
        self.new_file()
        
    def open_fileicon(self):
        self.open_file()
    
    def save_fileicon(self):
        self.save_file()
    
    def close_Menu(self):
        if not self.confirm_save_changes():
            return
        self.parent.text_editor.clear()
        print("Closing menu")
        
    def confirm_save_changes(self):
        # Verificar si hay cambios no guardados
        if self.parent.text_editor.document().isModified():
            if not self.parent.current_file:  # Si no hay un archivo actual, pregunta por la ubicación para guardar
                reply = QMessageBox.question(self.parent, 'Guardar Cambios', '¿Quieres guardar los cambios?',
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

                if reply == QMessageBox.Yes:
                    return self.save_as_file()
                elif reply == QMessageBox.Cancel:
                    return False  # Cancelar la acción si el usuario elige cancelar
            else:
                reply = QMessageBox.question(self.parent, 'Guardar Cambios', f'¿Quieres guardar los cambios en {self.current_file}?',
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

                if reply == QMessageBox.Yes:
                    return self.save_file()
                elif reply == QMessageBox.Cancel:
                    return False  # Cancelar la acción si el usuario elige cancelar

        return True
