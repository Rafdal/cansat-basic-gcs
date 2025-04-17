from PyQt5.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit
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
        self.stream = False
        toggle_stream_btn = Button("Toggle Stream", on_click=self.toggle_stream)
        hlayout.addWidget(refresh_btn)
        hlayout.addWidget(connect_btn)
        hlayout.addWidget(disconnect_btn)
        hlayout.addWidget(toggle_stream_btn)

        self.baud_input = TextInput("Baud Rate", default="9600", regex=r"^\d+$", layout='h', callOnEnter=False, 
                               on_change=lambda x: print(f"Baud Rate changed to: {x}"))

        hlayout.addWidget(self.baud_input)
        hlayout.addStretch()

        kill_port_btn = Button("Kill Port", on_click=self.model.serial.kill_port)
        hlayout.addWidget(kill_port_btn)

        # Add a list widget to display serial ports - with styling to ensure visibility
        self.port_list = QListWidget()
        self.port_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.port_list.setFixedHeight(0)  # Start with no height

        # Add a text area to display received data
        self.data_display = ConsoleWidget()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter text here...")

        # Add widgets to the main layout
        layout.addLayout(hlayout)
        layout.addWidget(self.port_list)
        layout.addWidget(self.data_display)
        layout.addWidget(self.user_input)
        
        self.init_signals()

    def init_signals(self):
        # Connect signals
        self.model.serial.data_received.connect(self.on_data_received)
        self.model.serial.error.connect(self.on_serial_error)
        self.model.serial.connected.connect(self.on_connection_status_changed)
        self.port_list.itemClicked.connect(self.on_port_clicked)
        self.user_input.returnPressed.connect(self.send_user_input)

    def toggle_stream(self):
        # Toggle the stream state and update the button text accordingly
        if self.stream:
            self.stream = False
            self.model.stop_timer()  # Stop the timer
        else:
            self.stream = True
            self.model.attach_timer_callback(self.send_ping)  # Attach the callback to send ping
            self.model.start_timer(500)  # Start the timer with a 1-second interval

    def send_ping(self):
        # Start streaming data from the serial port
        self.model.serial.send_data(b"ping")
        self.data_display.appendText(f"Sent: ping\n", color=QColor("blue"))

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
    
        # Adjust the height of the port_list to fit its content
        total_items = self.port_list.count()
        if total_items > 0:
            row_height = self.port_list.sizeHintForRow(0)
            self.port_list.setFixedHeight(row_height * total_items + 2 * self.port_list.frameWidth())
        else:
            self.port_list.setFixedHeight(0)

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
        self.model.serial.disconnect()
        print("Disconnected from port.")

    def on_data_received(self, data):
        # Append received data to the text display
        self.data_display.appendText(data + "\n")

    def send_user_input(self):
        # Get the text from the user input area and send it to the serial port
        user_text = self.user_input.text()
        if user_text:
            self.model.serial.send_data(user_text.encode())
            self.data_display.appendText(f"Sent: {user_text}\n", color=QColor("blue"))
            self.user_input.clear()

    def on_serial_error(self, error_message):
        # Display error message in the text display
        self.data_display.appendText(f"Error: {error_message}\n", color=QColor("red"))

    def on_connection_status_changed(self, connected):
        # Update the UI based on connection status
        if connected:
            self.data_display.appendText(f"Connected to serial port.\n", color=QColor("green"))
        else:
            self.data_display.appendText("Disconnected from serial port.\n", color=QColor("red"))