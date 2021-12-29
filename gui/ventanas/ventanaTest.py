# -*- coding: utf-8 -*-
"""
Ventana de prueba para probar Qt
"""

import sys
import os
import time
import PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QAction
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PySide2.QtWidgets import QWidget, QTabWidget, QListWidget, QSplitter
from PySide2.QtWidgets import QComboBox, QGroupBox
from PySide2.QtWidgets import QPushButton, QLineEdit, QLabel
from PySide2.QtGui import QFont, QIcon, QKeySequence, QPixmap

lista_centros = [
    'CICLO DE VERANO',
    'CUAAD',
    'CUALTOS',
    'CUALTOS NORTE',
    'CUCBA',
    'CUCEA',
    'CUCEA VALLES',
    'CUCEI',
    'CUCEI NORTE',
    'CUCEI VALLES',
    'CUCIENEGA',
    'CUCOSTA NORTE',
    'CUCOSTA',
    'CUCS',
    'CUCSH',
    'CUCSUR',
    'CUCSUR VALLES',
    'CULAGOS',
    'CUNORTE',
    'CUSUR',
    'CUTLAJOMULCO',
    'CUTONALA',
    'CUVALLES',
    'INCORPORADAS',
    'TLAJOMULCO',
    'UDGVIRTUAL',
]


class VentanaPrincipal(QtWidgets.QMainWindow):
    null_icon = QIcon()
    applicationIcon = QIcon()

    def __init__(self):
        super(VentanaPrincipal, self).__init__()

        # Definición inicial de Widgets
        # =============================

        # Widget principal que ocupará el área de cliente
        self.windowWidget = QWidget(self)
        self.windowWidgetLayout = QGridLayout(self.windowWidget)

        # Widget de tabulación que contendrá la mayoría de la interfaz
        self.tabWidget = QTabWidget(self)

        tab1 = self._getTab(0)
        tab2 = self._getTab(1)
        tab3 = self._getTab(2)

        # Adición de páginas
        # ==================
        self.tabWidget.addTab(
            tab1, self.null_icon, "Materias, profesores y grupos")
        self.tabWidget.addTab(
            tab2, self.null_icon, "Horario del estudiante")
        self.tabWidget.addTab(
            tab3, self.null_icon, "Preferencias de generación")

        # Adición de widgets a la ventana
        # ===============================
        self._addWidgetToScreen(self.tabWidget)

        # Propiedades de la ventana principal
        # ===================================
        width = (self.screen().availableSize().width() // 8) * 5
        height = (self.screen().availableSize().height() // 8) * 5
        self.resize(width, height)
        self.setCentralWidget(self.windowWidget)
        self.setWindowTitle("Apeiron 3.0")
        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QtCore.QLocale.Spanish)
        self._createMenus()
        self._createFooter()

    def _createMenus(self):
        # Menú Archivo
        # ============

        menuFile = self.menuBar().addMenu("&Archivo")

        menuFileUpdate = QAction(
            QIcon.fromTheme("update"),
            "Buscar act&ualizaciones",
            self,
        )
        menuFile.addAction(menuFileUpdate)

        menuFileExit = QAction(
            QIcon.fromTheme("application-exit"),
            "&Salir",
            self,
            shortcut="Ctrl+X",
            triggered=QApplication.quit,
        )
        menuFile.addAction(menuFileExit)

        # Menú Horario
        # ============

        menuSchedule = self.menuBar().addMenu("Horario")

        menuScheduleChooseSubjects = QAction(
            QIcon.fromTheme("schedule"),
            "Seleccionar materias",
            self,
        )
        menuSchedule.addAction(menuScheduleChooseSubjects)

        menuScheduleGenPrefs = QAction(
            QIcon.fromTheme("settings"),
            "Configurar generación",
            self,
        )
        menuSchedule.addAction(menuScheduleGenPrefs)

        menuScheduleGenerate = QAction(
            QIcon.fromTheme("application-update"),
            "Generar horarios",
            self,
        )
        menuSchedule.addAction(menuScheduleGenerate)

        menuSchedule.addSeparator()

        menuScheduleGenerate = QAction(
            QIcon.fromTheme("download"),
            "Administrador de descargas",
            self,
        )
        menuSchedule.addAction(menuScheduleGenerate)

        # Menú Ayuda
        # ==========

        menuHelp = self.menuBar().addMenu("Ayuda")

        menuHelpContents = QAction(
            QIcon.fromTheme("help"),
            "Guía para configurar los horarios",
            self,
            shortcut=QKeySequence(QKeySequence.HelpContents),
        )
        menuHelp.addAction(menuHelpContents)

        menuHelp.addSeparator()

        menuHelpAboutQt = QAction(
            QIcon.fromTheme("application-about"),
            "Acerca de Qt",
            self,
            triggered=QApplication.aboutQt,
        )
        menuHelp.addAction(menuHelpAboutQt)

        menuHelp.addSeparator()

        menuHelpAbout = QAction(
            QIcon.fromTheme("application-about"),
            "Acerca de esta aplicación",
            self,
        )
        menuHelp.addAction(menuHelpAbout)

    def _getTab(self, n: int):
        def tab1():
            """Materias, profesores, etc"""
            pagina = QSplitter(self)
            pagina.setOrientation(QtCore.Qt.Orientation.Vertical)

            # Para ajustar el tamaño de las columnas a un porcentaje
            tableWidthPercent = (self.size().width() * 1.8) // 100

            # Grupo Materias
            # ==============

            groupSubjects = QGroupBox("Materias")

            listSubjects = QListWidget()
            subjects = [
                QtWidgets.QListWidgetItem("FUNDAMENTOS DE PROGRAMACION"),
                QtWidgets.QListWidgetItem("PROGRAMACION ESTRUCTURADA"),
                QtWidgets.QListWidgetItem("PROGRAMACION ORIENTADA A OBJETOS"),
            ]

            for item in subjects:
                item.setCheckState(QtCore.Qt.Unchecked)
                listSubjects.addItem(item)

            btnCatalogo = QPushButton("Catálogo")
            btnAddByKey = QPushButton("Añadir por clave")
            btnRemove = QPushButton("Quitar")
            btnUpdateSubjects = QPushButton("Actualizar materias")

            actionsWidget = QWidget(groupSubjects)
            actionsHbox = QHBoxLayout(actionsWidget)
            actionsHbox.addStretch()
            actionsHbox.addWidget(btnCatalogo)
            actionsHbox.addWidget(btnAddByKey)
            actionsHbox.addWidget(btnRemove)
            actionsHbox.addWidget(btnUpdateSubjects)
            actionsWidget.setLayout(actionsHbox)

            vboxSubjects = QVBoxLayout(groupSubjects)
            vboxSubjects.addWidget(listSubjects)
            vboxSubjects.addWidget(actionsWidget)

            groupSubjects.setLayout(vboxSubjects)

            # Grupo Profesores
            # ================

            groupProfessors = QGroupBox("Profesores")

            lstProfessors = QListWidget()
            professors = [
                QtWidgets.QListWidgetItem("CRUZ GOMEZ, CONRADO"),
                QtWidgets.QListWidgetItem("ESQUIVEL TORRES, SARA"),
                QtWidgets.QListWidgetItem("MARTINEZ SOLTERO, ERASMO GABRIEL"),
                QtWidgets.QListWidgetItem("VEGA MALDONADO; SABRINA LIZBETH"),
            ]

            for item in professors:
                item.setCheckState(QtCore.Qt.Unchecked)
                lstProfessors.addItem(item)

            vboxProfessors = QVBoxLayout(groupProfessors)
            vboxProfessors.addWidget(lstProfessors)

            groupProfessors.setLayout(vboxProfessors)

            # Grupo Grupos
            # ============

            groupClasses = QGroupBox("Grupos")

            lstClasses = QtWidgets.QTableView(groupClasses)
            modelClasses = QtGui.QStandardItemModel(1, 2)

            modelClasses.setItem(0, 0, QtGui.QStandardItem("123456"))
            modelClasses.setItem(0, 1, QtGui.QStandardItem("D04"))
            modelClasses.setItem(0, 2, QtGui.QStandardItem("20"))
            modelClasses.setItem(0, 3, QtGui.QStandardItem("3"))
            modelClasses.setItem(0, 4, QtGui.QStandardItem(
                "Lunes 12:00-13:55 - Miércoles 12:00-13:55"))
            modelClasses.setItem(
                0, 5, QtGui.QStandardItem("16/01/2022 - 17/05/2022"))

            modelClasses.setHorizontalHeaderLabels([
                "NRC",
                "Sección",
                "Cupo",
                "Disponible",
                "Horario",
                "Periodo",
            ])
            lstClasses.setModel(modelClasses)
            lstClasses.setColumnWidth(4, tableWidthPercent * 30)
            lstClasses.setColumnWidth(5, tableWidthPercent * 20)

            vboxClasses = QVBoxLayout(groupClasses)
            vboxClasses.addWidget(lstClasses)

            groupClasses.setLayout(vboxClasses)

            # Adición de los widgets a la pestaña
            # ===================================

            pagina.addWidget(groupSubjects)
            pagina.addWidget(groupProfessors)
            pagina.addWidget(groupClasses)

            return pagina

        def tab2():
            """Horario preferido"""

            pagina = QWidget(self)

            btnMatutino = QPushButton("Mañana", pagina)
            btnVerspertino = QPushButton("Tarde", pagina)
            btnTodas = QPushButton("Todas", pagina)
            btnNinguna = QPushButton("Ninguna", pagina)
            btnClonar = QPushButton("Clonar selección", pagina)
            lblDia = QLabel("Día:", pagina)
            cmbDia = QComboBox(pagina)
            lblHorasDisp = QLabel("Horas para tomar clase:", pagina)

            chksHoras = {
                "700": QtWidgets.QCheckBox("7:00 am"),
                "800": QtWidgets.QCheckBox("8:00 am"),
                "900": QtWidgets.QCheckBox("9:00 am"),
                "1000": QtWidgets.QCheckBox("10:00 am"),
                "1100": QtWidgets.QCheckBox("11:00 am"),
                "1200": QtWidgets.QCheckBox("12:00 pm"),
                "1300": QtWidgets.QCheckBox("1:00 pm"),
                "1400": QtWidgets.QCheckBox("2:00 pm"),
                "1500": QtWidgets.QCheckBox("3:00 pm"),
                "1600": QtWidgets.QCheckBox("4:00 pm"),
                "1700": QtWidgets.QCheckBox("5:00 pm"),
                "1800": QtWidgets.QCheckBox("6:00 pm"),
                "1900": QtWidgets.QCheckBox("7:00 pm"),
                "2000": QtWidgets.QCheckBox("8:00 pm"),
                "2100": QtWidgets.QCheckBox("9:00 pm"),
            }

            cmbDia.insertItems(0, [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
            ])
            lstHoras = [
                "7:00 am",
                "8:00 am",
                "9:00 am",
                "10:00 am",
                "11:00 am",
                "12:00 pm",
                "1:00 pm",
                "2:00 pm",
                "3:00 pm",
                "4:00 pm",
                "5:00 pm",
                "6:00 pm",
                "7:00 pm",
                "8:00 pm",
                "9:00 pm",
            ]

            # Filas de la página 2
            # ====================

            filaBotones = QWidget()
            hboxBotones = QHBoxLayout()
            hboxBotones.addStretch()
            hboxBotones.addWidget(btnMatutino)
            hboxBotones.addWidget(btnVerspertino)
            hboxBotones.addWidget(btnTodas)
            hboxBotones.addWidget(btnNinguna)
            hboxBotones.addWidget(btnClonar)
            hboxBotones.addWidget(lblDia, alignment=QtGui.Qt.AlignRight)
            hboxBotones.addWidget(cmbDia)
            filaBotones.setLayout(hboxBotones)

            listaLayout = QVBoxLayout(pagina)
            listaLayout.addWidget(filaBotones)
            listaLayout.addWidget(lblHorasDisp)

            for key, chk in list(chksHoras.items()):
                if isinstance(chk, QtWidgets.QCheckBox):
                    chk.setChecked(True)
                    listaLayout.addWidget(chk)

            listaLayout.addStretch()

            pagina.setLayout(listaLayout)

            return pagina

        def tab3():
            """Preferencias, aunque me gustaría cambiarlo"""

            pagina = QWidget(self)

            lblMaxAGenerar = QLabel("Número máximo de horarios a generar:")
            MaxAGenerar = QLineEdit("50000")

            lblHuecos = QLabel("Huecos permisibles:")
            HuecosPerm = QLineEdit("2")

            lblHuecosInter = QLabel("Huecos intermedios permisibles:")
            HuecosInterPerm = QLineEdit("-1")

            lblHuecosAyuda = QLabel("-1 significa infinito")
            lblHuecosAyuda.setAlignment(QtCore.Qt.AlignRight)
            lblHuecosAyuda.setStyleSheet("QLabel { color: blue; }")

            lblOrdenAyuda = QLabel(
                "Coloca números entre -2 y 2, donde un nº positivo significa"
                "de menor a mayor y un nº negativo es de mayor a menor"
            )
            lblOrdenAyuda.setStyleSheet("QLabel { color: blue; }")

            SoloConCupo = QtWidgets.QCheckBox(
                "Solo considerar grupos con cupo")
            MateriasEspejo = QtWidgets.QCheckBox(
                "Tomar periodos en cuenta (materias espejo)")

            lblHora = QLabel("Hora del día:")
            PrioriHora = QLineEdit("2")

            lblDemanda = QLabel("Demanda:")
            PrioriDemanda = QLineEdit("-1")

            # Widgets de la página 3
            # ======================

            gboxGeneral = QtWidgets.QGroupBox("General", pagina)
            gridGeneral = QGridLayout(pagina)
            gridGeneral.addWidget(lblMaxAGenerar, 0, 0)
            gridGeneral.addWidget(MaxAGenerar, 0, 1)
            gridGeneral.addWidget(lblHuecos, 1, 0)
            gridGeneral.addWidget(HuecosPerm, 1, 1)
            gridGeneral.addWidget(lblHuecosInter, 2, 0)
            gridGeneral.addWidget(HuecosInterPerm, 2, 1)
            gridGeneral.addWidget(lblHuecosAyuda, 3, 1, QtGui.Qt.AlignLeft)
            gridGeneral.addWidget(SoloConCupo, 4, 0, QtGui.Qt.AlignTop)
            gridGeneral.addWidget(MateriasEspejo, 5, 0, QtGui.Qt.AlignTop)
            gboxGeneral.setLayout(gridGeneral)

            gboxOrden = QtWidgets.QGroupBox("Orden de los grupos", pagina)
            gridOrden = QGridLayout(pagina)
            gridOrden.addWidget(lblOrdenAyuda, 0, 0, 1, 2)
            gridOrden.addWidget(lblHora, 1, 0)
            gridOrden.addWidget(PrioriHora, 1, 1)
            gridOrden.addWidget(lblDemanda, 2, 0, -1, 1, QtGui.Qt.AlignTop)
            gridOrden.addWidget(PrioriDemanda, 2, 1, -1, 1, QtGui.Qt.AlignTop)
            gboxOrden.setLayout(gridOrden)

            # Intento de arreglo por conflicto con el espaciado
            listaLayout = QVBoxLayout(pagina)
            listaLayout.addWidget(gboxGeneral)
            listaLayout.addWidget(gboxOrden)
            listaLayout.addStretch()

            pagina.setLayout(listaLayout)

            return pagina

        tabs = {
            0: tab1(),
            1: tab2(),
            2: tab3(),
        }

        return tabs.get(n)

    def _createFooter(self):
        self.footer = QWidget(self)

        btnExport = QPushButton("Exportar")
        btnImport = QPushButton("Importar")
        btnSearchSchedule = QPushButton("Buscar horario")
        btnClose = QPushButton("Cerrar")
        btnClose.clicked.connect(QApplication.quit)

        footerGrid = QHBoxLayout(self.footer)

        footerGrid.addStretch()
        footerGrid.addWidget(btnExport)
        footerGrid.addWidget(btnImport)
        footerGrid.addWidget(btnSearchSchedule)
        footerGrid.addWidget(btnClose)

        self.footer.setLayout(footerGrid)

        self._addWidgetToScreen(self.footer)

    def _addWidgetToScreen(self, widget: QWidget):
        self.windowWidgetLayout.addWidget(widget)
        self.windowWidget.setLayout(self.windowWidgetLayout)

    def actionPerformed(self, e):
        # TODO Auto-generated method stub
        tmp = self.centro.getSelectedItem()

        self.datos.cargar(MateriaSiiau(
            clave.getText(), tmp.clave, ciclo.getText()))
        # btnGo.setEnabled(false);

    def moveCenter(self):
        screenSize = self.screen().size()
        newX = (screenSize.width() - self.size().width()) // 2
        newY = (screenSize.height() - self.size().height()) // 2
        self.move(newX, newY)


def main():
    app = QApplication(sys.argv)
    splashimage = QPixmap(os.path.join(":/recursos/apeiron.jpg"))
    splash = QtWidgets.QSplashScreen(splashimage)
    splash.show()

    form = VentanaPrincipal()
    form.moveCenter()
    form.show()

    splash.finish(form)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
