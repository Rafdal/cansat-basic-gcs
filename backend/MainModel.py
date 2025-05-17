from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import typing

from backend.serial.SerialPortHandler import SerialPortHandler
from backend.serial.XbeeTools import XbeeTools

class MainModel(QObject):
    on_error = pyqtSignal(str)                      # Signal for error handling
    on_second_elapsed = pyqtSignal()                # Signal for one second elapsed

    payload_mac = bytearray([0x00,0x13,0xA2,0x00,0x42,0x28,0xA1,0xB0])
    on_data_received = pyqtSignal(str, bytearray)   # Signal for data received (data, mac)

    # Initialization of Model members
    def __init__(self) -> None:
        super().__init__()
        self.serial = SerialPortHandler()
        self.xbee_tools = XbeeTools(dest_mac=self.payload_mac)
        self.timer = QTimer()
        self.__init_signals__()

    def transmit_data(self, data: str):
        """ Send data to the XBee device. """
        frame = self.xbee_tools.frame_formatter(data, self.payload_mac)
        self.serial.send_data(frame)


    def __init_signals__(self):
        self.xbee_tools.on_receive.connect(self.on_data_received.emit)
        self.serial.data_received.connect(self.xbee_tools.push_data)
        self.serial.error.connect(self.on_error.emit)
        self.xbee_tools.on_error.connect(self.on_error.emit)
        self.timer.timeout.connect(self.on_second_elapsed.emit)
        self.timer.start(1000)