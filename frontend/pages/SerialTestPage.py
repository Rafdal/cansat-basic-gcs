from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush

from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button, TextInput
from frontend.widgets.ConsoleWidget import ConsoleWidget

class SerialTestPage(BaseClassPage):
    title = "Serial Test"

    def initUI(self, layout):
        # Horizontal layout for the button
        hlayout = QHBoxLayout()

        refresh_btn = Button("Scan Ports", on_click=self.scan_ports)
        connect_btn = Button("Connect", on_click=self.connect_to_port)
        disconnect_btn = Button("Disconnect", on_click=self.disconnect_from_port)
        hlayout.addWidget(refresh_btn)
        hlayout.addWidget(connect_btn)
        hlayout.addWidget(disconnect_btn)

        self.baud_input = TextInput("Baud Rate", default="9600", regex=r"^\d+$", layout='h', callOnEnter=False, 
                               on_change=lambda x: print(f"Baud Rate changed to: {x}"))

        hlayout.addWidget(self.baud_input)
        hlayout.addStretch()

        # Add a list widget to display serial ports - with styling to ensure visibility
        self.port_list = QListWidget()
        self.port_list.setMinimumHeight(200)
        self.port_list.setMinimumWidth(300)
        

        # Add a text area to display received data
        self.data_display = ConsoleWidget()

        # Add widgets to the main layout
        layout.addLayout(hlayout)
        layout.addWidget(self.port_list)
        layout.addWidget(self.data_display)
        
        self.init_signals()

    def init_signals(self):
        # Connect signals
        self.model.serial.data_received.connect(self.on_data_received)
        self.model.serial.error.connect(self.on_serial_error)
        self.model.serial.connected.connect(self.on_connection_status_changed)
        self.port_list.itemClicked.connect(self.on_port_clicked)


    def scan_ports(self):
        # Clear the list before updating
        self.port_list.clear()
    
        # Fetch available serial ports using SerialPortHandler
        ports = self.model.serial.list_serial_ports()
    
        # Populate the list widget with port information - with explicit text setting
        for port in ports:            
            list_item = QListWidgetItem()
            list_item.setText(str(port))
            list_item.setForeground(QBrush(QColor(0, 0, 0)))  # Black text
            list_item.setData(Qt.UserRole, port)  # Store port data with explicit role
            self.port_list.addItem(list_item)
    
        self.port_list.update()

    def on_port_clicked(self, item):
        # Retrieve the SerialPortData object stored in the clicked item
        port_data = item.data(Qt.UserRole)
        self.model.serial.selected_port = port_data

    def connect_to_port(self):
        # Attempt to connect to the selected port
        self.model.serial.set_baudrate(int(self.baud_input.text()))
        if self.model.serial.connect():
            print(f"Page: Port Connected")
        else:
            print(f"Page: Failed to connect.")
        print(f"Port status: {'Open' if self.model.serial.serial_port.isOpen() else 'Closed'}")

    def disconnect_from_port(self):
        # Disconnect from the current port
        self.model.serial.disconnect_from_port()
        print("Disconnected from port.")

    def on_data_received(self, data):
        # Append received data to the text display
        self.data_display.appendText(data + "\n")

    def on_serial_error(self, error_message):
        # Display error message in the text display
        self.data_display.appendText(f"Error: {error_message}\n", color=QColor("red"))

    def on_connection_status_changed(self, connected):
        # Update the UI based on connection status
        if connected:
            self.data_display.appendText(f"Connected to serial port.\n", color=QColor("green"))
        else:
            self.data_display.appendText("Disconnected from serial port.\n", color=QColor("red"))