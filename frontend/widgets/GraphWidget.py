import pyqtgraph as pg

from PyQt5.QtGui import QColor
import numpy as np

class GraphWidget():
    def __init__(self, title, label_x, units_x, label_y, units_y):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.title = title
        self.label_x = label_x 
        self.units_x = units_x
        self.label_y = label_y
        self.units_y = units_y
        self.values = np.array([])

        self.pen = pg.mkPen(color=QColor(40, 51, 101), width=2)  
        self.plot = pg.plot()
        self.plot_item = self.plot.getPlotItem()
        self.plot_item.showGrid(x=True, y=True)
        self.plot_item.setLabel('left', self.label_y, units=self.units_y)
        self.plot_item.setLabel('bottom', self.label_x, units=self.units_x)

        self.curve = self.plot.plot(pen=self.pen, antialias=True)

    def update(self, value: float):
        # self.values.append(value)
        self.values = np.append(self.values, value)
        self.curve.setData(self.values)
