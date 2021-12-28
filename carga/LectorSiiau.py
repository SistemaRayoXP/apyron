# -*- coding: utf-8 -*-
"""
Módulo para descargar, esquematizar y traducir los datos del SIIAU a datos serializables
(parte transformadora de APP_NAME)
"""
# ================================================================
# BUG: Los horarios de múltiples filas no se agregan correctamente
#      Probar con clave I7370, centro D, ciclo 202210
#      Ej. HUERTA OROZCO, ROBERTO
#
#      Esperado:
#          Martes 1700-1855
#          Jueves 1700-*1755*
#      Obtenido:
#          Martes 1700-1855
#          Jueves 1700-*1855*
# ================================================================
# TODO: Mejorar la asignación de las variables ruta* en LectorSiiau.procesarEntrada():

from bs4 import BeautifulSoup
from collections import OrderedDict as odict
from util.Constants import *
from carga.Horario import Horario
from carga.LectorHttp import LectorHttp
from carga.MateriaSiiau import MateriaSiiau
from carga.Registro import Registro


class LectorSiiau:
    """
    Clase LectorSiiau para obtener los registros asociados a una
    materia desde el SIIAU.

    Si la aplicación deja de funcionar, puede que este módulo sea
    el culpable
    """
    f = None
    rutaNrc = ""
    rutaClave = ""
    rutaMateria = ""
    rutaSec = ""
    rutaCr = ""
    rutaCup = ""
    rutaDis = ""
    rutaHor = ""
    rutaProf = ""
    registros = []
    invReg = 0
    silent = not DEBUG_MODE
    url = ""
    urlparams = odict({
        'ciclop': "",
        'cup': "",
        'majrp': "",
        'crsep': "",
        'materiap': "",
        'horaip': "",
        'horafp': "",
        'edifp': "",
        'aulap': "",
        'ordenp': 0,
        'mostrarp': -1,
    })

    def __init__(self, f: MateriaSiiau):
        self.url = f"{SIIAU_SERVER}/wco/sspseca.consulta_oferta"
        self.urlparams['ciclop'] = f.getCal()
        self.urlparams['cup'] = f.getCentro()
        self.urlparams['crsep'] = f.getClave()
        self.registros = []
        self.f = f
        self.procesar()

    def getMateriaSiiau(self):
        return self.f

    def procesar(self):
        respuesta = LectorHttp(self.url, params=self.urlparams, soup=True)
        materias = []

        tabla = respuesta.soup.find('table').find('tbody')

        for tr in tabla.findAll('tr', recursive=False):
            if tr.find('td', class_='tddatos'):
                tag = tr.findAll('td', recursive=False)
                self.registros.append(self.procesarEntrada(tag))

    def procesarEntrada(self, tag):
        try:
            registro = Registro()
            registro.nrc = tag[0].text
            registro.clave = tag[1].text
            registro.materia = tag[2].text
            registro.seccion = tag[3].text
            registro.creditos = tag[4].text
            registro.cupo = tag[5].text
            registro.disponible = tag[6].text

            horarios = tag[7].findAll('tr')
            if horarios:
                for tr in horarios:
                    horario = tr.findAll('td')

                    horas = horario[1].text.strip()
                    dias = horario[2].text.strip()
                    modulo = horario[3].text.strip()
                    aula = horario[4].text.strip()
                    registro.horario.setDatos(dias, modulo, aula, horas)

                    registro.periodo = horario[5].text.strip()
                    registro.horario.setPeriodo(registro.periodo)

            celdaProfesor = tag[8].find('tr')

            if celdaProfesor:
                celdaProfesor = celdaProfesor.findAll('td')
                # registro.sesion = celdaProfesor[0].text
                registro.profesor = celdaProfesor[1].text.strip()

            if not self.rutaNrc:
                self.rutaNrc = registro.nrc
                self.rutaClave = registro.clave
                self.rutaMateria = registro.materia
                self.rutaSec = registro.seccion
                self.rutaCr = registro.creditos
                self.rutaCup = registro.cupo
                self.rutaDis = registro.disponible
                self.rutaHor = registro.horario
                self.rutaProf = registro.profesor

            return registro

        except Exception:
            self.invReg += 1

            if not self.silent:
                import traceback
                print(traceback.format_exc())
