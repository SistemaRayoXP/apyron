# -*- coding: utf-8 -*-
"""
Módulo de datos persistentes para no tener que consultar el SIIAU
cada vez que se abra la aplicación, más sin embargo poder obtener
siempre la información más actualizada

TODO: Implementar generador de catálogo generarCatalogoCarreras()

"""

import os
import re
import json
import csv

from multiprocessing import Process
from util . Constants import *
from carga . Calendario import CalendarioSiiau
from carga . CentroUniversitario import CentroUniversitario
from carga . LectorHttp import LectorHttp


class RegistroCatalogo:
    def __init__(self, clave: str, nombre: str = "", departamento: str = ""):
        self.departamento = departamento
        self.clave = clave
        self.nombre = nombre

    def __eq__(self, o):
        if isinstance(o, (RegistroCatalogo, str)):
            if isinstance(o, RegistroCatalogo):
                return self.clave == o.clave
            else:
                return o == self.nombre or o == self.clave

        return NotImplemented

    def __str__(self):
        return f"{self.nombre} - {self.clave}"

    def toDict(self):
        registro = {
            "departamento": self.departamento,
            "clave": self.clave,
            "materia": self.nombre,
        }

        return registro

    def toJson(self):
        return json.dumps(self.toDict())


class DatosPersistentes:
    """
    Obtén datos actualizados sin tener que estar siempre en línea.

    Esta clase se encarga de descargar y almacenar los últimos
    datos del SIIAU y los almacena localmente.

    Los datos se pueden actualizar si se pasa el parámetro `update`.

    Los centros son de clase CentroUniversitario (ver clase en carga)
    Los calendarios son de clase CalendarioSiiau (ver clase en carga)
    Las materias son de clase RegistroCatalogo (ver clase en este mismo archivo)
    """
    rutaCalendarios = os.path.join(APP_DATA, "calendarios.dat")
    rutaCentros = os.path.join(APP_DATA, "centros.dat")
    rutaCarreras = os.path.join(APP_DATA, "carreras")
    rutaMaterias = os.path.join(APP_DATA, "materias")
    calendarios = []
    centros = []
    carreras = {}
    materias = {}

    def __init__(self):
        dirCal = os.path.dirname(self.rutaCalendarios)
        dirCen = os.path.dirname(self.rutaCentros)

        if not os.path.exists(dirCal):
            os.makedirs(dirCal)

        if not os.path.exists(dirCen):
            os.makedirs(dirCen)

        if not os.path.exists(self.rutaCarreras):
            os.makedirs(self.rutaCarreras)
        
        if not os.path.exists(self.rutaMaterias):
            os.makedirs(self.rutaMaterias)

    def obtenerCalendarios(self, update: bool = False):
        if not self.calendarios or update:
            self._cargarCalendario(update)

        return self.calendarios

    def obtenerCentros(self, update: bool = False):
        if not self.centros or update:
            self._cargarCentros()

        return self.centros

    def obtenerCarreras(self, clave: str, update: bool = False):
        if not self.carreras.get(clave) or update:
            self._cargarCarreras(clave)

        return self.carreras[clave]

    def obtenerMaterias(self, clave: str, update: bool = False):
        if not self.materias.get(clave) or update:
            self._cargarMaterias(clave)

        return self.materias[clave]

    def _cargarCalendario(self, update: bool = False):
        if not os.path.exists(self.rutaCalendarios) or update:
            gc = GeneradorCatalogo()
            gc.generarCatalogoCalendarios(self.rutaCalendarios)

        # Hay que reiniciar si vamos a [re]cargar desde JSON
        self.calendarios = []

        if not os.path.exists(self.rutaCalendarios):
            return

        jsonCalendarios = self._abrirArchivo(self.rutaCalendarios)
        calendarios = sorted(json.loads(jsonCalendarios),
                             key=lambda x: x['clave'], reverse=True)

        for a in calendarios:
            self.calendarios.append(
                CalendarioSiiau(a['clave'], a['calendario']))

    def _cargarCentros(self, update: bool = False):
        if not os.path.exists(self.rutaCentros) or update:
            gc = GeneradorCatalogo()
            gc.generarCatalogoCentros(self.rutaCentros)

        # Hay que reiniciar si vamos a [re]cargar desde JSON
        self.centros = []

        if not os.path.exists(self.rutaCentros):
            return

        jsonCentros = self._abrirArchivo(self.rutaCentros)
        centros = sorted(json.loads(jsonCentros),
                         key=lambda x: x['clave'])

        for u in centros:
            self.centros.append(CentroUniversitario(u['clave'], u['centro']))

    def _cargarCarreras(self, claveCentro: str, update: bool = False):
        # Generamos la ruta al centro que intentamos cargar
        rutaCarrerasCentro = os.path.join(self.rutaCarreras, f"{claveCentro}.dat")

        if not os.path.exists(rutaCarrerasCentro) or update:
            # Si no existe solo pasamos la ruta a la carpeta,
            # ya que la ruta al centro se autogenera
            gc = GeneradorCatalogo()

            gc.generarCatalogoCarreras(self.rutaCarreras, claveCentro)

        # Hay que reiniciar si vamos a [re]cargar desde JSON
        self.carreras[claveCentro] = []

        if not os.path.exists(rutaCarrerasCentro):
            return

        carreras = json.loads(self._abrirArchivo(rutaCarrerasCentro))

        for c in carreras:
            # Iteramos sobre las materias y creamos los objetos
            # RegistroCatalogo que corresponden a las materias
            clave = c.get('clave', c.get('CLAVE'))
            nombre = c.get('materia', c.get('MATERIA', ''))
            depto = c.get('departamento', c.get('DEPTO'))
            self.carreras[claveCentro].append(RegistroCatalogo(clave, nombre, depto))

    def _cargarMaterias(self, claveCentro: str, update: bool = False):
        # Generamos la ruta al centro que intentamos cargar
        rutaMateriaCentro = os.path.join(self.rutaMaterias, f"{claveCentro}.dat")

        if not os.path.exists(rutaMateriaCentro) or update:
            # Si no existe solo pasamos la ruta a la carpeta,
            # ya que la ruta al centro se autogenera
            gc = GeneradorCatalogo()
            gc.generarCatalogoMaterias(self.rutaMaterias, claveCentro)

        # Hay que reiniciar si vamos a [re]cargar desde JSON
        self.materias[claveCentro] = []

        if not os.path.exists(rutaMateriaCentro):
            return

        materias = json.loads(self._abrirArchivo(rutaMateriaCentro))

        for m in materias:
            # Iteramos sobre las materias y creamos los objetos
            # RegistroCatalogo que corresponden a las materias
            clave = m.get('clave', m.get('CLAVE'))
            nombre = m.get('materia', m.get('MATERIA', ''))
            depto = m.get('departamento', m.get('DEPTO'))
            self.materias[claveCentro].append(RegistroCatalogo(clave, nombre, depto))

    def _abrirArchivo(self, filename: str):
        try:
            filename = os.path.expanduser(filename)
            filename = os.path.expandvars(filename)
            filename = os.path.abspath(filename)

            with open(filename, "r") as f:
                datos = f.read()

            return datos

        except IOError:
            import traceback
            print(traceback.format_exc())
            return None


class GeneradorCatalogo:
    ciclos = []
    centros = []
    materias = []
    silent = False

    def __init__(self, silent: bool = True):
        self.silent = silent

    def generarCatalogoAsync(self, tipo: str, ruta: str = "", letraCentro: str = "", update_if_exists: bool = True):
        """
        Opciones válidas para tipo:
        - materiastodas
        - materias
        - centros
        - calendarios
        """
        if tipo == "materiastodas":
            if not ruta:
                ruta = DatosPersistentes.rutaMaterias

            self.generarCatalogoMateriasTodas(ruta, True, update_if_exists)

        elif tipo == "materias" and letraCentro:
            if not ruta:
                ruta = DatosPersistentes.rutaMaterias

            process = Process(target=self.generarCatalogoMaterias,
                              args=(ruta, letraCentro, update_if_exists))
            process.start()
            process.join()

        elif tipo == "centros":
            if not ruta:
                ruta = DatosPersistentes.rutaCentros

            process = Process(target=self.generarCatalogoCentros,
                              args=(ruta, update_if_exists))
            process.start()
            process.join()

        elif tipo == "calendarios":
            if not ruta:
                ruta = DatosPersistentes.rutaCalendarios

            process = Process(target=self.generarCatalogoCalendarios,
                              args=(ruta, update_if_exists))
            process.start()
            process.join()

    def generarCatalogoMateriasTodas(self, ruta: str, multiprocess: bool = True, update_if_exists: bool = True):
        datos = DatosPersistentes()
        centros = datos.obtenerCentros()
        procesos = []

        for centro in centros:
            if multiprocess:
                procesos.append(Process(target=self.generarCatalogoMaterias,
                                        args=(ruta, centro.clave, update_if_exists)))
            else:
                hilo()

        if multiprocess:
            for proceso in procesos:
                proceso.start()

            for proceso in procesos:
                proceso.join()

    def generarCatalogoMaterias(self, carpetaMaterias: str, letraCentro: str, update_if_exists: bool = True):
        archivo = os.path.join(carpetaMaterias, f"{letraCentro}.dat")
        if not self.silent:
            print(f"Generando {archivo}...")

        if os.path.exists(archivo) and not update_if_exists:
            if not self.silent:
                print(f"{archivo} ya existe, saltando...")

        else:
            try:
                params = {
                    'planp': 'Y',
                    'cup': letraCentro,
                    'ordenp': 1,
                    'mostrarp': 5,
                    'tipop': 'D'
                }
                lector = LectorHttp(SIIAU_CATAX, params=params)
                html = lector.getHtml()

                if not html:
                    raise ConnectionError("No hay conexión a internet")

                br = csv.DictReader([x for x in html.split("\n")])
                listado = []

                for entrada in br:
                    registro = RegistroCatalogo(entrada)

                    if not registro.departamento or not registro.nombre or not registro.clave:
                        continue

                    listado.append(registro.toDict())

                listado = sorted(listado, key=lambda x: x['materia'])
                datosSerializados = json.dumps(listado).encode()

                self._guardarArchivo(archivo, datosSerializados)

            except IOError:
                print("Error generando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            except ConnectionError:
                print("Error generando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            finally:
                if not self.silent:
                    print(f"¡{archivo} terminado!")

    def generarCatalogoCentros(self, archivo: str, update_if_exists: bool = True):
        if not self.silent:
            print(f"Generando {archivo}...")

        if os.path.exists(archivo) and not update_if_exists:
            if not self.silent:
                print(f"{archivo} ya existe, saltando...")

        else:
            try:
                respuesta = LectorHttp(SIIAU_FORM, soup=True)
                soup = respuesta.getSoup()

                if soup is None:
                    raise ConnectionError("No hay conexión a internet")

                centrosTag = soup.find(
                    'select', {'name': 'cup'}).findAll('option')
                listaCentros = []

                for x in centrosTag:
                    clave = x['value']
                    centro = re.sub("%s - " % x['value'], '', x.text).strip()
                    listaCentros.append(
                        {
                            "clave": clave,
                            "centro": centro,
                        }
                    )

                datosSerializados = json.dumps(listaCentros).encode()

                self._guardarArchivo(archivo, datosSerializados)

            except ConnectionError:
                print("Error conectando al servidor...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            except IOError:
                print("Error guardando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            except Exception:
                print("Error generando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            finally:
                if not self.silent:
                    print(f"¡{archivo} terminado!")

    def generarCatalogoCalendarios(self, archivo: str, update_if_exists: bool = True):
        if not self.silent:
            print(f"Generando {archivo}...")

        if os.path.exists(archivo) and not update_if_exists:
            if not self.silent:
                print(f"{archivo} ya existe, saltando...")

        else:
            try:
                respuesta = LectorHttp(SIIAU_FORM, soup=True)
                soup = respuesta.getSoup()

                if soup is None:
                    raise ConnectionError("No hay conexión a internet")

                ciclosTag = soup.find(id='cicloID').findAll('option')
                listaCiclos = []

                for x in ciclosTag:
                    clave = x['value']
                    calendario = re.sub("%s - " %
                                        x['value'], '', x.text).strip()
                    listaCiclos.append(
                        {
                            "clave": clave,
                            "calendario": calendario,
                        }
                    )

                datosSerializados = json.dumps(listaCiclos).encode()

                self._guardarArchivo(archivo, datosSerializados)

            except IOError:
                print("Error guardando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            except ConnectionError:
                print("Error conectando al servidor...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            except Exception:
                print("Error generando el archivo...")

                if not self.silent:
                    import traceback
                    print(traceback.format_exc())

            finally:
                if not self.silent:
                    print(f"¡{archivo} terminado!")

    def _guardarArchivo(self, filename: str, datos: bytes):
        filename = os.path.expanduser(filename)
        filename = os.path.expandvars(filename)
        filename = os.path.abspath(filename)

        with open(filename, "wb") as f:
            f.write(datos)
