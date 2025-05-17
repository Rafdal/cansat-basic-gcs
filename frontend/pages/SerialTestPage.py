from PyQt5.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QVBoxLayout, QWidget, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush

from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button, TextInput
from frontend.widgets.ConsoleWidget import ConsoleWidget
from frontend.widgets.SerialPortMenu import SerialPortMenu


class SerialTestPage(BaseClassPage):
    title = "Serial Test"

    def initUI(self, layout):

        hlayout_userIO = QHBoxLayout()
        vlayout_btns = QVBoxLayout()

        vlayout_btns.addWidget(Button("PING", on_click=lambda: self.send_xbee("PING")))
        vlayout_btns.addWidget(Button("FIRE", on_click=lambda: self.send_xbee("FIRE")))
        vlayout_btns.addWidget(Button("TOGGLE TELEMETRY", on_click=lambda: self.send_xbee("TOGGLE")))
        vlayout_btns.addStretch()

        # Add a text area to display received data
        self.data_display = ConsoleWidget()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter text here...")

        hlayout_userIO.addWidget(self.data_display)
        hlayout_userIO.addLayout(vlayout_btns)

        # layout.addWidget(self.serial_menu)
        layout.addLayout(hlayout_userIO)
        layout.addWidget(self.user_input)
        
        self.init_signals()

    def init_signals(self):
        # Connect signals
        self.model.serial.connected.connect(self.on_connection_status_changed)
        self.model.on_data_received.connect(self.on_data_received)
        self.model.on_error.connect(self.on_error)
        self.user_input.returnPressed.connect(self.send_user_input)

    def send_xbee(self, data: str):
        self.model.transmit_data(data)
        self.data_display.appendText(f"Enviado: {data}\n", color=QColor("blue"))

    def on_data_received(self, data: str, mac: bytearray):
        self.data_display.appendText(f"Recibido: {data}\n", color=QColor("green"))

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
            self.data_display.appendText(f"Connected to serial port.\n", color=QColor("green"))
        else:
            self.data_display.appendText("Disconnected from serial port.\n", color=QColor("red"))