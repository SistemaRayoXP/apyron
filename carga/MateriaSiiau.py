# -*- coding: utf-8 -*-
"""
Contiene a la clase abstracta MateriaSiiau, que sirve para
obtener materias mediante el LectorSiiau
"""


class MateriaSiiau:
    """
    Clase abstracta MateriaSiiau para representar una materia disponible en el SIIAU.

    Funciona de intermediario para obtener una materia con LectorSiiau
    """
    clave = str()
    centro = str()
    calendario = str()

    def __init__(self, clave: str, centro: str, calendario: str):
        self.clave = clave
        self.centro = centro
        self.calendario = calendario

    def __copy__(self):
        return MateriaSiiau(self.clave, self.centro, self.calendario)

    def __str__(self):
        return "\n".join([
            f"Clave: {self.clave}",
            f"Centro: {self.centro}",
            f"Calendario: {self.calendario}",
        ])

    def getClave(self):
        return self.clave

    def getCentro(self):
        return self.centro

    def getCal(self):
        return self.calendario
