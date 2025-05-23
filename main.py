# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

print("Running main.py")

from backend.MainModel import MainModel
from frontend.MainWindow import *
from frontend.pages.MainPage import MainPage
import pyqtgraph as pg

from frontend.pages.SerialTestPage import SerialTestPage

import faulthandler
import cProfile

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('frontend/assets/icon.png'))
    

    # create a Data Model
    mainModel = MainModel()

    # create pages
    pages = [
        MainPage(),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        SerialTestPage(),
    ]

    print("Pages created, creating main window")

    ex = MainWindow(pages=pages, model=mainModel, title="Ground Station - SEDS ITBA")

    faulthandler.enable()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # cProfile.run('main()', 'profiling_results.prof')
    # import pstats
    # p = pstats.Stats('profiling_results.prof')
    # p.sort_stats('cumulative').print_stats(10)
    main()