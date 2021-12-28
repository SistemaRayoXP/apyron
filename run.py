# -*- coding: utf-8 -*-
"""
APP_NAME: Organizador y generador de horarios del SIIAU.
Escrito en Python 3, diseñado en Qt, preparado para otros 15 años de uso

Basado en el programa Apeiron, de «rieztra»

Código original escrito en Java por Francisco Riestra
"""

import os
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QSplashScreen
from PySide2.QtGui import QPixmap
from PySide2 import QtCore

from util.Constants import *
from gui import Principal
from gui.ventanas.Splash import Splash
from util import Inicializar


def main():
    app = QApplication(sys.argv)
    splashimage = QPixmap(APP_SPLASH_PATH)
    splash = Splash(splashimage)
    splash.show()
    app.processEvents()

    Inicializar.inicializar(splash)
    
    app.processEvents()

    form = Principal.Principal()
    form.moveCenter()
    form.show()
    splash.finish(form)

    return app.exec_()


if __name__ == '__main__':
    main()
