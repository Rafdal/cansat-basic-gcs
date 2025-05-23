import pyqtgraph as pg

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class GraphWidget(QWidget):
    def __init__(self, title, label_x, units_x, label_y, units_y):
        super().__init__()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.title = title
        self.label_x = label_x 
        self.units_x = units_x
        self.label_y = label_y
        self.units_y = units_y
        self.values = np.array([], dtype=np.float64)

        self.pen = pg.mkPen(color=QColor(40, 51, 101), width=2)  
        self.plot = pg.PlotWidget()
        self.plot_item = self.plot.getPlotItem()
        self.plot_item.showGrid(x=True, y=True)
        self.plot_item.setLabel('left', self.label_y, units=self.units_y, **{'font-size': '10pt'})
        self.plot_item.setLabel('bottom', self.label_x, units=self.units_x, **{'font-size': '10pt'})
        self.plot_item.setTitle(self.title, color=QColor(40, 51, 101), size='10pt')
        self.plot_item.vb.setMouseEnabled(x=True, y=False)

        self.curve = self.plot_item.plot(self.values, pen=self.pen, antialias=True)  
        self.curve.setSkipFiniteCheck(True)  # Skip finite check for performance

        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        self.setLayout(layout)

    def clear(self):
        self.values = np.array([], dtype=np.float64)
        self.curve.setData(self.values)

    def update(self, value: np.float64):
        self.values = np.append(self.values, value)
        self.curve.setData(self.values)



class GraphWidgetMultiplot(QWidget):
    def __init__(self, title, label_x, units_x, label_y, units_y):
        super().__init__()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.title = title
        self.label_x = label_x 
        self.units_x = units_x
        self.label_y = label_y
        self.units_y = units_y
        self.plots = {}

        self.plot = pg.PlotWidget()
        self.plot_item = self.plot.getPlotItem()
        self.plot_item.showGrid(x=True, y=True)
        self.plot_item.setLabel('left', self.label_y, units=self.units_y, **{'font-size': '10pt'})
        self.plot_item.setLabel('bottom', self.label_x, units=self.units_x, **{'font-size': '10pt'})
        self.plot_item.setTitle(self.title, color=QColor(40, 51, 101), size='10pt')
        self.plot_item.vb.setMouseEnabled(x=True, y=False)


        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        self.setLayout(layout)

    def clear(self):
        for plot in self.plots.values():
            plot['data'] = np.array([], dtype=np.float64)
            plot['plot_item'].setData(plot['data'])

    def add_plot(self, plot_name: str, color: QColor = QColor(40, 51, 101)):
        pen = pg.mkPen(color=color, width=2)
        self.plot_item.addLegend()
        self.plots[plot_name] = {
            'data': np.array([], dtype=np.float64),
            'plot_item': self.plot_item.plot(np.array([], dtype=np.float64), pen=pen, antialias=True, name=plot_name)
        }
        self.plots[plot_name]['plot_item'].setSkipFiniteCheck(True)  # Skip finite check for performance
        self.plots[plot_name]['plot_item'].setData(self.plots[plot_name]['data'])

    def update(self, plot_name: str, value: np.float64):
        self.plots[plot_name]['data'] = np.append(self.plots[plot_name]['data'], value)
        self.plots[plot_name]['plot_item'].setData(self.plots[plot_name]['data'])
