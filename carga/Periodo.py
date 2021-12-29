# -*- coding: utf-8 -*-
"""
Clase abstracta Periodo para administrar los periodos de inicio y fin de cursos de las materias
"""

from datetime import datetime


class Periodo:
    inicio = None
    fin = None

    def __init__(self, inicio: datetime, fin: datetime):
        self.inicio = inicio
        self.fin = fin

    def __str__(self):
        inicioStr = self.inicio.strftime("%d/%m/%y")
        finStr = self.fin.strftime("%d/%m/%y")
        periodo = f"{inicioStr} - {finStr}"
        return periodo

    def __eq__(self, o):
        if isinstance(o, Periodo):
            return o.inicio == self.inicio and o.fin == self.fin

        return False

    def getInicio(self):
        return self.inicio

    def getFin(self):
        return self.fin

    def compatible(self, p):
        if self.getInicio() and self.getFin() and p.getInicio() and p.getFin():
            if self.getInicio() > p.getFin() or p.getInicio() > self.getFin():
                return True

        return false

    def estaDentroDe(self, p):
        return self.estaDentroDe(p.getInicio(), p.getFin())

    def estaDentroDe(self, i: datetime, f: datetime):
        if inicio and fin:
            if ((self.inicio == i or self.inicio < i) and self.fin > i) or \
                    ((self.inicio == i or self.inicio > i) and inicio < f):
                return True

            return False

        return True
