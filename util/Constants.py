# -*- coding: utf-8 -*-
"""
Módulo de variables constantes que se utilizan en todo el programa (o eso se supone)

TODO: Mover variables de uso global aquí e importar el archivo de constantes
"""
import os


# NOTE: El servidor 1 (siiauescolar) no es compatible con
#       el código existente, reqiere código específico de
#       scraping que no pienso hacer por ahora.
SIIAU1 = "http://siiauescolar.siiau.udg.mx"

# NOTE: El servidor 2 es muy lento en CATAX, sería bueno
#       cambiar la estrategia de obtención de catálogos
#       de materias.
SIIAU2 = "http://consulta.siiau.udg.mx"

# NOTE: El servidor 3 no tiene la página CATAX,
# por lo que su uso para generar catálogos se
# descarta, aunque para obtener materias puede
# que funcione mejor
SIIAU3 = "http://electoral1.udg.mx"

# Por ahora usamos el s. 2, igual que Apeiron
SIIAU_SERVER = SIIAU2

SIIAU_FORM = f"{SIIAU_SERVER}/wco/sspseca.forma_consulta"
SIIAU_CONSUL = f"{SIIAU_SERVER}/wco/sspseca.consulta_oferta"
SIIAU_CATAX = f"{SIIAU_SERVER}/wco/scpcata.cataxcu"
SIIAU_CARR = f"{SIIAU_SERVER}/wco/sspseca.lista_carreras"

DEBUG_MODE = True

# APP_NAME = "Transformador Esquemático y Traductor de Agendas del SIIAU"
# APP_NAME = "Aypatrón - En Python con Qt"
APP_NAME = "Apyron - Escrito en Python con Qt"
APP_WEBSITE = "https://sistemarayoxp.github.io/apyron"

# Es esencial definir el directorio de trabajo como donde se ubica run.py
APP_FOLDER = os.path.dirname(os.path.dirname(__file__))
print(APP_FOLDER)
APP_DATA = os.path.join(APP_FOLDER, "data")
APP_RES = os.path.join(
    APP_FOLDER, "gui", "recursos"
)

APP_ICON_PATH = os.path.join(
    APP_RES, "app.ico"
)
APP_SPLASH_PATH = os.path.join(
    APP_RES, "splash.png"
)
APP_ABOUTPIC_PATH = APP_SPLASH_PATH
