# -*- coding: utf-8 -*-
"""
Clase Grupo para administrar grupos detectados del SIIAU
"""

from carga . Horario import Horario
from carga . Maestro import Maestro


class Grupo:
    padre = None
    nrc = ""
    sec = ""
    cup = 0
    dis = 0
    horario = None
    huecos = 0

    def __init__(self, padre):
        self.padre = padre

    def getPadre(self):
        return self.padre

    def getNrc(self):
        return self.nrc

    def getSec(self):
        return self.sec

    def getCup(self):
        return self.cup

    def getDis(self):
        return self.dis

    def subHorario(self, h):
        return self.horario.subHorario(h)

    def getHor(self):
        return str(self.horario)

    def __str__(self):
        return "{} {}".format(self.nrc, self.horario)

    def __eq__(self, o):
        if isinstance(o, (Grupo, str)):
            if isinstance(o, Grupo):
                return o.nrc == self.nrc
            else:
                return o == self.nrc
        else:
            return False

    def __copy__(self):
        g = Grupo(padre)
        g.nrc = self.nrc
        g.sec = self.sec
        g.cup = self.cup
        g.dis = self.dis
        g.horario = self.horario.copy()
        g.marca = self.marca
        return g
