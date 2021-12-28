# -*- coding: utf-8 -*-
"""
Clase Horario para administrar horarios del SIIAU
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from carga . Periodo import Periodo


class Horario(object):
    bit = [1, 2, 4, 8, 16, 32, 64, 128, 256,
           512, 1024, 2048, 4096, 8192, 16384]
    total = int()
    ultimosHuecos = int()
    periodoString = str()
    periodo = None

    modulos = []
    horario = []
    aulas = []

    def __init__(self, horas: list = []):
        self.modulos = ['', '', '', '', '', '']
        self.horario = horas if len(horas) == 6 else [0, 0, 0, 0, 0, 0]
        self.aulas = ['', '', '', '', '', '']
        self.total = 0

    def getPeriodo(self):
        return self.periodo

    def getHorario(self, i: int = -1):
        return self.horario[i] if i != -1 else self.horario

    def setPeriodo(self, periodo: str):
        self.periodoString = periodo
        # tz_mexico = timezone(timedelta(hours=-6))

        try:
            fechas = periodo.split(" - ")
            inicio = datetime.strptime(
                fechas[0], "%d/%m/%y")
            fin = datetime.strptime(
                fechas[1], "%d/%m/%y")

            # Error
            if not inicio < fin:
                raise Exception("Error: {} no es menor que {}".format(
                    fechas[0], fechas[1]))

            self.periodo = Periodo(inicio, fin)
        except Exception as e:
            # Nada que hacer, quiza algun problema de SIIAU
            import traceback
            print(traceback.format_exc())

    def getPeriodoString(self):
        return self.periodoString

    def getHorarioLleno(self):
        tmp = Horario()

        for c_bit in self.bit:
            tmp.horario[0] += c_bit

        tmp.horario[1] = tmp.horario[0]
        tmp.horario[2] = tmp.horario[0]
        tmp.horario[3] = tmp.horario[0]
        tmp.horario[4] = tmp.horario[0]
        tmp.horario[5] = tmp.horario[0]
        return tmp

    def getHorarioTotal(self):
        if self.total == 0:
            self.total = sum(self.horario)
        return self.total

    def getHuecos(self, h: int):
        tmp = 0
        inicio = -1
        fin = 0

        # Calcular inicio
        for c_bit in self.bit:
            if (h & c_bit) != 0:
                inicio = x
                break

        if inicio > -1:
            # Calcular fin
            for c_bit in reversed(self.bit):
                if (h & c_bit) != 0:
                    fin = x
                    break

            # Calcular huecos
            # for x in range(inicio, fin + 1):
            for c_bit in self.bit[inicio:fin + 1]:
                if (h & c_bit) == 0:
                    tmp += 1

        else:
            return 0

        return tmp

    def getHuecos(self):
        if self.total == 0:

            self.total = sum(self.horario)

            self.ultimosHuecos = sum([
                self.getHuecos(self.horario[0]),
                self.getHuecos(self.horario[1]),
                self.getHuecos(self.horario[2]),
                self.getHuecos(self.horario[3]),
                self.getHuecos(self.horario[4]),
                self.getHuecos(self.horario[5])
            ])

        return self.ultimosHuecos

    def agregar(self, h):
        self.total = 0
        for x in range(6):
            self.horario[x] += h.horario[x]

    def quitar(self, h):
        self.total = 0
        for x in range(6):
            self.horario[x] -= h.horario[x]

    def __copy__(self):
        h = Horario()
        h.periodoString = self.periodoString
        h.total = self.total
        h.ultimosHuecos = self.ultimosHuecos
        h.periodo = self.periodo

        for x in range(6):
            h.aulas[x] = self.aulas[x]
            h.modulos[x] = self.modulos[x]
            h.horario[x] = self.horario[x]

    def getHora(self, idx1: int, idx2: int):
        idx2 -= 7
        return (self.horario[idx1] & self.bit[idx2]) != 0

    def setHora(self, idx1: int, idx2: int, marca: bool):
        self.total = 0
        idx2 -= 7

        if marca:
            self.horario[idx1] = self.horario[idx1] | self.bit[idx2]
        else:
            if (self.horario[idx1] & self.bit[idx2]) != 0:
                self.horario[idx1] = self.horario[idx1] ^ self.bit[idx2]

    def compatible(self, h):
        for x in range(6):
            if (h.horario[x] & self.horario[x]) != 0:
                return False

        return True

    def subHorario(self, h):
        for x in range(6):
            if (h.horario[x] & self.horario[x]) != self.horario[x]:
                return False

        return True

    def limpiar(self):
        self.horario = [0, 0, 0, 0, 0, 0]
        self.total = 0

    def __str__(self):
        tmp = []
        for x, dia in enumerate(self.horario):
            if dia != 0:
                cases = {
                    0: "Lunes: {}".format(self.int2hora(dia)),
                    1: "Martes: {}".format(self.int2hora(dia)),
                    2: "Miércoles: {}".format(self.int2hora(dia)),
                    3: "Jueves: {}".format(self.int2hora(dia)),
                    4: "Viernes: {}".format(self.int2hora(dia)),
                    5: "Sábado: {}".format(self.int2hora(dia)),
                }
                tmp.append(cases.get(x, tmp))

        tmp = " - ".join(tmp)

        return tmp

    def int2hora(self, h: int):
        desde = 0
        hasta = 0
        x = int()

        if h == 0:
            return ""

        for x, c_bit in enumerate(self.bit):
            if (h & c_bit) != 0:
                desde = x
                break

        for x, c_bit in enumerate(self.bit):
            if (h & c_bit) != 0:
                hasta = x + 1
                break

        if hasta == desde:
            return "{}:00".format(desde + 7)
        else:
            return "{}:00-{}:55".format(desde + 7, hasta + 7)

    def hora2int(self, hora: str):
        sep = hora.index('-')

        # El -7 es para que las horas queden relativas a 0
        desde = int(hora[0:sep][0:2]) - 7
        hasta = int(hora[sep + 1:][0:2]) - 7
        tmp = 0

        for x in range(desde, hasta + 1):
            tmp += self.bit[x]

        return tmp

    def setDatos(self, dias: str, modulo: str, aula: str, horas: str):
        self.total = 0

        h = self.hora2int(horas)

        for x in dias:
            if x == 'L':
                self.modulos[0] = modulo
                self.aulas[0] = aula
                self.horario[0] += h

            elif x == 'M':
                self.modulos[1] = modulo
                self.aulas[1] = aula
                self.horario[1] += h

            elif x == 'I':
                self.modulos[2] = modulo
                self.aulas[2] = aula
                self.horario[2] += h

            elif x == 'J':
                self.modulos[3] = modulo
                self.aulas[3] = aula
                self.horario[3] += h

            elif x == 'V':
                self.modulos[4] = modulo
                self.aulas[4] = aula
                self.horario[4] += h

            elif x == 'S':
                self.modulos[5] = modulo
                self.aulas[5] = aula
                self.horario[5] += h
