# -*- coding: utf-8 -*-
"""
Básicamente, es la parte que descarga las páginas
"""

import requests
from bs4 import BeautifulSoup as bs

from http import cookiejar
from collections import OrderedDict as odict

from util.Constants import *

SILENT_MODE = not DEBUG_MODE


class LectorHttp:
    """
    Realiza peticiones HTTP y devuelve los datos asociados a la respuesta.
    Puede realizar peticiones GET y POST, cookies no implementadas
    """
    error = None
    soup = None
    html = None

    def __init__(self,
                 url,
                 params: dict = {},
                 data: dict = {},
                 soup: bool = False,
                 silent: bool = SILENT_MODE,
                 headers: dict = {},
                 debug: bool = False,
                 **requests_args,
                 ):
        # Variables de control internas
        self.abortar = False
        self.cookies = cookiejar.CookieJar()
        self.html = ""
        self.default_headers = odict(
            {
                'User-Agent':
                'Mozilla/7.6 (Windows NT 14.2; Macintosh; X11; U; Intel Mac OS X; PPC Mac OS X;'
                ' Linux x86_64; X12; XXX; x64; win64; ReactOS; rv169.9) AppleWebKit/696.9.69 '
                '(KHTML, like Gecko) Gecko/20100101 Version/16.9 Presto/6.9.699 Firefox/169.9 '
                'Chromium/169.9.6969.699 Safari/696.9.69 Edge/69.69699 OPR/169.9.6969.669 '
                'Edg/169.9.6969.699 TuMami/69.69'
            }
        )

        # Parámetros de la creación del objeto
        self.url = url
        self.data = data
        self.params = params
        self.retSoup = soup
        self.silent = silent
        self.headers = headers
        self.debug = debug
        self.kwargs = requests_args

        try:
            self.makeRequest()

        except requests.exceptions.ConnectionError:
            print("No hay conexión a internet")

            if not self.silent:
                import traceback
                print(traceback.format_exc())

        except Exception:
            print("Ocurrió un error no procesado al intentar realizar la petición")

            # TODO: Implementar estos métodos para informar del resultado de la petición
            # self.error("Error: Sin respuesta del servidor")
            # self.error("Error: No se encuentra el servidor")
            # self.error("Error: No se encuentra el servidor")

            if not self.silent:
                import traceback
                print(traceback.format_exc())

    def getCode(self):
        return self.response.status_code

    def getHeaders(self):
        return self.response.headers

    def getSoup(self):
        return self.soup

    def getHtml(self):
        return self.html

    def makeRequest(self):
        """Hace la petición a la url con los parámetros
        previamente establecidos y almacena la respuesta"""
        # Datos provistos por el usuario
        url = self.url
        data = self.data
        params = self.params
        silent = self.silent
        headers = self.headers
        debug = self.debug
        kwargs = self.kwargs

        # Parámetros internos para la petición
        def_headers = self.default_headers
        session = requests.sessions.Session()
        session.cookies = self.cookies

        if headers:
            def_headers.update(headers)

        if data is not None:
            response = session.post(
                url, data=data, params=params, headers=def_headers, **kwargs)
        else:
            response = session.get(
                url, params=params, headers=def_headers, **kwargs)

        if not silent and response.status_code > 399:
            print("Error obteniendo la url: {}".format(response.status_code))

        if debug:
            print(response.text)

        self.data = response.content
        self.html = response.text

        if self.retSoup:
            self.soup = bs(self.html, "html5lib")

        self.response = response

        return True
