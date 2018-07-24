# -*- coding: utf-8 -*-

import os                                                                         

from PyQt4 import QtGui, uic 
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL, Qt
import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence, QIcon, QPixmap, QAction
from PyQt4.QtCore import QSettings
from geometricaAquisition import GeometricaAcquisition
from qgis.core import QgsPoint, QGis, QgsGeometry
from qgis.gui import QgsMapMouseEvent, QgsMapTool, QgsMessageBar
from PyQt4.Qt import QObject
from qgis.gui import QgsMapToolEmitPoint

class CriaPoligono(GeometricaAcquisition):
    
    def __init__(self, canvas, iface, action):
        super(CriaPoligono, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface

    def endGeometry(self):
        if len(self.geometry) > 2:
            inter = self.lineIntersection(self.geometry[1],self.geometry[0],self.geometry[-2],self.geometry[-1])
            if inter:
                if self.iface.activeLayer().geometryType() == QGis.Polygon:
                    geom = QgsGeometry.fromPolygon([self.geometry+[inter]])
                elif self.iface.activeLayer().geometryType() == QGis.Line:
                    geom = QgsGeometry.fromPolyline(self.geometry+[inter])
                self.rubberBand.setToGeometry(geom,None)
                self.createGeometry(geom)

    def endGeometryFree(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QGis.Polygon:
                geom = QgsGeometry.fromPolygon([self.geometry])
            elif self.iface.activeLayer().geometryType() == QGis.Line:
                geom = QgsGeometry.fromPolyline(self.geometry + [self.geometry[0]])
            self.rubberBand.setToGeometry(geom, None)
            self.createGeometry(geom)
  
    def canvasReleaseEvent(self, event):
        event.snapPoint(QgsMapMouseEvent.SnapProjectConfig) #snap!!!
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
        pointMap = QgsPoint(event.mapPoint())
        # pointMap = self.snapToLayer(event) 
        if event.button() == Qt.RightButton:
            if self.free:
                self.geometry.append(pointMap)
                self.endGeometryFree()
            else:
                self.endGeometry()        
        elif self.free:
            self.geometry.append(pointMap)
            self.qntPoint += 1
        else:
            if event.button() == Qt.LeftButton:
                if self.qntPoint == 0:
                    self.rubberBand = self.getRubberBand()
                    point = QgsPoint(pointMap)
                    self.geometry.append(point)
                elif self.qntPoint == 1:
                    point = QgsPoint(pointMap)
                    self.geometry.append(point)
                else:
                    point = QgsPoint(pointMap)
                    testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if testgeom:
                        self.geometry.append(QgsPoint(testgeom.x(), testgeom.y()))        
                self.qntPoint += 1
               
    def canvasMoveEvent(self, event):
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand = None
        oldPoint = QgsPoint(event.mapPoint())
        event.snapPoint(QgsMapMouseEvent.SnapProjectConfig)
        point = QgsPoint(event.mapPoint())
        if oldPoint != point:
            self.createSnapCursor(point)
        point = QgsPoint(event.mapPoint())   
        if self.qntPoint == 1:
            geom = QgsGeometry.fromPolyline([self.geometry[0], point])
            self.rubberBand.setToGeometry(geom, None)
        elif self.qntPoint >= 2:
            if self.free:
                geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(point.x(), point.y())]])
                self.rubberBand.setToGeometry(geom, None)             
            else:        
                testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                if testgeom:
                    geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(testgeom.x(), testgeom.y())]])
                    self.rubberBand.setToGeometry(geom, None)




# class PointMapTool (QgsMapToolEmitPoint):

#     def __init __ (self, canvas):

#         self.canvas = canvas
#         QgsMapToolEmitPoint .__ init __ (self, self.canvas)
#         self.point = Nenhum
#         defcanvasPressEvent (self, e):
#         self.point = self.toMapCoordinates (e.pos ())
#         printself.point.x (), self.point.y ()
#         m = QgsVertexMarker (self.canvas)
#         m.setCenter (self.point)
#         m.setColor (QColor (0,255,0))
#         m.setIconSize (5)
#         m.setIconType (QgsVertexMarker.ICON_BOX) # ou ICON_CROSS, ICON_X
#         m.setPenWidth (3)


# class Acquisition(QObject):
    
#     def __init__(self, iface):
#         super(Acquisition, self).__init__()
#         self.iface = iface
#         self.canvas = iface.mapCanvas()
#         self.tool = None

#     def setPolygonAction(self, action):
#         self.polygonAction = action 

#     def acquisitionNinetyDegrees(self):
#         self.run(CriaPoligono, self.polygonAction)
        
#     def run(self, func, action):
#         layer = self.canvas.currentLayer()
#         if layer in self.iface.editableLayers():
#             if layer.geometryType() in [QGis.Line , QGis.Polygon]:
#                 if self.tool:
#                     self.tool.deactivate()
#                 self.tool = func(self.canvas, self.iface, action)
#                 self.tool.setAction(action)
#                 self.canvas.setMapTool(self.tool)
#             else:
#                 self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Tool not defined for points'),
#                                                                     level=QgsMessageBar.INFO, duration=3)
#                 self.tool.deactivate() if self.tool else ""
#         else:
#             self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Start editing in current layer!'), level=QgsMessageBar.INFO, duration=3)
#             self.tool.deactivate() if self.tool else ""
                                    
            
