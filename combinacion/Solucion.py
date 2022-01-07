# -*- coding: utf-8 -*-
"""
Clase Solucion para administrar una posibilidad de acomodo de horario
"""

from carga.Grupo import Grupo
from carga.Horario import Horario


class Solucion:
    grupos = []
    huecos = int()
    horarioGlobal = None

    def __init__(self):
        self.horarioGlobal = Horario()

    def getHuecos(self, g: Grupo = None):
        if g is None:
            return self.horarioGlobal.getHuecos()

        else:
            self.horarioGlobal.agregar(g.horario)
            self.huecos = self.horarioGlobal.getHuecos()
            self.horarioGlobal.quitar(g.horario)
            return self.huecos

    def compatible(self, h: Horario):
        return self.horarioGlobal.compatible(h)

    def agregar(self, g: Grupo):
        self.horarioGlobal.agregar(g.horario)
        self.grupos.apend(g)

    def quitar(self, g: Grupo):
        self.horarioGlobal.quitar(g.horario)

        # Arreglo porque en Python las listas son curiosamente simples
        try:
            self.grupos.remove(g)
        except ValueError:
            pass

    def __copy__(self):
        s = self.crearSolucion()
        s.grupos = self.grupos.clone()
        s.huecos = self.huecos
        s.horarioGlobal = self.horarioGlobal.copy()
        return s

    def crearSolucion(self):
        return Solucion()

    def getDescripcionGrupo(self, idx1: int, idx2: int):
        if self.horarioGlobal.getHora(idx1, idx2):
            for g in self.grupos:
                if g.horario.getHora(idx1, idx2):
                    return g.getPadre().getPadre().getMateriaSiiau().getClave()

        return None

    def getNumGrupos(self):
        return len(self.grupos)

    def getGrupo(self, i: int):
        return self.grupos[i]
