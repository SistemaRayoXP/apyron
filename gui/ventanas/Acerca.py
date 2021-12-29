# -*- coding: utf-8 -*-
"""
Ventana Acerca que contiene información sobre la aplicación y sus creadores :)
"""

import sys
import os
import PySide2

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QKeySequence, QPixmap, QBitmap

from util . Constants import *


class Acerca(QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()

    def __init__(self, parent: QWidget = None):
        super(Acerca, self).__init__(parent)
        
        if parent is not None:
            self.setParent(parent)

        # Propiedades del diálogo principal
        # ===================================
        width = (self.screen().availableSize().width() // 16) * 6
        height = (self.screen().availableSize().height() // 16) * 4
        self.resize(width, height)
        self.setModal(True)
        self.setWindowTitle(f"Acerca de {APP_NAME}")

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QtCore.QLocale.Spanish)

        # Layout para agregar widgets a la ventana
        self.dialogLayout = QVBoxLayout(self)
        
        # Agregamos los controles
        self._createControls(self)
        # self._createFooter()
        # self.centerToParent()

    def _createControls(self, parent):
        """Materias, profesores, etc"""
        # Para ajustar el tamaño de las columnas a un porcentaje
        tableWidthPercent = (self.size().width() * 1.8) // 100

        # Contenedores
        # ============

        # Página de controles
        pagina = QWidget(parent)
        paginaLayout = QHBoxLayout(pagina)

        # Widget de la imagen
        imageWidget = QWidget(pagina)
        imageLayout = QVBoxLayout(imageWidget)

        # Widget del texto
        creditsContainer = QWidget(pagina)
        creditsContainer.setMinimumWidth(400)
        creditsLayout = QVBoxLayout(creditsContainer)

        # Controles
        # =========

        # Imagen
        # ......

        imagePixmap = QPixmap(APP_ABOUTPIC_PATH)
        imageLabel = QLabel()
        imageLabel.setPixmap(imagePixmap)
        imageLabel.setMask(imagePixmap.mask())
        imageLabel.show()

        # Texto de créditos
        # .................

        lblAbout = QLabel(
            f"{APP_NAME}, por SistemaRayoXP. "
            "Derivado del código original de Apeiron. Apeiron fue "
            "desarrollado en Java originalmente por Francisco Riestra",
            creditsContainer
        )
        lblAbout.setWordWrap(True)
        lblSuppport = QLabel(
            f'Para información y soporte del proyecto, visita:<br />'
            f'<a href="{APP_WEBSITE}">{APP_WEBSITE}</a>',
            creditsContainer
        )
        lblSuppport.setWordWrap(True)
        lblSuppport.setTextFormat(QtCore.Qt.TextFormat.RichText)
        lblOriginalCredits = QLabel("\n".join([
            "Créditos originales de Apeiron (F. Riestra):",
            "        Emma: Gracias por todo...",
            "        Gerardo Flores Correa: Gracias por tu amistad ",
            "        Dulce Espinoza: Ayudó a probar el proyecto desde que era ScheduleMaker, "
            "osea 3 años atras. Tiene tanta paciencia que todavia me ayuda a probar cosas. ",
            "        Faby Galindo",
            "        Ahgue Figueroa",
            "        Anabell Saldaña",
            "        Daniel Rodríguez",
            "        Ing. Luis F. Rodríguez Acosta: Aunque no participó de manera "
            "directa, las búsquedas nunca hubieran salido sin él. ¡Es el mejor profe que "
            "he tenido en la facu!",
            "        Francisco Noriega (Bango): Gracias por los tips \n",
            "A TODOS ELLOS MIL GRACIAS!",
        ]), creditsContainer)
        lblOriginalCredits.setWordWrap(True)

        # Establecimiento de layouts
        # ==========================

        # Imagen
        # ......
        imageLayout.addWidget(imageLabel)

        # Texto de créditos
        # .................
        creditsLayout.addWidget(lblAbout)
        creditsLayout.addWidget(lblSuppport)
        creditsLayout.addWidget(lblOriginalCredits)
        creditsLayout.addStretch()

        # Página
        # ......
        paginaLayout.addWidget(imageWidget)
        paginaLayout.addWidget(creditsContainer)
        paginaLayout.setStretch(1, 300)

        self._addWidgetToScreen(pagina)

    def _createFooter(self):
        self.footer = QWidget(self)

        lblSearch = QLabel("Buscar:")
        inputSearch = QLineEdit()
        btnFilter = QPushButton("Filtrar")
        btnClear = QPushButton("Limpiar")
        btnDownload = QPushButton("Descargar")

        footerGrid = QHBoxLayout(self.footer)

        footerGrid.addStretch()
        footerGrid.addWidget(lblSearch)
        footerGrid.addWidget(inputSearch)
        footerGrid.addWidget(btnFilter)
        footerGrid.addWidget(btnClear)
        footerGrid.addWidget(btnDownload)
        footerGrid.addStretch()

        self.footer.setLayout(footerGrid)

        self._addWidgetToScreen(self.footer)

    def _addWidgetToScreen(self, widget: QWidget):
        self.dialogLayout.addWidget(widget)
        self.setLayout(self.dialogLayout)

    def centerToParent(self):
        parentX = self.parent().x() + (self.parent().width() // 2)
        parentY = self.parent().y() + (self.parent().height() // 2)
        newX = parentX - (self.width() // 2)
        newY = parentY - (self.height() // 2)
        self.move(newX, newY)


def main():
    app = QApplication(sys.argv)
    form = Acerca()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
