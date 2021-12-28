# -*- coding: utf-8 -*-
"""
Módulo de la clase AdDatos para almacenar materias de SIIAU
"""

# from gui.ventana import Descarga
# from gui.ventana import Descargas
from carga.Grupo import Grupo
from carga.Horario import Horario
from carga.LectorSiiau import LectorSiiau
from carga.Maestro import Maestro
from carga.Materia import Materia
from carga.MateriaSiiau import MateriaSiiau
from carga.Registro import Registro


class AdDatos:
    """
    Clase AdDatos para descargar y almacenar materias desde SIIAU

    Descarga y administra las materias para la generación de horarios.
    Se deben cargar nuevas materias utilizando cargar(), pasando la
    materia MateriaSiiau a cargar.
    """
    conCupo = bool()
    maxHorarios = int()
    maxHuecos = int()
    maxHuecosInt = int()
    prHora = int()
    prDemanda = int()
    evaluarPeriodos = bool()

    materias = []
    horarioUsuario = None
    descargas = None

    eventos = []
    lectoresSiiau = []

    def __init__(self):
        """Constructor"""
        self.descargas = None
        self.lectoresSiiau = []
        self.eventos = []
        self.materias = []
        self.horarioUsuario = Horario().getHorarioLleno()
        self.conCupo = True
        self.maxHorarios = 50000
        self.maxHuecos = -1
        self.maxHuecosInt = -1
        self.prDemanda = -1
        self.prHora = -1
        self.evaluarPeriodos = False

    def getDescargas(self):
        return self.descargas

    """""""""""""""""""""""""""""""""""""""
    =======================================
      Métodos para acceder a los registros
    =======================================
    """""""""""""""""""""""""""""""""""""""

    def buscarMateria(self, obj):
        """
        Si la materia se encuentra, regresa un valor positivo
        indicando el indice del vector.
        NOTE: Lo de abajo no tiene mucho sentido en la forma en que lo
        implementé, así que por ahora si no se encuentra se salta y ya
        ~~De lo contrario, regresa un
        valor negativo indicando donde se encuentra el siguiente lugar
        donde deberia estar.~~
        """

        for x, materia in enumerate(self.materias):
            if str(obj) in str(materia):
                if str(obj) == str(materia):
                    return x
                # else:
                #     return -(x + 1)

        return (len(self.materias) + 1) * -1

    def inserta(self, reg: Registro, f: MateriaSiiau):
        """
        Inserta un registro, si ya existe lo sobreescribe
        """
        tmpMateria = None
        tmpMaestro = None
        tmpGrupo = None

        # Buscamos si ya existe la materia en los datos
        tmp = self.buscarMateria(reg.materia)

        # No existe la materia
        if tmp < 0:
            # Ajustar el indice
            tmp *= -1
            tmp -= 1

            tmpMateria = Materia()
            tmpMateria.fuente = f
            tmpMateria.creditos = reg.creditos
            tmpMateria.nombre = reg.materia

            self.materias.append(tmpMateria)

        # La materia ya existe
        else:
            tmpMateria = self.materias[tmp]

        # Buscamos si ya existe el maestro en los datos
        tmp = tmpMateria.buscarMaestro(reg.profesor)

        if tmp < 0:
            tmp *= -1
            tmp -= 1
            tmpMaestro = Maestro(tmpMateria)
            tmpMaestro.nombre = reg.profesor
            tmpMateria.maestros.append(tmpMaestro)
        else:
            tmpMaestro = tmpMateria.maestros[tmp]

        tmpGrupo = tmpMaestro.buscarGrupo(reg.nrc)

        if tmpGrupo is None:
            tmpGrupo = Grupo(tmpMaestro)
            tmpMaestro.grupos.append(tmpGrupo)

        tmpGrupo.cup = int(reg.cupo)
        tmpGrupo.dis = int(reg.disponible)
        tmpGrupo.nrc = reg.nrc
        tmpGrupo.sec = reg.seccion
        tmpGrupo.horario = reg.horario

    def cargar(self, ms: MateriaSiiau):
        """
        Obtiene el html de SIIAU a determinado ciclo, cientro y clave
        """

        ls = LectorSiiau(ms)

        for reg in ls.registros:
            self.inserta(reg, ms)

        for x, e in enumerate(list(self.eventos)):
            # Procesamos y descartamos el evento
            self.eventos.pop(x)()
