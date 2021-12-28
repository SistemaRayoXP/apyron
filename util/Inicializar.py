# -*- coding: utf-8 -*-
"""
Módulo para la inicialización del programa.

Verifica algunas cosas, como carpetas, archivos, etcétera
"""

import os

from multiprocessing import Process

from PySide2.QtWidgets import QSplashScreen

from util.DatosPersistentes import GeneradorCatalogo
from util.DatosPersistentes import DatosPersistentes

def inicializar(splashobj: QSplashScreen):
    splashobj.showMessage("Iniciando...")
    gc = GeneradorCatalogo()
    procesos = []
    # TODO: Informar la tarea mediante los subprocesos
    # TODO: Mejorar lo de los subprocesos, está medio extraño/malhecho por ahora

    # splashobj.showMessage("Cargando calendarios...")
    procesos.append(
        Process(
            target=gc.generarCatalogoAsync,
            args=("calendarios",),
            kwargs={'update_if_exists': False}
        )
    )
    # splashobj.showMessage("Cargando centros...")
    procesos.append(
        Process(
            target=gc.generarCatalogoAsync,
            args=("centro",),
            kwargs={'update_if_exists': False}
        )
    )
    # splashobj.showMessage("Cargando materias...")
    procesos.append(
        Process(
            target=gc.generarCatalogoAsync,
            args=("materiastodas",),
            kwargs={'update_if_exists': False}
        )
    )

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()
