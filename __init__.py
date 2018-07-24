# -*- coding: utf-8 -*-

def classFactory(iface):
    
    from .CriaPoligono import CriaPoligono
    return CriaPoligono(iface)
