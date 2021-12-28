# -*- coding: utf-8 -*-
"""
Módulo de la clase CalendarioSiiau para administrar
centros universitarios como objetos
"""


class CalendarioSiiau:
    nombre = str()
    clave = str()

    def __init__(self, clave: str, nombre: str = ""):
        self.clave = clave
        self.nombre = nombre

    def __str__(self):
        if self.nombre:
            return self.nombre
        else:
            return self.clave

    def obtenerClave(self):
        return self.clave

    def __eq__(self, o):
        if isinstance(o, CalendarioSiiau):
            return o.clave == self.clave

        elif isinstance(o, str):
            return o == self.clave

        return NotImplemented
