from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from backend.serial.SerialPortHandler import SerialPortHandler
from PyQt5.QtCore import QTimer

class MainModel:

    # Initialization of Model members
    def __init__(self) -> None:
        self.serial = SerialPortHandler()

        self.dest_mac = bytearray([0x00,0x13,0xA2,0x00,0x42,0x28,0xA1,0xB0])  # (Payload Address) para todos los casos

    def xbee_frame_parser(self, frame: bytearray) -> str:
        print("From CanSat Xbee: "+" ".join(f"{byte:02X}" for byte in frame))

        # Parse the frame (codigo)
    def xbee_frame_analyzer(frame: bytearray): 
        if len(frame) < 4 or frame[0] != 0x7E:
            print("Error: Frame inválido o no comienza con 0x7E.")
            return

        print(f"Byte(s)\t\tValor\t\t\tSignificado")
        print(f"0x7E\t\t0x7E\t\t\tStart delimiter")

        length = (frame[1] << 8) | frame[2]
        print(f"0x{frame[1]:02X} 0x{frame[2]:02X}\t{length} bytes\t\tLongitud del frame data")

        if len(frame) != 3 + length + 1:
            print(f"Error: El largo real del frame ({len(frame)}) no coincide con la longitud declarada ({length}).")
            return

        frame_data = frame[3:3+length]
        checksum_sender = frame[-1]

        print(f"0x{frame[3]:02X}\t\tFrame type: 0x{frame[3]:02X}")
        print(f"0x{frame[4]:02X}\t\tFrame ID: {frame[4]}")

        mac_bytes = frame[5:13]
        mac_str = ' '.join(f'0x{b:02X}' for b in mac_bytes)
        print(f"{mac_str}\tMAC destino")

        options = frame[13]
        print(f"0x{options:02X}\t\tOpciones / Broadcast radius")

        payload = frame[14:-1]
        payload_ascii = ''.join(chr(b) for b in payload if 32 <= b <= 126)
        payload_hex = ' '.join(f'0x{b:02X}' for b in payload)
        print(f"{payload_hex}\tPayload (ASCII): '{payload_ascii}'")
        #print(f"Mensaje recibido (hex): {payload_hex}")
        print(f"Mensaje recibido (esp): {payload_ascii}")

        print(f"0x{checksum_sender:02X}\t\tChecksum recibido")

        checksum_calc = 0xFF - (sum(frame_data) & 0xFF)
        print(f"0x{checksum_calc:02X}\t\tChecksum calculado")

        if checksum_sender == checksum_calc:
            print("Checksum válido.")
        else:
            print("Checksum inválido.")


        pass # borrar

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