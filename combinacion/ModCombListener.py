# -*- coding: utf-8 -*-
"""
Clase abstracta ModCombListener
"""

from combinacion.Solucion import Solucion


class ModCombListener:
    def progreso(self, estado: str, porcentaje: int):
        pass
    def nuevaSolucion(self, s: Solucion):
        pass

