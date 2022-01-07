# -*- coding: utf-8 -*-
"""
Clase Maestro para administrar maestros y los grupos que administran
"""

import copy

from carga.Materia import Materia

class Maestro:
    materia = None
    nombre = ""
    grupos = []

    def __init__(self, materia):
        self.materia = materia
        self.grupos = []
        self.marca = True

    def getNombre(self):
        return self.nombre

    def getPadre(self):
        return self.materia

    def __copy__(self):
        m = Maestro(self.materia)
        m.nombre = self.nombre
        m.marca = self.marca

        for grupo in self.grupos:
            m.grupos.append(copy.copy(grupo))

        return m

    def __str__(self):
        return self.nombre

    def __eq__(self, o):
        if isinstance(o, (Maestro, str)):
            if isinstance(o, Maestro):
                return o.nombre == self.nombre
            else:
                return o == self.nombre
        else:
            return False

    def buscarGrupo(self, grupo: str):
        for g in self.grupos:
            if g == grupo:
                return g

        return None
