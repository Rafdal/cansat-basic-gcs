from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from backend.serial.SerialPortHandler import SerialPortHandler
from PyQt5.QtCore import QTimer

class MainModel:

    # Initialization of Model members
    def __init__(self) -> None:
        self.serial = SerialPortHandler()

        self.dest_mac = bytearray([0x00,0x13,0xA2,0x00,0x42,0x28,0xA1,0xB0])  # (Payload Address) para todos los casos


    def xbee_frame_formatter(self, data: str, mac: bytearray) -> bytearray:
        start_delimiter = 0x7E
        frame_type = 0x00
        frame_id = 0x01
        broadcast_radius = 0x00

        #paso a ascii
        data_bytes = data.encode('ascii')

        #aca armo el frame en si
        frame_data = bytearray()
        frame_data.append(frame_type)
        frame_data.append(frame_id)
        frame_data += mac
        frame_data.append(broadcast_radius)
        frame_data += data_bytes

        #qca aclculo longitud para agregarlo al frame
        length = len(frame_data)
        length_msb = (length >> 8) & 0xFF
        length_lsb = length & 0xFF

        # se calcula el checksum
        checksum = 0xFF - (sum(frame_data) & 0xFF)

        # frame completo
        frame = bytearray()
        frame.append(start_delimiter)
        frame.append(length_msb)
        frame.append(length_lsb)
        frame += frame_data
        frame.append(checksum)

        return frame