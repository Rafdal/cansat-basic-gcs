from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QColor, QFont

from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button
from frontend.widgets.ConsoleWidget import ConsoleWidget


class SerialTestPage(BaseClassPage):
    title = "Serial Test"

    def initUI(self, layout):


        vlayout_btns = QVBoxLayout()
        vlayout_btns.addWidget(Button("PING", on_click=lambda: self.send_xbee("PING")))
        vlayout_btns.addWidget(Button("FIRE", on_click=lambda: self.send_xbee("FIRE")))
        # vlayout_btns.addWidget(Button("TOGGLE TELEMETRY", on_click=self.toggle_telemetry))
        vlayout_btns.addWidget(Button("ACTIVATE TELEMETRY", on_click=self.activate_telemetry))
        vlayout_btns.addWidget(Button("DEACTIVATE TELEMETRY", on_click=self.deactivate_telemetry))
        vlayout_btns.addWidget(Button("CAL", on_click=lambda: self.send_xbee("CAL")))
        vlayout_btns.addStretch()
        self.data_display = ConsoleWidget()

        hlayout_userIO = QHBoxLayout()
        hlayout_userIO.addWidget(self.data_display)
        hlayout_userIO.addLayout(vlayout_btns)

        self.send_prefix = QLineEdit()
        self.send_prefix.setPlaceholderText("Prefix")
        self.send_prefix.setFont(QFont("Monospace", 10))
        self.send_prefix.setText("CMD,3165,")
        self.send_prefix.setFixedWidth(120)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter text here...")
        self.user_input.setFont(QFont("Monospace", 10))

        hlayout_input = QHBoxLayout()
        hlayout_input.addWidget(self.send_prefix)
        hlayout_input.addWidget(self.user_input)

        # layout.addWidget(self.serial_menu)
        layout.addLayout(hlayout_userIO)
        layout.addLayout(hlayout_input)

        self.init_signals()

    def init_signals(self):
        # Connect signals
        self.model.serial.connected.connect(self.on_connection_status_changed)
        self.model.on_data_received.connect(self.on_data_received)
        self.model.on_error.connect(self.on_error)
        self.user_input.returnPressed.connect(self.send_user_input)

    def activate_telemetry(self):
        self.model.commands.start_telemetry_handler()
        self.model.storage.open()

    def deactivate_telemetry(self):
        self.model.commands.end_telemetry_handler()

    def send_xbee(self, data: str):
        data = self.send_prefix.text() + data
        self.model.transmit_data(data)
        self.data_display.appendText(f"Enviado: \'{data}\'\n", color=QColor("blue"))

    def on_data_received(self, data: str, mac: bytearray):
        color = QColor("green")
        if "ERR" in data:
            color = QColor("red")
        self.data_display.appendText(f"Recibido: \'{data}\'\n", color=color)

    def send_user_input(self):
        # Get the text from the user input area and send it to the serial port
        user_text = self.user_input.text()
        if user_text:
            self.send_xbee(user_text)
            self.user_input.clear()

    def on_error(self, error_message):
        # Display error message in the text display
        self.data_display.appendText(f"Error: {error_message}\n", color=QColor("red"))

    def on_connection_status_changed(self, connected):
        if connected:
            self.data_display.appendText(f"Connected to serial port \'{self.model.serial.selected_port.name}\' at {self.model.serial.selected_port.baudrate}.\n", 
                                         color=QColor("green"))
        else:
            self.data_display.appendText(f"Disconnected from serial port \'{self.model.serial.selected_port.name}\'.\n", color=QColor("red"))