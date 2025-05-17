from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, QDialogButtonBox, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from backend.MainModel import MainModel

from frontend.widgets.SerialPortMenu import SerialPortMenuDialog

def create_menu_bar(main: QMainWindow, menuBar: QMenuBar, model: MainModel):
    fileMenu = menuBar.addMenu('&File')
    
    exitAction = QAction(QIcon('exit.png'), '&Exit', main)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(main.close)

    fileMenu.addAction(exitAction)

    # Add a "Serial Port" menu
    serialMenu = menuBar.addMenu('&Serial')

    openSerialAction = QAction('&Open Serial Port', main)
    openSerialAction.triggered.connect(lambda: SerialPortMenuDialog(model.serial).exec_())
    closeSerialAction = QAction('&Close Port', main)
    closeSerialAction.setEnabled(False)  # Initially disabled, will be enabled when a port is open
    closeSerialAction.triggered.connect(lambda: confirm_close_port(main, model))
    killPortAction = QAction('&Kill Port', main)
    killPortAction.setEnabled(False)  # Initially disabled, will be enabled when a port is open
    killPortAction.triggered.connect(lambda: confirm_kill_port(main, model))
    serialMenu.addAction(openSerialAction)
    serialMenu.addAction(closeSerialAction)
    serialMenu.addSeparator()  # Add a separator for better organization
    serialMenu.addAction(killPortAction)

    model.serial.connected.connect(lambda status: closeSerialAction.setEnabled(status))
    model.serial.connected.connect(lambda status: killPortAction.setEnabled(status))

    print("Menu bar created")


def confirm_close_port(parent, model):
    """Show confirmation dialog before closing port"""
    port_name = model.serial.port_name if hasattr(model.serial, 'port_name') else "current port"
    reply = QMessageBox.question(
        parent, 
        'Close Port Confirmation',
        f'Are you sure you want to close {port_name}?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        model.serial.disconnect()

def confirm_kill_port(parent, model):
    """Show confirmation dialog before killing port"""
    port_name = model.serial.port_name if hasattr(model.serial, 'port_name') else "current port"
    reply = QMessageBox.warning(
        parent, 
        'Kill Port Confirmation',
        f'Are you sure you want to kill {port_name}?\nThis should only be used if the port is unresponsive.',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        model.serial.kill_port()