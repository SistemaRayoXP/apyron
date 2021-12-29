# -*- coding: utf-8 -*-
"""
Módulo base de la clase ModeloCombinatorio
TODO: Implementar bien este módulo
"""

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

        if not inverso:
            for z in range(len(materias)):
                for x in reversed(range(len(materias[z]) - 1)):
                    for y in range(x, len(materias[z])-1):
                        if materias[z][y].getDis() < materias[z][y+1].getDis():
                            tmp = materias[z][y]
                            materias[z][y] = materias[z][y+1]
                            materias[z][y+1] = tmp
                        else:
                            break

        else:

            for z in range(len(materias)):
                for x in reversed(range(len(materias[z])-1)):
                    for y in range(x, len(materias[z])-2):
                        if materias[z][y].getDis() > materias[z][y+1].getDis():
                            tmp = materias[z][y]
                            materias[z][y] = materias[z][y+1]
                            materias[z][y+1] = tmp
                        else:
                            break

    def ordenaPorTemprano(self, inverso: bool):
        # Ordenar por horarios mas tempranos

        if inverso:
            for z in range(len(materias)):
                for x in reversed(range(len(materias[z])-1)):
                    for y in range(x, len(materias[z])-2):
                        if materias[z][y].horario.getHorarioTotal() < materias[z][y+1].horario.getHorarioTotal():
                            tmp = materias[z][y]
                            materias[z][y] = materias[z][y+1]
                            materias[z][y+1] = tmp
                        else:
                            break

        else:
            # for(int z=0;z<materias.length;z++):
            for z in range(len(materias)):
                for x in reversed(range(len(materias[z])-1)):
                    for y in range(x, len(materias[z])-2):
                        if(materias[z][y].horario.getHorarioTotal() > materias[z][y+1].horario.getHorarioTotal()):
                            tmp = materias[z][y]
                            materias[z][y] = materias[z][y+1]
                            materias[z][y+1] = tmp
                        else:
                            break

    def ordenaPorNdGrupos(self, inverso: bool):
        if inverso:
            for x in reversed(range(len(materias)-1)):
                for y in range(x, len(materias[z])-1):
                    if len(materias[y]) < len(materias[y+1]):
                        tmp = materias[y]
                        materias[y] = materias[y+1]
                        materias[y+1] = tmp
                    else:
                        break
        else:

            for x in reversed(range(len(materias)-1)):
                for y in range(x, len(materias[z])-1):
                    if len(materias[y]) > len(materias[y+1]):
                        tmp = materias[y]
                        materias[y] = materias[y+1]
                        materias[y+1] = tmp
                    else:
                        break

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

        self.horarioUsuario = datos.horarioUsuario.copy()

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
                        if (grp.getDis() > 0 or conCupo == False) and grp.subHorario(horarioUsuario):
                            self.grps += 1

            materias[x] = []

            # for (int y=0;y<mat.maestros.size();y++){
            for maestro in mat.maestros:
                if maestro.getMarca():  # Filtrar por maestro
                    for z, grp in enumerate(maestro.grupos):
                        # Filtrar por cupo y por horario del usuario
                        if (grp.getDis() > 0 or conCupo == False) and grp.subHorario(horarioUsuario):
                            idx += 1
                            materias[x][idx] = maestro.grupos[z]

        # Ordenacion de materias
        ordenaPorNdGrupos(False)

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
        for evento in eventos:
            evento.progreso(estado, porcentaje)

    def fireNuevaSolucion(self, s):
        for evento in eventos:
            evento.nuevaSolucion(s)

    def run(self):
        try:
            self.combinar()

            if (solCount > 0):
                self.arrSol = []

                indice = 0

                for x in range(90):
                    if hashHuecos[x] != None:
                        for i in range(len(hashHuecos[x])):
                            self.arrSol.append(hashHuecos[x][i])
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
