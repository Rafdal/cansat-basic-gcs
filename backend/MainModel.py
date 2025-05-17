from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from backend.serial.SerialPortHandler import SerialPortHandler
from PyQt5.QtCore import QTimer

from typing import Tuple, Union

class MainModel:

    # Initialization of Model members
    def __init__(self) -> None:
        self.serial = SerialPortHandler()

        self.payload_mac = bytearray([0x00,0x13,0xA2,0x00,0x42,0x28,0xA1,0xB0])

    def xbee_frame_analyzer(self, frame: bytearray) -> Tuple[str, bytearray]:
        """
        Analyzes an XBee frame and extracts the payload and MAC address.
        """
        if frame[0] != 0x7E or len(frame) < 6:
            print("Error: Frame no comienza con 0x7E o es demasiado corto.")
            return None, None

        length = (frame[1] << 8) | frame[2]
        if len(frame) != 3 + length + 1:
            print(f"Error: El largo real del frame ({len(frame)}) no coincide con la longitud declarada ({length}).")
            print(f"\tFrame: {self.bytes_to_str(frame)}")
            print(f"\t0x{frame[1]:02X} 0x{frame[2]:02X}\t= {length} bytes")
            return None, None

        frame_data = frame[3:3+length]
        checksum_sender = frame[-1]
        match frame[3]: # Frame type
            case 0x00:
                # print("(Transmit)")
                pass
            case 0x89:
                # print("(TX Status)")
                status = frame[5]
                if status == 0x00:
                    # print("(TX Status: OK)")
                    pass
                else:
                    print(f"(TX Status: Error {status})")
                    return None, None
                pass
            case 0x90:
                # print("(Receive)")
                pass
            case _:
                print(f"0x{frame[3]:02X}\t\tFrame type: 0x{frame[3]:02X}", end='\t')
                print("(TX Status: Desconocido)")

        checksum_calc = 0xFF - (sum(frame_data) & 0xFF)
        if checksum_sender == checksum_calc:
            # print("(Valido)")
            pass
        else:
            print("Checksum INVALIDO")
            print(f"\tChecksum: 0x{checksum_sender:02X} != 0x{checksum_calc:02X}")
            print(f"\tFrame: {self.bytes_to_str(frame, prefix='')}")
            return None, None

        match frame[3]: # Frame type
            case 0x00:
                pass
            case 0x89:
                pass
            case 0x90:
                return self.xbee_extract_packet_data(frame)
            case _:
                pass
        return None, None

    def bytes_to_str(self, data: bytearray, prefix: str = "0x", delimiter: str = " ") -> str:
        """Converts bytes to a formatted string."""
        return delimiter.join(f'{prefix}{b:02X}' for b in data)

    def xbee_extract_packet_data(self, frame: bytearray) -> Tuple[str, bytearray]:
        """
        Extracts the payload and MAC address from an XBee receive frame.
        Args:
            frame (bytearray): The XBee receive frame.
        Returns:
            packet_data (Tuple[str, bytearray]): A tuple containing the payload as a string and the MAC address as a bytearray.
        """
        mac_bytes = frame[5:13]
        payload = frame[14:-1]
        payload_ascii = payload.decode('ascii', errors='ignore')
        return payload_ascii, mac_bytes

    def xbee_frame_formatter(self, data: str, mac: bytearray) -> bytearray:
        if not isinstance(mac, bytearray) or len(mac) != 8:
            raise ValueError("MAC debe ser un bytearray de 8 bytes.")
        start_delimiter = 0x7E
        frame_type = 0x00
        frame_id = 0x01
        broadcast_radius = 0x00

        # paso a ascii
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