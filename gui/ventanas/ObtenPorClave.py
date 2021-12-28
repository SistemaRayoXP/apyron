# -*- coding: utf-8 -*-
"""
Ventana ObtenPorClave para obtener una materia por su clave

Es más una comodidad que utilidad, ya que en la versión final
las materias SIEMPRE estarán actualizadas, porque se obtendrán
directamente desde SIIAU cada vez que se inicie la aplicación.
"""

import sys
import os
import time
import PySide2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QKeySequence, QPixmap

from carga.AdDatos import AdDatos
from carga.MateriaSiiau import MateriaSiiau
from gui.clases.ControlCollection import ControlCollection
from util.DatosPersistentes import DatosPersistentes


class ObtenPorClave(QtWidgets.QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()
    datos = None
    controls = ControlCollection()
    lectorCatalogo = DatosPersistentes()
    centros = lectorCatalogo.obtenerCentros()
    calendarios = lectorCatalogo.obtenerCalendarios()

    def __init__(self, datos: AdDatos, parent: QWidget = None):
        super(ObtenPorClave, self).__init__(parent)

        if parent is not None:
            self.setParent(parent)

        # Propiedades de la ventana principal
        # ===================================
        width = (self.screen().availableSize().width() // 16) * 4
        height = (self.screen().availableSize().height() // 16) * 2
        self.dialogLayout = QVBoxLayout(self)
        self.resize(width, height)
        self.setWindowTitle("Descarga por clave")

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QtCore.QLocale.Spanish)

        # Creamos los controles
        self._createControls(parent)

        # Y centramos respecto al padre
        self.centerToParent()

    def _createControls(self, parent):
        """Controles principales de la aplicación"""
        # Contenedores
        self.controls.pagina = QWidget(self)
        self.controls.paginaLayout = QVBoxLayout(self.controls.pagina)
        self.controls.rowWidget = QWidget(self.controls.pagina)
        self.controls.rowLayout = QHBoxLayout(self.controls.rowWidget)

        # Controles

        self.controls.cmbUniversity = QComboBox(self.controls.pagina)
        self.controls.cmbCalendar = QComboBox(self.controls.pagina)
        self.controls.lblHelp = QLabel(
            "Separa las claves con comas o espacios", self.controls.pagina)

        self.controls.lblKeys = QLabel("Claves:", self.controls.rowWidget)
        self.controls.inputClaves = QLineEdit(self.controls.rowWidget)
        self.controls.btnDownload = QPushButton(
            "Descargar", self.controls.rowWidget)
        self.controls.btnDownload.clicked.connect(self._downloadSubjects)

        # Procesos

        for c in self.centros:
            self.controls.cmbUniversity.addItem(str(c), c)

        for c in self.calendarios:
            self.controls.cmbCalendar.addItem(str(c), c)

        # Adición a layouts

        self.controls.rowLayout.addWidget(self.controls.lblKeys)
        self.controls.rowLayout.addWidget(self.controls.inputClaves)
        self.controls.rowLayout.addWidget(self.controls.btnDownload)

        self.controls.paginaLayout.addWidget(self.controls.cmbUniversity)
        self.controls.paginaLayout.addWidget(self.controls.cmbCalendar)
        self.controls.paginaLayout.addWidget(self.controls.lblHelp)
        self.controls.paginaLayout.addWidget(self.controls.rowWidget)
        self.controls.paginaLayout.addStretch()

        self._addWidgetToScreen(self.controls.pagina)

    def _addWidgetToScreen(self, widget: QWidget):
        self.dialogLayout.addWidget(widget)
        self.setLayout(self.dialogLayout)

    def _procesarClaves(self):
        entrada = self.controls.inputClaves.text()
        claves = []
        tmp = ""

        for c in entrada:
            # Si es un separador, verificamos si ya recolectamos una clave
            if c in [" ", ","]:
                # Si hay caracteres en tmp, agregamos la clave y reiniciamos
                if tmp:
                    claves.append(tmp)
                    tmp = ""
            # Si no es separador, agregamos el carácter y seguimos
            else:
                tmp += c

        # Agregamos la clave que haya podido quedado en tmp
        if tmp:
            claves.append(tmp)

        return claves

    def _downloadSubjects(self):
        centroData = self.controls.cmbUniversity.itemData(
            self.controls.cmbUniversity.currentIndex())
        calData = self.controls.cmbCalendar.itemData(
            self.controls.cmbCalendar.currentIndex())

        claves = self._procesarClaves()
        centro = centroData.obtenerClave()
        calendario = calData.obtenerClave()

        self.close()
        self.parent().agregarMateria(claves, centro, calendario)

    def centerToParent(self):
        parentX = self.parent().x() + (self.parent().width() // 2)
        parentY = self.parent().y() + (self.parent().height() // 2)
        newX = parentX - (self.width() // 2)
        newY = parentY - (self.height() // 2)
        self.move(newX, newY)
