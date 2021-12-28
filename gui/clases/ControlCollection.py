# -*- coding: utf-8 -*-
"""
Módulo ControlCollection para almacenar controles Qt en un objeto
"""

class ControlCollection:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    
    def __getattr__(self, name):
        return None
