# -*- coding: utf-8 -*-
"""
Clase abstracta SubHora
"""

from carga . Horario import Horario
from carga . Marcable import Marcable


class SubHora(Marcable):
    h = Horario()
    idx1 = int()
    idx2 = int()
    label = ""

    def getMarca(self):
        return self.h.getHora(idx1, idx2)

    def setMarca(marca: bool):
        self.h.setHora(idx1, idx2, marca)

    def __init__(self, h: Horario, idx1: int, idx2: int, label: str):
        self.h = h
        self.idx1 = idx1
        self.idx2 = idx2
        self.label = label

    def __str__(self):
        return self.label
