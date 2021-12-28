# -*- coding: utf-8 -*-
"""
Clase Materia para administrar materias y los maestros y grupos que tengan registrados
"""

from carga.MateriaSiiau import MateriaSiiau


class Materia:
    fuente = None
    nombre = ""
    creditos = ""
    maestros = []

    def __init__(self):
        super()
        self.maestros = []

    def getNombre(self):
        return self.nombre

    def __copy__(self):
        m = Materia()
        m.fuente = self.fuente.copy()
        m.nombre = self.nombre
        m.creditos = self.creditos
        m.marca = self.marca

        for maestro in self.maestros:
            m.maestros.append(maestro.copy())

        return m

    def getMateriaSiiau(self):
        return self.fuente

    def __str__(self):
        return self.nombre

    def __eq__(self, x):
        return str(x) == self.nombre

    def buscarMaestro(self, obj):
        for x in range(len(self.maestros)):
            if str(obj) in str(self.maestros[x]):
                if str(obj) == str(self.maestros[x]):
                    return x
                # else:
                #     return -(x+1)

        return -(len(self.maestros)+1)

    """
    def buscarMaestro(self, obj):
        for maestro in self.maestros:
            if maestro == obj:
                return maestro

        return None
    """
