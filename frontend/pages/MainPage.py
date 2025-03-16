from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLineEdit
from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button
from frontend.widgets.Sidebar import Sidebar
from frontend.widgets.GraphWidget import GraphWidget
from frontend.widgets.ButtonsGroup import ButtonsGroup
from PyQt5.QtWidgets import QWidget

class MainPage(BaseClassPage):
    title = "Dashboard"

    def initUI(self, layout):

        hlayout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()
        hlayout.addWidget(self.sidebar.sidebar_widget)

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        hlayout.addWidget(center_widget)

        title_style = '''QLabel{font-size:24px; margin:5px; font-weight:600;}'''

        text_command = QLabel('Commands', center_widget)
        text_command.setStyleSheet(title_style)
        center_layout.addWidget(text_command)

        buttons_group = ButtonsGroup(center_widget)

        # Command line
        custom_command_title = QLabel('Send Custom Command', center_widget)
        custom_command_title.setStyleSheet(title_style)
        command_line = QLineEdit(center_widget)
        command_line.setStyleSheet('''QLineEdit{font-size:24px; padding:5px; font-weight:350;}''')
        send_command_btn = QPushButton("SEND", center_widget)
        send_command_btn.setStyleSheet('''QPushButton{font-size:20px; margin:5px; padding:10px; height:20px; width:50;}''')
        send_command_btn.clicked.connect(lambda: print(command_line.text()))

        # Create a grid layout for the graphs
        graphs_title = QLabel('Telemetry', center_widget)
        graphs_title.setStyleSheet(title_style)

        # Horizontal layout for command line and send button
        command_layout = QHBoxLayout()
        command_layout.addWidget(command_line)
        command_layout.addWidget(send_command_btn)

        graph_layout = QGridLayout()

        # Graph widgets
        graph_altitude = GraphWidget("Altitude", "Time", "s", "Altitude", "[m]")
        graph_airspeed = GraphWidget("Air Speed", "Time", "s", "Air Speed", "[m/s]")
        graph_temperature = GraphWidget("Temperature", "Time", "s", "Temperature", "[C]")
        graph_pressure = GraphWidget("Pressure", "Time", "s", "Pressure", "[Pa]")
        graph_voltage = GraphWidget("Voltage", "Time", "s", "Voltage", "[V]")

        # Add graphs to the grid layout
        graph_layout.addWidget(graph_altitude.plot, 0, 0)
        graph_layout.addWidget(graph_airspeed.plot, 0, 1)
        graph_layout.addWidget(graph_temperature.plot, 0, 2)
        graph_layout.addWidget(graph_pressure.plot, 1, 0)
        graph_layout.addWidget(graph_voltage.plot, 1, 1)

        layout.addLayout(hlayout)
        center_layout.addLayout(buttons_group.button_layout)
        center_layout.addWidget(custom_command_title)
        center_layout.addLayout(command_layout)
        center_layout.addWidget(graphs_title)
        center_layout.addLayout(graph_layout)

    def update(self, data):
        # TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
        # TEMPERATURE, PRESSURE, VOLTAGE, GYRO_R, GYRO_P, GYRO_Y, ACCEL_R,
        # ACCEL_P, ACCEL_Y, MAG_R, MAG_P, MAG_Y, AUTO_GYRO_ROTATION_RATE,
        # GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS,
        # CMD_ECHO [,,OPTIONAL_DATA]

        self.sidebar.update()


