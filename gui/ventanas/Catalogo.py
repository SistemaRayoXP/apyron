# -*- coding: utf-8 -*-
"""
Ventana Catálogo que contiene el catálogo de materias

Las materias SIEMPRE estarán actualizadas, porque se obtendrán
directamente desde SIIAU cada vez que se inicie la aplicación.

Se podrá configurar cuándo actualizar las materias, ya que el
proceso de actualización puede tomar varios segundos, considerable
solo para iniciar y usar la aplicación.

Ideas:
- Almacenamiento persistente de "bases de datos" (realmente solo unos JSON)
- Actualizar 1 vez al día
- Actualizar, ¿antes o después de mostrar la interfaz principal?
    - Si es antes, la pantalla de bienvenida deberá informarlo
        - ~~~Desventaja: El inicio se verá retrasado por cuanto tome actualizar~~~
            - Actualización: Utilicé multiproceso, eso deja de lado esta desventaja
    - Si es despés, se mostrará el progreso en la barra de estado
        - Desventaja: Puede usar recursos de segundo plano
- Actualizaciones, a elección (auto-manual)
"""

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QFont, QIcon, QKeySequence, QPixmap, Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot

from carga.AdDatos import AdDatos
from gui.clases.ControlCollection import ControlCollection
from util.DatosPersistentes import DatosPersistentes


class Catalogo(QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()
    controls = ControlCollection()

    lectorCatalogo = DatosPersistentes()
    centros = lectorCatalogo.obtenerCentros()
    calendarios = lectorCatalogo.obtenerCalendarios()

    materias = []
    materiasSeleccionadas = {}
    filtro = ""

    def __init__(self, parent=None):
        super(Catalogo, self).__init__(parent)

        if parent is not None:
            self.setParent(parent)

        # Propiedades de la ventana principal
        # ===================================
        width = (self.screen().availableSize().width() // 8) * 4
        height = (self.screen().availableSize().height() // 8) * 4
        self.resize(width, height)
        self.setWindowTitle("Catálogo de materias")

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QtCore.QLocale.Spanish)

        # Layout del diálogo
        self.dialogLayout = QGridLayout(self)

        self._createControls(self)
        self._createFooter()
        self._cargarPreferencias()
        self.centerToParent()

    def _createControls(self, parent):
        """Genera los controles principales de la ventana"""
        # Para ajustar el tamaño de las columnas a un porcentaje
        tableWidthPercent = (self.size().width() * 1.8) // 100

        # Contenedores
        # ============

        # Diálogo
        # .......
        self.controls.pagina = QSplitter(parent)
        self.controls.pagina.setOrientation(QtCore.Qt.Orientation.Vertical)

        # Materias
        # ........
        self.controls.groupSubjects = QGroupBox(
            "Lista de materias", self.controls.pagina)
        self.controls.vboxSubjects = QVBoxLayout(self.controls.groupSubjects)

        # Layouts del grupo etc
        self.controls.widActions = QWidget(self.controls.groupSubjects)
        self.controls.hboxActions = QHBoxLayout(self.controls.widActions)

        # Selecciones
        # ...........
        self.controls.groupSelected = QGroupBox(
            "Materias seleccionadas", self.controls.pagina)
        self.controls.vboxSelected = QVBoxLayout(self.controls.groupSelected)

        # Controles
        # =========

        # Grupo Materias
        # ..............

        # Definición

        self.controls.lblUniversity = QLabel(
            "Centro universitario:", self.controls.widActions)
        self.cmbUniversity = QComboBox(self.controls.widActions)
        self.controls.lblCalendar = QLabel(
            "Calendario:", self.controls.widActions)
        self.cmbCalendar = QComboBox(self.controls.widActions)
        self.listSubjects = QListWidget(self.controls.groupSubjects)
        self.listSubjects.itemChanged.connect(self._itemChanged)

        # Parte lógica

        # Agregamos los centros
        for c in self.centros:
            self.cmbUniversity.addItem(str(c), userData=c)

        self.cmbUniversity.currentIndexChanged.connect(
            self._centrosChanged)

        # Agregamos los calendarios
        for c in self.calendarios:
            self.cmbCalendar.addItem(str(c), userData=c)

        self.cmbCalendar.currentIndexChanged.connect(
            self._calendarioChanged)

        # Seleccionados
        # .............

        self.listSelected = QListWidget(self.controls.pagina)

        # Establecimiento de layouts
        # ==========================

        # Materias
        # ........

        self.controls.hboxActions.addWidget(self.controls.lblUniversity)
        self.controls.hboxActions.addWidget(self.cmbUniversity)
        self.controls.hboxActions.addWidget(self.controls.lblCalendar)
        self.controls.hboxActions.addWidget(self.cmbCalendar)
        self.controls.hboxActions.addStretch()

        self.controls.vboxSubjects.addWidget(self.controls.widActions)
        self.controls.vboxSubjects.addWidget(self.listSubjects)

        # Selecciones
        # ...........

        self.controls.vboxSelected.addWidget(self.listSelected)

        # Diálogo
        # .......

        self.controls.pagina.addWidget(self.controls.groupSubjects)
        self.controls.pagina.addWidget(self.controls.groupSelected)

        self._addWidgetToScreen(self.controls.pagina)

    def _createFooter(self):
        """Genera el pie de la ventana"""
        self.footer = QWidget(self)
        self.footerGrid = QHBoxLayout(self.footer)

        self.controls.lblSearch = QLabel("Buscar:", self.footer)
        self.inputSearch = QLineEdit(self.footer)
        self.btnFilter = QPushButton("Filtrar", self.footer)
        self.btnClear = QPushButton("Limpiar", self.footer)
        self.btnDownload = QPushButton("Descargar", self.footer)
        
        self.inputSearch.editingFinished.connect(self.btnFilter.clicked)
        self.btnFilter.setAutoDefault(True)
        self.btnFilter.clicked.connect(self.filtrarMaterias)
        self.btnClear.clicked.connect(self.limpiarSeleccion)
        self.btnDownload.clicked.connect(self.descargarMaterias)

        self.footerGrid.addStretch()
        self.footerGrid.addWidget(self.controls.lblSearch)
        self.footerGrid.addWidget(self.inputSearch)
        self.footerGrid.addWidget(self.btnFilter)
        self.footerGrid.addWidget(self.btnClear)
        self.footerGrid.addWidget(self.btnDownload)
        self.footerGrid.addStretch()

        self._addWidgetToScreen(self.footer)

        self.inputSearch.setFocus(QtCore.Qt.FocusReason.ActiveWindowFocusReason)

    def _addWidgetToScreen(self, widget: QWidget):
        self.dialogLayout.addWidget(widget)
        self.setLayout(self.dialogLayout)

    def _cargarPreferencias(self):
        self.cmbUniversity.setCurrentIndex(4)
        self.cmbCalendar.setCurrentIndex(2)

    @Slot()
    def _itemChanged(self, item: QListWidgetItem):
        if item.checkState() == Qt.CheckState.Checked:
            # Obtenemos la materia
            registro = item.data(Qt.UserRole)

            # Verificamos que no exista
            if self.materiasSeleccionadas.get(registro.clave) is None:
                # Creamos el item
                new_item = QListWidgetItem(item.text())
                # Establecemos la materia en userData
                new_item.setData(Qt.UserRole, registro)
                # Agregamos el item al diccionario de selccionados
                self.materiasSeleccionadas[registro.clave] = new_item
                # Agregamos el item al widget
                self.listSelected.addItem(new_item)

        else:
            registro = item.data(Qt.UserRole)
            checked_item = self.materiasSeleccionadas.pop(registro.clave, None)

            if checked_item is not None:
                index = self.listSelected.indexFromItem(checked_item).row()
                self.listSelected.takeItem(index)

    @Slot()
    def _calendarioChanged(self, index: int):
        # TODO: Investigar cómo obtener materias de ciertos periodos en CATAX
        # calendario =self.cmbCalendar.itemData(index)
        # clave = calendario.clave
        # print(f'calendarioIndex: {index}')
        pass

    @Slot()
    def _centrosChanged(self, index: int):
        self.inputSearch.setText("")
        self.filtro = self.inputSearch.text()
        self.loadSubjects()

    @Slot()
    def filtrarMaterias(self):
        self.filtro = self.inputSearch.text()
        self.loadSubjects(self.filtro)
        self.listSubjects.setFocus(Qt.FocusReason.TabFocusReason)

    @Slot()
    def limpiarSeleccion(self):
        self.listSelected.clear()
        self.loadSubjects()

    @Slot()
    def descargarMaterias(self):
        self.close()

        clavesObj = [
            self.listSelected.item(r).data(Qt.UserRole)
            for r in range(self.listSelected.count())
        ]
        centroObj = self.cmbUniversity.currentData(Qt.UserRole)
        calendarioObj = self.cmbCalendar.currentData(Qt.UserRole)

        claves = [c.clave for c in clavesObj]
        centro = centroObj.clave
        calendario = calendarioObj.clave

        self.parent().agregarMateria(claves, centro, calendario)

    def loadSubjects(self, filtro: str = None):
        # Como guardamos el centro en itemData, de ahí lo sacamos
        centroObj = self.cmbUniversity.currentData(Qt.UserRole)
        centro = centroObj.clave

        # Cargamos las materias del centro
        self.materias = self.lectorCatalogo.obtenerMaterias(centro)

        # Obtenemos la lista de claves (para no perder las marcas)
        claves = []

        for i in range(self.listSelected.count()):
            registro = self.listSelected.item(i).data(Qt.UserRole)
            claves.append(registro.clave)

        # Cargamos el filtro global si no se nos dió ninguno
        filtro = self.filtro if filtro is None else filtro

        # Reiniciamos la lista de materias
        self.listSubjects.clear()

        # Agregamos las materias a la lista, filtramos
        for m in self.materias:
            # Filtramos, si aplica
            if filtro:
                materiastr = str(m).upper()
                filtro = filtro.upper()

                if not filtro in materiastr:
                    continue

            item = QListWidgetItem(str(m))
            item.setData(Qt.UserRole, m)

            if m.clave in claves:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            self.listSubjects.addItem(item)

    def centerToParent(self):
        parentX = self.parent().x() + (self.parent().width() // 2)
        parentY = self.parent().y() + (self.parent().height() // 2)
        newX = parentX - (self.width() // 2)
        newY = parentY - (self.height() // 2)
        self.move(newX, newY)
