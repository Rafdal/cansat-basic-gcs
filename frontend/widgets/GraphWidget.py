import pyqtgraph as pg

from PyQt5.QtGui import QColor

class GraphWidget():
    def __init__(self, title, label_x, units_x, label_y, units_y):
        
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        self.title = title
        self.label_x = label_x 
        self.units_x = units_x
        self.label_y = label_y
        self.units_y = units_y
        self.values = []

        self.pen = pg.mkPen(color=QColor(150, 0, 150), width=2)  

        self.plot = pg.plot()

        self.plot.showGrid(x = True, y = True)
        self.plot.setLabel('left', self.label_y, units = self.units_y)
        self.plot.setLabel('bottom', self.label_x, units = self.units_x)

    def update(self, value):
        self.values.append(value)
        self.plot.plot(self.values, pen = self.pen)
        