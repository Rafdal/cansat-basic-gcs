from PyQt5.QtCore import pyqtSignal, QObject
from typing import Tuple, Union

XBEE_FRAME_TYPE_TX_REQUEST_64   = 0x00 # Transmit Request (64-bit address)
XBEE_FRAME_TYPE_RX_PACKET_64    = 0x80 # Receive Packet (64-bit address)
XBEE_FRAME_TYPE_TX_STATUS       = 0x89 # Transmit Status
XBEE_FRAME_TYPE_ERROR           = 0xFE # Error Frame
XBEE_FRAME_TYPE_RECEIVE         = 0x90 # Receive Request (16-bit address)

class XbeeFrame:
    frame_type: int  # Type of the frame (e.g., 0x00 for Transmit Request, 0x90 for Receive Packet)
    mac: bytearray
    payload: str
    status: int
    def __init__(self, frame_type: int = 0, mac: bytearray = bytearray(), payload: str = "", status: int = 0):
        self.frame_type = frame_type
        self.mac = mac
        self.payload = payload
        self.status = status

class XbeeTools(QObject):
    on_error = pyqtSignal(str)  # Signal for error handling
    on_receive = pyqtSignal(str, bytearray)  # Signal for data received
    """
    Clase para manejar frames de XBee y extraer datos de ellos.
    """
    def __init__(self, dest_mac: bytearray = None, start_delimiter: int = 0x7E) -> None:
        super().__init__()
        """
        Inicializa la clase XbeeTools.
        Args:
            dest_mac (bytearray): Dirección MAC de destino. Si no se proporciona, se usa una dirección por defecto.
        """
        self.dest_mac = dest_mac
        self._buffer = bytearray()
        self.start_delimiter = start_delimiter

    def push_data(self, data: bytearray):
        """ 
        Agrega datos al buffer, detecta si hay uno o más frames completos y los procesa.
        
        Args:
            data (bytearray): Nuevos datos a agregar al buffer
        """
        # Agregar los nuevos datos al buffer
        self._buffer.extend(data)   
        
        # Procesar todos los frames completos que puedan existir en el buffer
        while True:
            # Buscar el delimitador de inicio en el buffer
            start_index = self._buffer.find(bytes([self.start_delimiter]))
            
            # Si no hay delimitador, salir del bucle
            if start_index == -1:
                break
            
            # Si el delimitador no está al inicio, descartar los bytes anteriores
            if start_index > 0:
                # Emitir un error si hay bytes antes del delimitador
                self.on_error.emit(f"Bytes antes del delimitador de inicio: {self.bytes_to_str(self._buffer[:start_index])}\n\tbuffer: {self.bytes_to_str(self._buffer)}")
                self._buffer = self._buffer[start_index:]
                start_index = 0

            # Verificar si tenemos suficientes bytes para leer la longitud (necesitamos al menos 4 bytes)
            if len(self._buffer) < 4:
                break  # Esperamos más datos
            
            # Obtener la longitud declarada del frame
            length = (self._buffer[1] << 8) | self._buffer[2]
            
            # Calcular el tamaño total del frame (3 bytes de cabecera + longitud + 1 byte de checksum)
            total_frame_size = 3 + length + 1
            
            # Verificar si tenemos el frame completo
            if len(self._buffer) < total_frame_size:
                break  # Esperamos más datos
            
            # Extraer el frame completo (raw frame)
            raw_frame = self._buffer[:total_frame_size]

            # Extraer el frame completo y analizarlo
            frame = self.frame_analyzer(raw_frame)

            # Eliminar el frame procesado del buffer
            self._buffer = self._buffer[total_frame_size:]
            if frame.frame_type == XBEE_FRAME_TYPE_ERROR:
                # Si el frame es inválido, emitir un error
                self.on_error.emit(f"Frame inválido o error al analizar: {self.bytes_to_str(raw_frame)}")
                continue
            elif frame.frame_type == XBEE_FRAME_TYPE_RECEIVE:
                # Emitir la señal de datos recibidos
                self.on_receive.emit(frame.payload, frame.mac)

    def frame_analyzer(self, frame: bytearray) -> XbeeFrame:
        """
        Analyzes an XBee frame and extracts the payload and MAC address.
        Args:
            frame (bytearray): The XBee frame to analyze.
        Returns:
            packet_data (Tuple[str, bytearray]): A tuple containing the payload as a string and the MAC address as a bytearray.
            Returns 'None, None' if the frame is invalid or an error occurs.
        """
        if frame[0] != self.start_delimiter or len(frame) < 6:
            # print("Error: Frame no comienza con 0x7E o es demasiado corto.")
            self.on_error.emit(f"Frame no comienza con {self.start_delimiter} o es demasiado corto.\n\tFrame: {self.bytes_to_str(frame)}")
            return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)

        length = (frame[1] << 8) | frame[2]
        if len(frame) != 3 + length + 1:
            self.on_error.emit(f"El largo real del frame ({len(frame)}) no coincide con la longitud declarada ({length}).\n\tFrame: {self.bytes_to_str(frame)}\n\tLength = 0x{frame[1]:02X} 0x{frame[2]:02X}\t= {length} bytes")
            return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)

        frame_data = frame[3:3+length]
        checksum_sender = frame[-1]
        match frame[3]: # Frame type
            case 0x00:
                # print("(Transmit)")
                pass
            case 0x89:
                # print("(TX Status)")
                status = frame[5]
                if status != 0x00:
                    self.on_error.emit(f"\tTX Status: {status:02X} = {status}")
                    return XbeeFrame(frame_type=XBEE_FRAME_TYPE_TX_STATUS, status=status)
                pass
            case 0x90:
                # print("(Receive)")
                pass
            case _:
                self.on_error.emit(f"\tFrame type: 0x{frame[3]:02X} = {frame[3]}\t(Desconocido)")
                return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)

        checksum_calc = 0xFF - (sum(frame_data) & 0xFF)
        if checksum_sender != checksum_calc:
            self.on_error.emit(f"Checksum INVALIDO\n\tChecksum: 0x{checksum_sender:02X} != 0x{checksum_calc:02X}\n\tFrame: {self.bytes_to_str(frame, prefix='')}")
            return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)

        match frame[3]: # Frame type
            case 0x00:  # Transmit Request
                pass
            case 0x89:  # Transmit Status
                return XbeeFrame(frame_type=XBEE_FRAME_TYPE_TX_STATUS, status=frame[5])
            case 0x90:  # Receive Packet
                data, mac = self._extract_packet_data(frame)
                if data is None or mac is None:
                    self.on_error.emit(f"Error al extraer datos del frame de recepción: {self.bytes_to_str(frame)}")
                    return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)
                return XbeeFrame(frame_type=XBEE_FRAME_TYPE_RECEIVE, mac=mac, payload=data)
            case _:
                pass
        self.on_error.emit(f"Frame no reconocido o no implementado: {self.bytes_to_str(frame)}")
        return XbeeFrame(frame_type=XBEE_FRAME_TYPE_ERROR)

    def bytes_to_str(self, data: bytearray, prefix: str = "0x", delimiter: str = " ") -> str:
        """Converts bytes to a formatted string."""
        return delimiter.join(f'{prefix}{b:02X}' for b in data)

    def _extract_packet_data(self, frame: bytearray) -> Tuple[str, bytearray]:
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

    def frame_formatter(self, data: str, mac: bytearray) -> bytearray:
        """
        Formatea un frame XBee para enviar datos.
        """
        if not isinstance(mac, bytearray) or len(mac) != 8:
            raise ValueError("MAC debe ser un bytearray de 8 bytes.")
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
        frame.append(self.start_delimiter)
        frame.append(length_msb)
        frame.append(length_lsb)
        frame += frame_data
        frame.append(checksum)

        return frame