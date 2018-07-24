# -*- coding: utf-8 -*-
from PyQt4.QtGui import QIcon, QPixmap, QAction
from PyQt4.Qt import QObject
from qgis.gui import QgsMessageBar
from qgis.core import QGis
from CriaPoligono import CriaPoligono

class Acquisition(QObject):
    def __init__(self, iface):
        super(Acquisition, self).__init__()
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool = None

    def setPolygonAction(self, action):
        self.polygonAction = action 

    def acquisitionNinetyDegrees(self):
        self.run(CriaPoligono, self.polygonAction)
        
    def run(self, func, action):
        layer = self.canvas.currentLayer()
        if layer in self.iface.editableLayers():
            if layer.geometryType() in [QGis.Line , QGis.Polygon]:
                if self.tool:
                    self.tool.deactivate()
                self.tool = func(self.canvas, self.iface, action)
                self.tool.setAction(action)
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Tool not defined for points'),
                                                                    level=QgsMessageBar.INFO, duration=3)
                self.tool.deactivate() if self.tool else ""
        else:
            self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Start editing in current layer!'), level=QgsMessageBar.INFO, duration=3)
            self.tool.deactivate() if self.tool else ""
                                    
            
