# -*- coding: utf-8 -*-
"""
Ventana Descargas para administrar las descargas de materias
"""

import sys
import os
import time
import PySide2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QKeySequence, QPixmap

from carga.LectorSiiau import LectorSiiau
from carga.MateriaSiiau import MateriaSiiau


class Descargas(QtWidgets.QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()
    lectorSiiau = None

    def __init__(self, lectorSiiau: LectorSiiau, parent: QWidget = None):
        super(Descargas, self).__init__(parent)

        if parent is not None:
            self.setParent(parent)

        self.lectorSiiau = lectorSiiau

        # Layout del diálogo
        self.dialogLayout = QVBoxLayout(self)

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QtCore.QLocale.Spanish)

        # Generador de los controles
        self._createControls()

        # Propiedades del diálogo
        # ===================================
        self.setWindowTitle("Descargas")
        width = (self.screen().availableSize().width() // 16) * 3
        height = (self.screen().availableSize().height() // 16) * 6
        self.resize(width, height)

    def _createControls(self):
        """Caja de descarga"""
        # Área/widget de descargas
        self.downloadsWidget = QWidget(self)
        # Layout del área de descargas
        self.downloadsLayout = QVBoxLayout(self.downloadsWidget)
        # Contenedor de los controles de pie de diálogo
        self.footer = QWidget(self)

        # Controles del pie de diálogo
        btnClear = QPushButton("Limpiar")
        btnClose = QPushButton("Cerrar")

        # Layout del pie de diálogo
        footerLayout = QHBoxLayout(self.footer)
        footerLayout.addStretch()
        footerLayout.addWidget(btnClear)
        footerLayout.addWidget(btnClose)
        footerLayout.addStretch()

        # Establecemos el layout del pie
        self.footer.setLayout(footerLayout)

        # Agregamos los widgets al layout del diálogo
        self.dialogLayout.addWidget(self.downloadsWidget)
        self.dialogLayout.addStretch()
        self.dialogLayout.addWidget(self.footer)

        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")
        self.addDownload("IL352")

    def addDownload(self, details: str):
        """Elemento de descarga"""
        downloadItem = QWidget(self.downloadsWidget)

        lblDetails = QLabel(f"Descargando {details}")
        downloadProgress = QProgressBar(downloadItem)
        btnCancel = QPushButton("Cancelar")

        itemLayout = QGridLayout(downloadItem)
        itemLayout.addWidget(lblDetails, 0, 0, 1, 2)
        itemLayout.addWidget(downloadProgress, 1, 0, 1, 2)
        itemLayout.addWidget(btnCancel, 2, 1, 1, 1, QtCore.Qt.AlignRight)

        self.downloadsLayout.addWidget(downloadItem)

    def moveCenter(self):
        screenSize = self.screen().size()
        newX = (screenSize.width() - self.size().width()) // 2
        newY = (screenSize.height() - self.size().height()) // 2
        self.move(newX, newY)


def main():
    app = QApplication(sys.argv)

    form = Descargas()
    form.moveCenter()
    form.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

