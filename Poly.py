
actionPolig = QAction("Poligono",self)
actionPolig.setCheckable(True)

self.connect(actionPolig, SIGNAL("triggered()"), self.poly)
self.toolbar.addAction(actionPoly)
self.toolPoly = PolyMapTool(self.canvas)
self.toolPoly.setAction(actionPoly)
self.poly ()

def poly(self):
    self.canvas.setMapTool(self.toolPoly)   


Poly(QgsMapToolEmitPoint):
    
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberband = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberband.setColor(Qt.red)
        self.rubberband.setWidth(1)
        self.point = None
        self.points = []

    def canvasPressEvent(self, e):
        self.point = self.toMapCoordinates(e.pos())
        m = QgsVertexMarker(self.canvas)
        m.setCenter(self.point)
        m.setColor(QColor(0,255,0))
        m.setIconSize(5)
        m.setIconType(QgsVertexMarker.ICON_BOX)
        m.setPenWidth(3)
        self.points.append(self.point)
        self.isEmittingPoint = True
        self.showPoly()
        
    def showPoly(self):
        self.rubberband.reset(QGis.Polygon)
        for point in self.points[:-1]:
        self.rubberband.addPoint(point, False)
        self.rubberband.addPoint(self.points[-1], True)
        self.rubberband.show()