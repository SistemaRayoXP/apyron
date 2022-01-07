# -*- coding: utf-8 -*-
"""
Ventana Principal de la aplicación
"""

from collections import OrderedDict as odict

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtGui import QKeySequence, QStandardItem, QStandardItemModel
from PySide2.QtCore import Qt, Slot, QLocale, QItemSelectionModel

from util.Constants import *
from gui.ventanas import Acerca, Catalogo, ObtenPorClave, Descargas, Combinador
from gui.clases.ControlCollection import ControlCollection
from carga.AdDatos import AdDatos
from carga.Horario import Horario
from carga.MateriaSiiau import MateriaSiiau


class Principal(QMainWindow):
    null_icon = QIcon()
    applicationIcon = QIcon()
    datos = AdDatos()
    diasString = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

    # Hacemos una lista de horas (identificadores)
    horas = odict({
        "7:00 am":  True,  "8:00 am": True, "9:00 am": True, "10:00 am": True,
        "11:00 am": True, "12:00 pm": True, "1:00 pm": True, "2:00 pm":  True,
        "3:00 pm":  True,  "4:00 pm": True, "5:00 pm": True, "6:00 pm":  True,
        "7:00 pm":  True,  "8:00 pm": True, "9:00 pm": True,
    })
    # Y asignamos las horas a los [6] días
    dias = [
        horas.copy(), horas.copy(), horas.copy(),
        horas.copy(), horas.copy(), horas.copy()
    ]

    def __init__(self):
        super(Principal, self).__init__()

        # Definición inicial de Widgets
        # =============================

        # Widget principal que ocupará el área de cliente
        self.windowWidget = QWidget(self)
        self.windowLayout = QGridLayout(self.windowWidget)

        # Propiedades de la ventana principal
        width = (self.screen().availableSize().width() // 8) * 5
        height = (self.screen().availableSize().height() // 8) * 5
        self.applicationIcon = QIcon(APP_ICON_PATH)
        self.resize(780, 550)
        self.setCentralWidget(self.windowWidget)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(self.applicationIcon)

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QLocale.Spanish)

        # Añadimos los controles al formulario al final
        self._createMenus()
        self._addTabs()
        self._createFooter()

        # TODO: Arreglar el estilo oscuro en Win32 y X11
        self._setPlatformStyle()

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
            triggered=self._showDialogDescargas,
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
            # triggered=self._ayuda,
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
            f"Acerca de {APP_NAME}",
            self,
            triggered=self._showDialogAbout
        )
        menuHelp.addAction(menuHelpAbout)

    def _addTabs(self):
        # Widget de tabulación que contendrá la mayoría de la interfaz
        self.tabWidget = QTabWidget(self.windowWidget)

        tab1 = self._getTab(0, self.tabWidget)
        tab2 = self._getTab(1, self.tabWidget)
        tab3 = self._getTab(2, self.tabWidget)

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

    def _getTab(self, n: int, parent):
        """
        Devuelve una página de la interfaz
        """
        # Materias, profesores, etc
        if n == 0:
            # Contenedores
            # ============

            pagina = QSplitter(parent)
            pagina.setOrientation(Qt.Orientation.Vertical)

            # Grupo de materias
            groupSubjects = QGroupBox("Materias", pagina)
            # Layout del grupo
            layoutSubjects = QVBoxLayout(groupSubjects)
            # Fila de controles del grupo
            actionsSubjects = QWidget(groupSubjects)
            # Layout de la fila de controles
            actionsLSubjects = QHBoxLayout(actionsSubjects)

            # Grupo de profesores
            groupProfessors = QGroupBox("Profesores", pagina)
            # Layout del grupo
            layoutProfessors = QVBoxLayout(groupProfessors)

            # Grupo de horarios
            groupSchedules = QGroupBox("Grupos", pagina)
            # Layout del grupo
            layoutSchedules = QVBoxLayout(groupSchedules)

            # Controles
            # =========

            # Materias
            # ........

            self.listSubjects = QListWidget(groupSubjects)
            self.listSubjects.currentItemChanged.connect(
                self.actualMateriaCambio)

            btnCatalogo = QPushButton("Catálogo", actionsSubjects)
            btnCatalogo.clicked.connect(self._showDialogCatalogo)
            btnAddByKey = QPushButton("Añadir por clave", actionsSubjects)
            btnAddByKey.clicked.connect(self._showDialogObtenPorClave)
            btnRemove = QPushButton("Quitar", actionsSubjects)
            btnRemove.clicked.connect(self.eliminarMateria)
            btnUpdateSubjects = QPushButton(
                "Actualizar materias", actionsSubjects)
            # btnUpdateSubjects.clicked.connect(self.)

            # Profesores
            # ..........

            self.listProfessors = QListWidget(groupProfessors)
            self.listProfessors.currentItemChanged.connect(
                self.actualProfesorCambio)

            # Grupos
            # ......
            self.listSchedules = QTableView(groupSchedules)
            self.listSchedules.setTabKeyNavigation(False)

            self.modelSchedules = QStandardItemModel(0, 6, self.listSchedules)

            # Distibución de controles en los widgets
            # =======================================

            # Materias
            # ........
            actionsLSubjects.addStretch()
            actionsLSubjects.addWidget(btnCatalogo)
            actionsLSubjects.addWidget(btnAddByKey)
            actionsLSubjects.addWidget(btnRemove)
            actionsLSubjects.addWidget(btnUpdateSubjects)

            layoutSubjects.addWidget(self.listSubjects)
            layoutSubjects.addWidget(actionsSubjects)

            # Profesores
            # ..........
            layoutProfessors.addWidget(self.listProfessors)

            # Horarios
            # ........
            layoutSchedules.addWidget(self.listSchedules)

            # Página
            # ......
            pagina.addWidget(groupSubjects)
            pagina.addWidget(groupProfessors)
            pagina.addWidget(groupSchedules)

        # Horario preferido
        elif n == 1:

            # Contenedores
            # ============
            pagina = QWidget(parent)
            paginaLayout = QVBoxLayout(pagina)

            filaBotones = QWidget(pagina)
            hboxBotones = QHBoxLayout(filaBotones)

            # Controles
            # =========

            # Fila botones
            btnMatutino = QPushButton("Mañana", filaBotones)
            btnVerspertino = QPushButton("Tarde", filaBotones)
            btnTodas = QPushButton("Todas", filaBotones)
            btnNinguna = QPushButton("Ninguna", filaBotones)
            btnClonar = QPushButton("Clonar selección", filaBotones)
            lblDia = QLabel("Día:", filaBotones)

            # Asignamos las señales a los botones
            btnMatutino.clicked.connect(self._horasMatutino)
            btnVerspertino.clicked.connect(self._horasVespertino)
            btnTodas.clicked.connect(self._horasTodas)
            btnNinguna.clicked.connect(self._horasNinguna)
            btnClonar.clicked.connect(self._horasClonar)

            self.cmbDia = QComboBox(filaBotones)
            self.cmbDia.addItems(self.diasString)
            self.cmbDia.currentIndexChanged.connect(
                self.actualDiaCambio)

            # Lista horas
            lblHorasDisp = QLabel("Horas para tomar clase:", pagina)
            self.listHours = QListWidget(pagina)
            self.listHours.setSelectionMode(self.listHours.ExtendedSelection)
            self.listHours.itemChanged.connect(self._horaCambio)

            for h in self.horas.keys():
                item = QListWidgetItem(h, self.listHours)
                item.setCheckState(Qt.Checked)

            # Disposición de controles
            # ========================
            hboxBotones.addStretch()
            hboxBotones.addWidget(btnMatutino)
            hboxBotones.addWidget(btnVerspertino)
            hboxBotones.addWidget(btnTodas)
            hboxBotones.addWidget(btnNinguna)
            hboxBotones.addWidget(btnClonar)
            hboxBotones.addWidget(lblDia, alignment=QtGui.Qt.AlignRight)
            hboxBotones.addWidget(self.cmbDia)

            paginaLayout.addWidget(filaBotones)
            paginaLayout.addWidget(lblHorasDisp)
            paginaLayout.addWidget(self.listHours)

        # Preferencias, aunque me gustaría cambiarlo
        elif n == 2:
            # Contenedores
            # ============
            pagina = QWidget(parent)
            paginaLayout = QVBoxLayout(pagina)

            gboxGeneral = QGroupBox("General", pagina)
            gridGeneral = QGridLayout(gboxGeneral)

            gboxOrden = QGroupBox("Orden de los grupos", pagina)
            gridOrden = QGridLayout(gboxOrden)

            # Controles
            # =========

            # Grupo General
            lblMaxAGenerar = QLabel(
                "Número máximo de horarios a generar:", gboxGeneral)
            self.MaxAGenerar = QLineEdit("50000", gboxGeneral)
            self.MaxAGenerar.setValidator(QtGui.QIntValidator())
            self.MaxAGenerar.editingFinished.connect(self._MaxHorariosCambio)

            lblHuecos = QLabel("Huecos permisibles:", gboxGeneral)
            self.HuecosPerm = QLineEdit("2", gboxGeneral)
            self.HuecosPerm.setValidator(QtGui.QIntValidator(-1, 2))
            self.HuecosPerm.editingFinished.connect(self._HuecosCambio)

            lblHuecosInter = QLabel(
                "Huecos intermedios permisibles:", gboxGeneral)
            self.HuecosInterPerm = QLineEdit("-1", gboxGeneral)
            self.HuecosInterPerm.setValidator(QtGui.QIntValidator(-1, 2))
            self.HuecosInterPerm.editingFinished.connect(self._HuecosInterCambio)

            lblHuecosAyuda = QLabel("-1 significa infinito", gboxGeneral)
            lblHuecosAyuda.setAlignment(Qt.AlignRight)
            lblHuecosAyuda.setStyleSheet("QLabel { color: #77F; }")

            # Grupo Orden
            lblOrdenAyuda = QLabel(
                "Coloca números entre -2 y 2, donde un nº positivo significa"
                "de menor a mayor y un nº negativo es de mayor a menor",
                gboxOrden
            )
            lblOrdenAyuda.setStyleSheet("QLabel { color: #77F; }")

            SoloConCupo = QCheckBox(
                "Solo considerar grupos con cupo", gboxOrden)
            SoloConCupo.stateChanged.connect(self._SoloCupoCambio)
            MateriasEspejo = QCheckBox(
                "Tomar periodos en cuenta (materias espejo)", gboxOrden)
            MateriasEspejo.stateChanged.connect(self._ConsPeriodoCambio)

            lblHora = QLabel("Hora del día:", gboxOrden)
            self.PrioriHora = QLineEdit("2", gboxOrden)
            self.PrioriHora.setValidator(QtGui.QIntValidator(-1, 2))
            self.PrioriHora.editingFinished.connect(self._PriHoraCambio)

            lblDemanda = QLabel("Demanda:", gboxOrden)
            self.PrioriDemanda = QLineEdit("-1", gboxOrden)
            self.PrioriDemanda.setValidator(QtGui.QIntValidator(-1, 2))
            self.PrioriDemanda.editingFinished.connect(self._PriDemaCambio)

            # Disposición de controles
            # ========================

            gridGeneral.addWidget(lblMaxAGenerar, 0, 0)
            gridGeneral.addWidget(self.MaxAGenerar, 0, 1)
            gridGeneral.addWidget(lblHuecos, 1, 0)
            gridGeneral.addWidget(self.HuecosPerm, 1, 1)
            gridGeneral.addWidget(lblHuecosInter, 2, 0)
            gridGeneral.addWidget(self.HuecosInterPerm, 2, 1)
            gridGeneral.addWidget(lblHuecosAyuda, 3, 1, QtGui.Qt.AlignLeft)
            gridGeneral.addWidget(SoloConCupo, 4, 0, QtGui.Qt.AlignTop)
            gridGeneral.addWidget(MateriasEspejo, 5, 0, QtGui.Qt.AlignTop)

            gridOrden.addWidget(lblOrdenAyuda, 0, 0, 1, 2)
            gridOrden.addWidget(lblHora, 1, 0)
            gridOrden.addWidget(self.PrioriHora, 1, 1)
            gridOrden.addWidget(lblDemanda, 2, 0, -1, 1, QtGui.Qt.AlignTop)
            gridOrden.addWidget(self.PrioriDemanda, 2, 1, -1, 1, QtGui.Qt.AlignTop)

            paginaLayout.addWidget(gboxGeneral)
            paginaLayout.addWidget(gboxOrden)
            paginaLayout.addStretch()

        return pagina

    def _createFooter(self):
        self.footer = QWidget(self.windowWidget)

        btnExport = QPushButton("Exportar")
        btnImport = QPushButton("Importar")
        btnSearchSchedule = QPushButton("Buscar horario")
        btnClose = QPushButton("Cerrar")

        # TODO: Implementar exportación e importación de preferencias (baja prioridad)
        # btnExport.clicked.connect(self.exportarPreferencias)
        # btnImport.clicked.connect(self.importarPreferencias)
        btnSearchSchedule.clicked.connect(self._showDialogCombinador)
        btnClose.clicked.connect(QApplication.quit)

        footerGrid = QHBoxLayout(self.footer)

        footerGrid.addStretch()
        footerGrid.addWidget(btnExport)
        footerGrid.addWidget(btnImport)
        footerGrid.addWidget(btnSearchSchedule)
        footerGrid.addWidget(btnClose)

        self._addWidgetToScreen(self.footer)

    def _addWidgetToScreen(self, widget: QWidget):
        self.windowLayout.addWidget(widget)
        self.windowWidget.setLayout(self.windowLayout)

    def resizeEvent(self, event):
        self.redimensionarTablaHorarios()

    @Slot()
    def _showDialogCatalogo(self):
        dialog = Catalogo.Catalogo(self)
        dialog.show()

    @Slot()
    def _showDialogDescargas(self):
        dialog = Descargas.Descargas(self)
        dialog.show()

    @Slot()
    def _showDialogObtenPorClave(self):
        dialog = ObtenPorClave.ObtenPorClave(self.datos, self)
        dialog.show()

    @Slot()
    def _showDialogAbout(self):
        dialog = Acerca.Acerca(self)
        dialog.show()

    @Slot()
    def _showDialogCombinador(self):
        dialog = Combinador.Combinador(self, self.datos)
        dialog.show()

    @Slot()
    def _MaxHorariosCambio(self):
        print("_MaxHorariosCambio")
        self.datos.maxHorarios = self.MaxAGenerar.text()

    @Slot()
    def _HuecosCambio(self):
        self.datos.maxHuecos = self.HuecosPerm.text()

    @Slot()
    def _HuecosInterCambio(self):
        self.datos.maxHuecosInt = self.HuecosInterPerm.text()

    @Slot()
    def _SoloCupoCambio(self, state: int):
        # Cabe considerar que se nos da un 2 si se marca, o un 0 si no
        # se marca, reservando el 1 a un estado "intermedio" (la casilla
        # rellena pero no marcada)
        if state:
            self.datos.conCupo = True
        else:
            self.datos.conCupo = False

    @Slot()
    def _ConsPeriodoCambio(self, state: int):
        # Cabe considerar que se nos da un 2 si se marca, o un 0 si no
        # se marca, reservando el 1 a un estado "intermedio" (la casilla
        # rellena pero no marcada)
        if state:
            self.datos.evaluarPeriodos = True
        else:
            self.datos.evaluarPeriodos = False

    @Slot()
    def _PriHoraCambio(self):
        self.datos.prHora = self.PrioriHora.text()

    @Slot()
    def _PriDemaCambio(self):
        self.datos.prDemanda = self.PrioriDemanda.text()

    @Slot()
    def _horasMatutino(self):
        horasMatutinas = list(self.horas.keys())[:6]

        for i in range(self.listHours.count()):
            item = self.listHours.item(i)

            # Verificamos que esté en las horas de 7:00 am a 12:00 pm
            if item.text() in horasMatutinas:
                self.listHours.item(i).setCheckState(Qt.Checked)
            else:
                self.listHours.item(i).setCheckState(Qt.Unchecked)

    @Slot()
    def _horasVespertino(self):
        horasVespertinas = list(self.horas.keys())[6:]

        for i in range(self.listHours.count()):
            item = self.listHours.item(i)

            # Verificamos que esté en las horas de 1:00 pm en adelante
            # TODO: Agregar una opción "Noche"
            if item.text() in horasVespertinas:
                self.listHours.item(i).setCheckState(Qt.Checked)
            else:
                self.listHours.item(i).setCheckState(Qt.Unchecked)

    @Slot()
    def _horasTodas(self):
        for i in range(self.listHours.count()):
            self.listHours.item(i).setCheckState(Qt.Checked)

    @Slot()
    def _horasNinguna(self):
        for i in range(self.listHours.count()):
            self.listHours.item(i).setCheckState(Qt.Unchecked)

    @Slot()
    def _horasClonar(self):
        # Construimos un pequeño diálogo/función para
        # preguntar a cuándo clonar la selección
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.setWindowTitle(f"Clonar selección del día {self.cmbDia.currentText()}")
        dialogLayout = QVBoxLayout(dialog)

        # Lista con los días y su etiqueta
        lblDays = QLabel("Selecciona los días a cuando clonar la selección")
        listDays = QListWidget(dialog)

        # Botones del diálogo
        btnWidget = QWidget(dialog)
        btnLayout = QHBoxLayout(btnWidget)
        btnOk = QPushButton("Aceptar")
        btnOk.clicked.connect(dialog.accept)
        btnOk.setDefault(True)
        btnCancel = QPushButton("Cancelar")
        btnCancel.clicked.connect(dialog.reject)
        btnLayout.addStretch()
        btnLayout.addWidget(btnOk)
        btnLayout.addWidget(btnCancel)
        btnLayout.addStretch()

        # Agregamos los días
        for d in self.diasString:
            item = QListWidgetItem(d, listDays)
            item.setCheckState(Qt.Unchecked)

        dialogLayout.addWidget(lblDays)
        dialogLayout.addWidget(listDays)
        dialogLayout.addWidget(btnWidget)

        result = dialog.exec_()

        # Si el usuario confirmó la clonación...
        if result:
            # Obtenemos las horas del día a clonar
            diaActual = self.cmbDia.currentIndex()
            horasDiaActual = self.dias[diaActual]

            # Iteramos sobre la lista de días
            for i in range(listDays.count()):
                item = listDays.item(i)

                # Si fue seleccionado para clonar, proseguimos
                if item.checkState() == Qt.Checked:
                    # Obtenemos el índice buscando por texto en la lista de textos
                    dia = self.diasString.index(item.text())
                    # Asignamos las horas del día visualizado actualmente
                    self.dias[dia] = horasDiaActual

    @Slot()
    def _horaCambio(self, item: QListWidgetItem):
        dia = self.cmbDia.currentIndex()
        hora = item.text()
        horaMarcada = item.checkState() == Qt.Checked
        self.dias[dia][hora] = horaMarcada

    @Slot()
    def actualDiaCambio(self, index: int):
        horasDia = self.dias[index].items()

        self.listHours.clear()

        for hora, activa in horasDia:
            checkstate = Qt.Checked if activa else Qt.Unchecked

            item = QListWidgetItem(hora, self.listHours)
            item.setCheckState(checkstate)

    @Slot()
    def actualMateriaCambio(self, current: QListWidgetItem, previous: QListWidgetItem):
        # Si SI se seleccionó una materia, proseguimos
        if current is not None:
            materia = current.data(QtGui.Qt.UserRole)

            # Limpiamos la lista
            self.listProfessors.clear()

            for m in materia.maestros:
                # Creamos el item del maestro
                item = QListWidgetItem(str(m))
                # Lo hacemos marcable
                item.setCheckState(QtGui.Qt.Checked)
                # Guardamos los datos como UserRole (cosa del usuario, básicamente)
                item.setData(QtGui.Qt.UserRole, m)
                # Añadimos el item
                self.listProfessors.addItem(item)

        # Si NO se seleccionó una materia, limpiamos la lista
        else:
            self.listProfessors.clear()

    @Slot()
    def actualProfesorCambio(self, current: QListWidgetItem, previous: QListWidgetItem):
        # Limpiamos la lista
        self.modelSchedules.clear()

        # Ponemos las cabeceras siempre que limpiemos la lista
        self.modelSchedules.setHorizontalHeaderLabels([
            "NRC", "Sección", "Cupo", "Disponible", "Horario", "Periodo",
        ])

        # Si SI se seleccionó un maestro, proseguimos
        if current is not None:
            maestro = current.data(QtGui.Qt.UserRole)

            for r, g in enumerate(maestro.grupos):
                row = [
                    QStandardItem(g.getNrc()),
                    QStandardItem(g.getSec()),
                    QStandardItem(str(g.getCup())),
                    QStandardItem(str(g.getDis())),
                    QStandardItem(g.getHor()),
                    QStandardItem(str(g.horario.getPeriodo())),
                ]

                for c, item in enumerate(row):
                    item.setEditable(False)
                    self.modelSchedules.setItem(r, c, item)

        # Si NO se seleccionó un maestro, limpiamos la lista
        else:
            self.modelSchedules.clear()

        self.listSchedules.setModel(self.modelSchedules)
        self.redimensionarTablaHorarios()

    @Slot()
    def redimensionarTablaHorarios(self):
        # Para ajustar el tamaño de las columnas a un porcentaje
        tableWidthPercent = self.listSchedules.width() // 100

        self.listSchedules.setColumnWidth(0, tableWidthPercent * 9)
        self.listSchedules.setColumnWidth(1, tableWidthPercent * 8)
        self.listSchedules.setColumnWidth(2, tableWidthPercent * 7)
        self.listSchedules.setColumnWidth(3, tableWidthPercent * 11)
        self.listSchedules.setColumnWidth(4, tableWidthPercent * 46)
        self.listSchedules.setColumnWidth(5, tableWidthPercent * 20)

    def agregarMateria(self, claves: list, centro: str, calendario: str):
        if DEBUG_MODE:
            print(claves)
            print(centro)
            print(calendario)

        for clave in claves:
            # Añadimos un callback a la función self.actualizarDatos() para actualizar la lista de materias
            self.datos.eventos.append(self.actualizarDatos)
            # Creamos la MateriaSiiau
            materia = MateriaSiiau(clave, centro, calendario)
            # Procesamos
            self.datos.cargar(materia)

    @Slot()
    def eliminarMateria(self):
        index = -1

        for item in reversed(self.listSubjects.selectedItems()):
            index = self.listSubjects.indexFromItem(item).row()
            item = self.listSubjects.takeItem(index)
            i = self.datos.materias.index(item.data(QtGui.Qt.UserRole))
            self.datos.materias.pop(i)

        self.actualizarDatos()
        lstSubCnt = self.listSubjects.count()
        if lstSubCnt > 0:
            # Sumamos o restamos según sea el último elemento o no
            index = index + 1 if lstSubCnt > index else index - 1
            self.listSubjects.setCurrentRow(
                index, QItemSelectionModel.Select)

    def actualizarDatos(self):
        self.listSubjects.clear()

        for m in self.datos.materias:
            item = QListWidgetItem(str(m))
            item.setCheckState(QtGui.Qt.Checked)
            item.setData(QtGui.Qt.UserRole, m)
            self.listSubjects.addItem(item)

    def _setPlatformStyle(self):
        # A ver si descubro cómo rayos hacer una buena interfaz
        # Los temas de GTK no se aplican a aplicaciones en Qt escritas en Python, qué estupendo
        styleSheet = """
            background-color: #333;
            color: #FFF;
            font-family: Helvetica;
        """
        self.setStyleSheet(styleSheet)

    def moveCenter(self):
        screenSize = self.screen().size()
        newX = (screenSize.width() - self.size().width()) // 2
        newY = (screenSize.height() - self.size().height()) // 2
        self.move(newX, newY)
