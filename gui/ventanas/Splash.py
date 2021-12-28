# -*- coding: utf-8 -*-
"""
Ventana de Bienvenida (Splash) al iniciar la aplicación
"""

from PySide2.QtWidgets import QSplashScreen
from PySide2.QtGui import QPainter, QPixmap
from util.Constants import *


class Splash(QSplashScreen):
    # def drawContents(self, painter: QPainter):
    #     # painter.setBackground(bg)
    #     pass

    def moveCenter(self):
        screenSize = self.screen().size()
        newX = (screenSize.width() - self.size().width()) // 2
        newY = (screenSize.height() - self.size().height()) // 2
        self.move(newX, newY)

