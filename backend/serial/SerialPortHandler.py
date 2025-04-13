from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import pyqtSignal, QObject, QThread
import typing, dataclasses

@dataclasses.dataclass
class SerialPortData:
    name: str = "None"
    description: str = "None"
    manufacturer: str = "None"
    baudrate: int = 9600
    def prettyPrint(self):
        return f"Port: {self.name}, Description: {self.description}, Manufacturer: {self.manufacturer}, Baud Rate: {self.baudrate}"
    def __str__(self):
        return f"{self.name} | {self.description} | {self.manufacturer}"


class SerialPortHandler(QObject):
    connected = pyqtSignal(bool)
    error = pyqtSignal(str)
    data_received = pyqtSignal(str)

    terminator = b'\n'  # Define a terminator for the data
    max_buffer_size = 1024  # Define a maximum buffer size

    def __init__(self):
        super().__init__()
        self.serial_port = QSerialPort()
        self.buffer = bytearray()  # Initialize buffer as a bytearray
        self.serial_port.errorOccurred.connect(self._on_error)
        self.serial_port.readyRead.connect(self._handle_read)
        self.selected_port = SerialPortData()

    def set_baudrate(self, baudrate: int):
        """Set the baud rate for the serial port"""
        self.selected_port.baudrate = baudrate

    def connect(self):
        """Connect to a serial port with the specified baud rate"""
        if not self.selected_port.name or self.selected_port.name == "None":
            self.error.emit("No port selected")
            return False
        
        # Close any existing connection
        if self.serial_port.isOpen():
            self.serial_port.close()
            
        try:
            # Configure port with explicit settings
            self.serial_port.setPortName(self.selected_port.name)
            self.serial_port.setBaudRate(self.selected_port.baudrate)
            # self.serial_port.setDataBits(QSerialPort.Data8)
            # self.serial_port.setParity(QSerialPort.NoParity)
            # self.serial_port.setStopBits(QSerialPort.OneStop)
            # self.serial_port.setFlowControl(QSerialPort.NoFlowControl)

            # Set read/write timeouts (add these lines)
            # self.serial_port.setReadBufferSize(4096)
            
            # Try to open the port
            if not self.serial_port.open(QSerialPort.ReadWrite):
                error_msg = f"Failed to open port {self.selected_port.name}: {self.serial_port.errorString()}"
                self.error.emit(error_msg)
                return False
            else:
                # Clear buffer on new connection
                self.buffer.clear()
                self.connected.emit(True)
                return True
        except Exception as e:
            self.error.emit(f"Error connecting to port {self.selected_port.name}: {str(e)}")
            return False
        
    def list_serial_ports(self) -> typing.List[SerialPortData]:
        """Lists all available serial ports with their information."""
        ports = []
        for info in QSerialPortInfo.availablePorts():
            port_data = SerialPortData(
                name=info.portName(),
                description=info.description(),
                manufacturer=info.manufacturer(),
            )
            ports.append(port_data)
        return ports

    def disconnect_from_port(self):
        """Disconnect from the current serial port"""
        try:
            if self.serial_port.isOpen():
                self.serial_port.close()
            self.connected.emit(False)
        except Exception as e:
            self.error.emit(f"Error disconnecting: {str(e)}")

    def send_data(self, data):
        """Send data to the serial port"""
        if not self.serial_port.isOpen():
            self.error.emit("Cannot send data: Port is not open")
            return False

        try:
            # Convert string to bytes if needed
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            bytes_written = self.serial_port.write(data)
            return bytes_written == len(data)
        except Exception as e:
            self.error.emit(f"Error sending data: {str(e)}")
            return False
        
    def _handle_read(self):
        """Handle data received from the serial port"""
        print("handle_read called")
        if self.serial_port.bytesAvailable() > 0:
            try:
                # Convert QByteArray to bytes properly
                raw_data = self.serial_port.readAll()
                newData = bytes(raw_data)
                
                print(f"Raw data received: {newData.hex()}")
                
                if newData:
                    # Add new data to buffer
                    self.buffer.extend(newData)
                    
                    # Limit buffer size
                    if len(self.buffer) > self.max_buffer_size:
                        self.buffer = self.buffer[-self.max_buffer_size:]
                    
                    # Process complete lines
                    self._process_buffer()
            except Exception as e:
                self.error.emit(f"Error reading from serial port: {str(e)}")

    def _process_buffer(self):
        """Process buffer for complete lines"""
        try:
            # Find position of first terminator
            terminator_pos = self.buffer.find(self.terminator)
            
            # Process all complete lines in buffer
            while terminator_pos >= 0:
                # Extract line (excluding terminator)
                line_bytes = self.buffer[:terminator_pos]
                
                # Convert to string and emit
                try:
                    line = line_bytes.decode('utf-8', errors='replace').strip()
                    if line:
                        self.data_received.emit(line)
                        print(f"Line emitted: {line}")
                except Exception as e:
                    self.error.emit(f"Error decoding line: {str(e)}")
                
                # Remove processed data from buffer (including terminator)
                self.buffer = self.buffer[terminator_pos + len(self.terminator):]
                
                # Find next terminator
                terminator_pos = self.buffer.find(self.terminator)
        except Exception as e:
            self.error.emit(f"Error processing buffer: {str(e)}")

    def _on_data_received(self, data):
        """Handle data received from the reader thread"""
        self.data_received.emit(data)

    def _on_error(self, e):
        """Handle error from the reader thread"""
        if isinstance(e, QSerialPort.SerialPortError):
            self._serial_error_handler(e)
        else:
            self.error.emit(f"Serial port error: {str(e)}")

    def _serial_error_handler(self, error):
        if type(error) != QSerialPort.SerialPortError:
            raise ValueError("The error is not a QSerialPort.SerialPortError")
        
        match error:
            case QSerialPort.SerialPortError.NoError:
                return
            case QSerialPort.SerialPortError.DeviceNotFoundError:
                self.errorOcurred.emit(f"Device {self.selected_port.name} not found")
            case QSerialPort.SerialPortError.PermissionError:
                self.errorOcurred.emit(f"Permission error on {self.selected_port.name}")
            case QSerialPort.SerialPortError.OpenError:
                self.errorOcurred.emit(f"Error opening {self.selected_port.name}")
            case QSerialPort.SerialPortError.ParityError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} ParityError")
            case QSerialPort.SerialPortError.FramingError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} FramingError")
            case QSerialPort.SerialPortError.BreakConditionError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} BreakConditionError")
            case QSerialPort.SerialPortError.WriteError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} WriteError")
            case QSerialPort.SerialPortError.ReadError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} ReadError")
            case QSerialPort.SerialPortError.ResourceError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} ResourceError")
            case QSerialPort.SerialPortError.UnsupportedOperationError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} UnsupportedOperationError")
            case QSerialPort.SerialPortError.TimeoutError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} TimeoutError")
            case QSerialPort.SerialPortError.NotOpenError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} NotOpenError")
            case QSerialPort.SerialPortError.UnknownError:
                self.errorOcurred.emit(f"Error on {self.selected_port.name} UnknownError")
            case _:
                self.errorOcurred.emit(f"Undefined Error {str(error)} on {self.selected_port.name}")