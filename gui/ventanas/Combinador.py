# -*- coding: utf-8 -*-
"""
Módulo de la ventana de combinaciones
"""

import random

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtGui import QKeySequence, QStandardItem, QStandardItemModel
from PySide2.QtCore import Qt, Slot, QLocale, QItemSelectionModel
from carga.AdDatos import AdDatos

from combinacion.PrimeroElMejor import PrimeroElMejor
from util.Constants import *

# IL352 IL340 IL341 IG738 I5247


class Combinador(QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()
    datos = None
    modcomb = None

    def __init__(self, parent=None, datos: AdDatos=None):
        super(Combinador, self).__init__(parent)

        if datos is not None:
            self.datos = datos

        self.modcomb = PrimeroElMejor(self.datos)

        # Propiedades de la ventana principal
        # ===================================
        width = 800
        height = 600
        self.resize(width, height)
        self.setWindowTitle("Combinador de horarios")

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QLocale.Spanish)

        # Layout del diálogo
        self.dialogLayout = QVBoxLayout(self)

        self._createControls(self)
        self._createFooter()
        self._updatePreview()
        self._updateDetails()

        self.modcomb.run()
        self._cargarSoluciones()

    def _createControls(self, parent):
        """Genera los controles principales de la ventana"""
        # Contenedores
        # ============

        # Widget principal
        self.pagina = QSplitter(parent)
        self.pagina.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Donde se muestra el horario
        self.schedule = QSplitter(self.pagina)
        self.schedule.setOrientation(Qt.Orientation.Vertical)

        # Controles
        # =========

        # Lista/selector de combinaciones
        # ...............................

        self.listCombinations = QListWidget(self.pagina)
        self.listCombinations.setMaximumWidth(100)
        # TODO: self.actualHorarioCambio()
        # self.listCombinations.currentItemChanged.connect(self.actualHorarioCambio)

        for x in range(20):
            self.listCombinations.addItem(str(x + 1))

        # Vista previa del horario
        # ........................

        self.schedulePreview = QTableView(self.schedule)
        self.schedulePreview.setTabKeyNavigation(False)
        self.modelPreview = QStandardItemModel(15, 6, self.schedulePreview)

        # Detalles del horario seleccionado
        # .................................

        self.scheduleDetails = QTableView(self.schedule)
        self.scheduleDetails.setTabKeyNavigation(False)
        self.modelDetails = QStandardItemModel(0, 6, self.scheduleDetails)

        # Distibución de controles en los widgets
        # =======================================

        self.schedule.addWidget(self.schedulePreview)
        self.schedule.addWidget(self.scheduleDetails)

        self.pagina.addWidget(self.listCombinations)
        self.pagina.addWidget(self.schedule)

        self._addWidgetToScreen(self.pagina)

    def _createFooter(self):
        """Genera el pie de la ventana"""
        self.footer = QWidget(self)
        self.footerGrid = QHBoxLayout(self.footer)

        self.btnPrint = QPushButton("Imprimir", self.footer)
        self.btnClose = QPushButton("Cerrar", self.footer)

        # self.btnPrint.clicked.connect(self.imprimirHorario)
        self.btnClose.clicked.connect(self.close)

        self.footerGrid.addStretch()
        self.footerGrid.addWidget(self.btnPrint)
        self.footerGrid.addWidget(self.btnClose)

        self._addWidgetToScreen(self.footer)

    def _addWidgetToScreen(self, widget: QWidget):
        self.dialogLayout.addWidget(widget)
        self.setLayout(self.dialogLayout)

    def _cargarSoluciones(self):
        print("_cargarSoluciones")
        print(self.modcomb.getSolCount())
        print(self.modcomb.arrSol)

    def _updatePreview(self):
        self.modelPreview.clear()
        self.modelPreview.setHorizontalHeaderLabels([
            "Lunes", "Martes", "Miércoles",
            "Jueves", "Viernes", "Sábado",
        ])
        self.modelPreview.setVerticalHeaderLabels([
            "7:00 am",  "8:00 am", "9:00 am", "10:00 am",
            "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm",
            "3:00 pm",  "4:00 pm", "5:00 pm", "6:00 pm",
            "7:00 pm",  "8:00 pm", "9:00 pm",
        ])

        for row in range(15):
            for column in range(6):
                texto = random.choice([
                    "", "", "", "IL352", "IL340", "IL341", "IG738", "I5247"
                ])
                color = random.choice([
                    "red", "blue", "green", "yellow", "orange", "magenta",
                    "cyan", "black", "gray", "brown", "purple"
                ])
                foreground = QtGui.QBrush(QtGui.QColor(color))
                item = QStandardItem(texto)
                item.setForeground(foreground)
                item.setFont(QtGui.QFont("Helvetica", pointSize=10, weight=QtGui.QFont.Black, italic=True))
                item.setEditable(False)
                self.modelPreview.setItem(row, column, item)

        self.schedulePreview.setModel(self.modelPreview)

    # TODO: Quitar el =None, siempre se debe pasar un parámetro
    def _updateDetails(self, grupo=None):
        self.modelDetails.clear()
        self.modelDetails.setHorizontalHeaderLabels([
            "NRC", "Clave", "Materia", "Profesor",
            "Cupo", "Sección", "Periodo",
        ])

        for x in range(5):
            self.modelDetails.appendRow([
                QStandardItem("189660"),
                QStandardItem("IG738"),
                QStandardItem("PRECALCULO"),
                QStandardItem("JOSE SOLIS ROGRIGUEZ"),
                QStandardItem("8/20"),
                QStandardItem("D05"),
                QStandardItem("16/01/22 - 15/07/22"),
            ])

        self.scheduleDetails.setModel(self.modelDetails)
