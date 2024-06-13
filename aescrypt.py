# -*- coding: utf-8 -*-
import os
import sys
import pyAesCrypt
from PyQt5 import QtWidgets, QtGui, QtCore

class Form(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setFont(QtGui.QFont('Arial', 14))
        self.plainTextEdit.appendHtml("<br>Добро пожаловать!<br><br>Выберите, что вы хотите сделать:<br>")

        crypt = QtWidgets.QPushButton("Зашифровать")
        crypt.clicked.connect(self.crypt)

        decrypt = QtWidgets.QPushButton("Расшифровать")
        decrypt.clicked.connect(self.decrypt)

        layoutV = QtWidgets.QVBoxLayout()
        layoutV.addWidget(crypt)
        layoutV.addWidget(decrypt)

        layoutH = QtWidgets.QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)

        centerWidget = QtWidgets.QWidget()
        centerWidget.setLayout(layoutH)
        self.setCentralWidget(centerWidget)

        self.resize(740, 480)
        self.setWindowTitle("WinRestore")

    def crypt(self):
        try:
            filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "All Files(*)")
            if filename:
                password, okPressed = QtWidgets.QInputDialog.getText(self, "Введите пароль", "Введите пароль:", QtWidgets.QLineEdit.Password, "")
                if okPressed and password:
                    bufferSize = 512 * 1024
                    pyAesCrypt.encryptFile(filename, filename + ".aes", password, bufferSize)
                    os.remove(filename)
                    self.plainTextEdit.appendHtml(f"<br>Файл зашифрован: {filename}")
                else:
                    self.plainTextEdit.appendHtml("<br>Ошибка! Проверьте пароль!<br>")
            else:
                self.plainTextEdit.appendHtml("<br>Ошибка! Выберите файл!<br>")
        except Exception as e:
            self.plainTextEdit.appendHtml("<br>Ошибка! Проверьте пароль!<br>")
            print(f"Error: {e}")

    def decrypt(self):
        try:
            filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "All Files(*)")
            if filename:
                password, okPressed = QtWidgets.QInputDialog.getText(self, "Введите пароль", "Введите пароль:", QtWidgets.QLineEdit.Password, "")
                if okPressed and password:
                    bufferSize = 512 * 1024
                    pyAesCrypt.decryptFile(filename, os.path.splitext(filename)[0], password, bufferSize)
                    os.remove(filename)
                    self.plainTextEdit.appendHtml(f"<br>Файл расшифрован: {filename}")
                else:
                    self.plainTextEdit.appendHtml("<br>Ошибка! Проверьте пароль!<br>")
            else:
                self.plainTextEdit.appendHtml("<br>Ошибка! Выберите файл!<br>")
        except Exception as e:
            self.plainTextEdit.appendHtml("<br>Ошибка! Проверьте пароль!<br>")
            print(f"Error: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())