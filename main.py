# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

print("Running main.py")

from backend.MainModel import MainModel
from frontend.MainWindow import *
from frontend.pages.MainPage import MainPage
import pyqtgraph as pg


import faulthandler

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('frontend/assets/icon.ico'))
    

    # create a Data Model
    mainModel = MainModel()

    # create pages
    pages = [
        MainPage()
    ]

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(pages[0].update)
    timer.start(500)

    print("Pages created, creating main window")

    ex = MainWindow(pages=pages, model=mainModel, title="Ground Station - SEDS ITBA")

    faulthandler.enable()
    sys.exit(app.exec_())