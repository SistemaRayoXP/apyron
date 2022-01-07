# -*- coding: utf-8 -*-
"""
Módulo base de la clase ModeloCombinatorio
TODO: Implementar bien este módulo
"""

import copy

from carga.AdDatos import AdDatos
from carga.Grupo import Grupo
from carga.Horario import Horario
from carga.Maestro import Maestro
from carga.Materia import Materia


class ModeloCombinatorio:
    eventos = []
    total = int()
    progreso = int()

    maxHuecos = int()
    maxHorarios = int()
    maxHuecosInt = int()
    conCupo = bool()
    abortar = bool()
    materias = []
    horarioUsuario = None  # Clase Horario

    datos = None  # AdDatos
    # soluciones = []
    arrSol = []
    hashHuecos = []
    solCount = int()

    def getTotal(self):
        return self.total

    def getProgreso(self):
        return self.progreso

    """
    def quickSort(self, primero: int, ultimo: int, soluciones):
        
        if primero>=ultimo:
            return
        
        pivote=soluciones[(primero+ultimo)//2].horario.getHuecos()
        i=primero
        j=ultimo
        
        while True:
            while soluciones[i].horario.getHuecos()<=pivote and i<ultimo:
                i += 1
            while soluciones[j].horario.getHuecos()>=pivote and j>primero:
                j -= 1
            
            if i<=j:
                tmp = soluciones[i]
                soluciones[i]=soluciones[j]
                soluciones[j]=tmp
                i += 1
                j -= 1
            }
            if not i<=j:
                break
        
        if primero<j:
            self.quickSort(primero,j,soluciones)
        
        if i<ultimo:
            self.quickSort(i,ultimo,soluciones)
    
    """

    def ordenaPorDemanda(self, inverso: bool):
        # Ordenar por horarios mas tempranos
        tmp_materias = copy.copy(self.materias)

        for x, mat in self.materias:
            mat = sorted(mat, key=lambda x: x.getDis())
            tmp_materias[x] = mat

        self.materias = tmp_materias

    def ordenaPorTemprano(self, inverso: bool):
        # Ordenar por horarios mas tempranos
        tmp_materias = copy.copy(self.materias)

        for x, mat in self.materias:
            mat = sorted(mat, key=lambda x: x.horario.getHorarioTotal())
            tmp_materias[x] = mat

        self.materias = tmp_materias

    def ordenaPorNdGrupos(self, inverso: bool):
        # Ordenar por longitud de lista
        self.materias = sorted(self.materias, key=lambda x: len(x))

    def __init__(self, datos: AdDatos):
        self.datos = datos
        self.eventos = []
        self.hashHuecos = []
        self.solCount = 0
        self.abortar = False
        self.maxHorarios = datos.maxHorarios
        self.maxHuecos = datos.maxHuecos
        self.maxHuecosInt = datos.maxHuecosInt
        self.conCupo = datos.conCupo

        self.horarioUsuario = copy.copy(datos.horarioUsuario)

        self.materias = []

        for x in range(len(datos.materias)):
            self.idx = 0
            self.grps = 0

            # Determinar el numero de grupos
            mat = datos.materias[x]
            # for (int y=0;y<mat.maestros.size();y++){
            for maestro in mat.maestros:
                if maestro.getMarca():  # Filtrar por maestro
                    # for (int z=0;z<maestro.grupos.size();z++){
                    for grp in maestro.grupos:
                        # Filtrar por cupo y por horario del usuario
                        if (grp.getDis() > 0 or self.conCupo == False) and grp.subHorario(self.horarioUsuario):
                            self.grps += 1

            self.materias[x] = []
            idx = 0

            # for (int y=0;y<mat.maestros.size();y++){
            for maestro in mat.maestros:
                if maestro.getMarca():  # Filtrar por maestro
                    for z, grp in enumerate(maestro.grupos):
                        # Filtrar por cupo y por horario del usuario
                        if (grp.getDis() > 0 or self.conCupo == False) and grp.subHorario(self.horarioUsuario):
                            idx += 1
                            self.materias[x][idx] = maestro.grupos[z]

        # Ordenacion de materias
        self.ordenaPorNdGrupos(False)

        # Ordenacion de grupos
        if datos.prDemanda > -1:
            if datos.prHora > -1:
                if (datos.prDemanda < datos.prHora):
                    self.ordenaPorTemprano(False)
                    self.ordenaPorDemanda(False)
                else:
                    self.ordenaPorDemanda(False)
                    self.ordenaPorTemprano(False)

            else:
                if datos.prDemanda < (datos.prHora*-1):
                    self.ordenaPorTemprano(True)
                    self.ordenaPorDemanda(False)
                else:
                    self.ordenaPorDemanda(False)
                    self.ordenaPorTemprano(True)

        else:
            if (datos.prHora > -1):
                if (-1*datos.prDemanda) < datos.prHora:
                    self.ordenaPorTemprano(False)
                    self.ordenaPorDemanda(True)
                else:
                    self.ordenaPorDemanda(True)
                    self.ordenaPorTemprano(False)

            else:
                if (datos.prDemanda > datos.prHora):
                    self.ordenaPorTemprano(True)
                    self.ordenaPorDemanda(True)
                else:
                    self.ordenaPorDemanda(True)
                    self.ordenaPorTemprano(True)

    def abortar(self):
        self.abortar = True

    def addModCombListener(self, ml):
        self.eventos.apend(ml)

    def terminar(self):
        self.eventos = []
        self.arrSol = None
        self.hashHuecos = None
        self.solCount = 0

    def fireProgreso(self, estado: str, porcentaje: int):
        for evento in self.eventos:
            evento.progreso(estado, porcentaje)

    def fireNuevaSolucion(self, s):
        for evento in self.eventos:
            evento.nuevaSolucion(s)

    def run(self):
        try:
            self.combinar()

            if self.solCount > 0:
                self.arrSol = []

                indice = 0

                for x in range(90):
                    if self.hashHuecos[x] != None:
                        for i in range(len(self.hashHuecos[x])):
                            self.arrSol.append(self.hashHuecos[x][i])
                            indice += 1
                self.fireProgreso("Proceso terminado al", -3)

            else:
                self.fireProgreso(
                    "No se encontro ningun horario. Trata cambiando las Preferencias", -3)

        except MemoryError:
            self.arrSol = None
            self.hashHuecos = None
            self.solCount = 0
            self.System.gc()
            self.fireProgreso(
                "Falta Memoria [Cierra ventanas y limita el número de horarios a generar]", -3)

    def getSolCount(self):
        return self.solCount

    def getSol(self, indice: int):
        return self.arrSol[indice]

    def combinar(self):
        pass
