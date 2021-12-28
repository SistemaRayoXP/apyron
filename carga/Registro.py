# -*- coding: utf-8 -*-
"""
Contiene a la clase Registro para administrar una configuración de
materia única (NRC)
"""

from carga . Horario import Horario


class Registro():
    """
    Clase abstracta Registro para representar una configuración única de
    materia, sección, horario, periodo y profesor.
    """
    nrc = ""
    clave = ""
    materia = ""
    seccion = ""
    creditos = ""
    cupo = ""
    disponible = ""
    profesor = ""
    periodo = None

    horario = None

    def __init__(self, h: Horario = None):
        self.horario = Horario()

    def __str__(self):
        msg = \
            "\n".join([
                f"NRC: {self.nrc}",
                f"Clave: {self.clave}",
                f"Materia: {self.materia}",
                f"Seccion: {self.seccion}",
                f"Creditos: {self.creditos}",
                f"Cupo: {self.cupo}",
                f"Disponible: {self.disponible}",
                f"Periodo: {self.periodo}",
                f"Horario: {self.horario}",
                f"Profesor: {self.profesor}",
                f"",
            ])
        return msg
