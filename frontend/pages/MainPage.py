from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.Sidebar import Sidebar
from frontend.widgets.GraphWidget import GraphWidget
from frontend.widgets.ButtonsGroup import ButtonsGroup
from frontend.widgets.CommandLine import CommandLine
from backend.Storage import Storage
from backend.SimulationMode import SimulationMode
from PyQt5.QtWidgets import QWidget, QPushButton
import pyqtgraph as pg
from backend.Commands import Commands

## Solo para test
import random
import time
##

class MainPage(BaseClassPage):
    title = "Dashboard"

    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar()

        self.graph_altitude = GraphWidget("Altitude", "Time", "s", "Altitude", "[m]")
        self.graph_airspeed = GraphWidget("Air Speed", "Time", "s", "Air Speed", "[m/s]")
        self.graph_temperature = GraphWidget("Temperature", "Time", "s", "Temperature", "[C]")
        self.graph_pressure = GraphWidget("Pressure", "Time", "s", "Pressure", "[Pa]")
        self.graph_voltage = GraphWidget("Voltage", "Time", "s", "Voltage", "[V]")

        self.simulation = SimulationMode()
        self.storage = Storage()
        self.xbee = "xbee" # TODO: connect xbee

        self.timer = pg.QtCore.QTimer()

        self.commands = Commands()

    def initUI(self, layout):

        hlayout = QHBoxLayout()

        # Sidebar
        hlayout.addWidget(self.sidebar.sidebar_widget)

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        hlayout.addWidget(center_widget)

        telemetry_button_layout = QHBoxLayout()

        button_style = '''QPushButton{font-size:20px; margin:5px; padding:10px; height:20px; width:175px;}'''

        # Start telemetry button
        start_telemetry_btn = QPushButton("START TELEMETRY", center_widget)
        start_telemetry_btn.setStyleSheet(button_style)
        start_telemetry_btn.clicked.connect(lambda: self.start_telemetry_wrapper())
        telemetry_button_layout.addWidget(start_telemetry_btn)

        # End telemetry button
        end_telemetry_btn = QPushButton("END TELEMETRY", center_widget)
        end_telemetry_btn.setStyleSheet(button_style)
        end_telemetry_btn.clicked.connect(lambda: self.end_telemetry_wrapper())
        telemetry_button_layout.addWidget(end_telemetry_btn)

        center_layout.addLayout(telemetry_button_layout)

        title_style = '''QLabel{font-size:24px; margin:5px; font-weight:600;}'''

        text_command = QLabel('Commands', center_widget)
        text_command.setStyleSheet(title_style)
        center_layout.addWidget(text_command)

        buttons_group = ButtonsGroup(center_widget, self.xbee) 

        command_line = CommandLine(center_widget, self.xbee) 

        layout.addLayout(hlayout)
        center_layout.addLayout(buttons_group.button_layout)
        center_layout.addLayout(command_line.command_line_layout)
        
        graph_layout = QGridLayout()
        
        # Add graphs widgets to the grid layout
        graph_layout.addWidget(self.graph_altitude.plot, 0, 0)
        graph_layout.addWidget(self.graph_airspeed.plot, 0, 1)
        graph_layout.addWidget(self.graph_temperature.plot, 0, 2)
        graph_layout.addWidget(self.graph_pressure.plot, 1, 0)
        graph_layout.addWidget(self.graph_voltage.plot, 1, 1)

        center_layout.addLayout(graph_layout)
        
    def update(self):

        ## solo para test
        def random_float(min_val, max_val):
            return round(random.uniform(min_val, max_val), 2)

        def random_int(min_val, max_val):
            return random.randint(min_val, max_val)
        ##

        # TODO: change this to get data from the XBEE
        # Simulate data for testing
        data = {
            "mission_time": time.strftime("%H:%M:%S", time.gmtime(random_int(0, 36000))),
            "packet_count": random_int(1, 1000),
            "mode": random.choice(["S", "N"]),
            "state": random.choice(["ASCENT", "DESCENT"]),
            "temperature": random_float(-20.0, 40.0),
            "airspeed": random_float(0.0, 50.0),
            "altitude": random_float(0.0, 5000.0),
            "pressure": random_float(900.0, 1100.0),
            "voltage": random_float(3.0, 4.2),
            "gyro_r": random_float(-1.0, 1.0),
            "gyro_p": random_float(-1.0, 1.0),
            "gyro_y": random_float(-1.0, 1.0),
            "accel_r": random_float(-2.0, 2.0),
            "accel_p": random_float(-2.0, 2.0),
            "accel_y": random_float(-2.0, 2.0),
            "mag_r": random_float(-50.0, 50.0),
            "mag_p": random_float(-50.0, 50.0),
            "mag_y": random_float(-50.0, 50.0),
            "autogyro_desc_rate": random_float(0.0, 5.0),
            "gps_time": time.strftime("%H:%M:%S", time.gmtime(random_int(0, 86400))),
            "gps_altitude": random_float(0.0, 2000.0),
            "gps_latitude": random_float(-90.0, 90.0),
            "gps_longitude": random_float(-180.0, 180.0),
            "gps_sats": random_int(0, 12),
            "cmd_echo": random.choice(["CAL_ALTITUDE"])
        }

        if data['mode'] == "S":

            if self.simulation.initialized == False:
                self.simulation.enable()

            self.simulation.send_command(xbee=None)

            simulated_value = self.simulation.send_command(self.xbee)
            data['pressure'] = simulated_value
        
        self.sidebar.update(data['mission_time'], data['packet_count'], data['mode'], data['state'], data['altitude'], data['temperature'], data['pressure'], data['voltage'], data['gyro_r'], data['gyro_p'], data['gyro_y'], data['accel_r'], data['accel_p'], data['accel_y'], data['mag_r'], data['mag_p'], data['mag_y'], data['autogyro_desc_rate'], data['gps_time'], data['gps_altitude'], data['gps_latitude'], data['gps_longitude'], data['gps_sats'], data['cmd_echo'])
        self.graph_altitude.update(data['altitude'])
        self.graph_airspeed.update(data['airspeed'])
        self.graph_temperature.update(data['temperature'])
        self.graph_pressure.update(data['pressure'])
        self.graph_voltage.update(data['voltage'])    

        self.storage.write(data.values()) # TODO: change to the actual data format (CSV)        

    def start_telemetry_wrapper(self):
        print(f"Telemetry started")
        self.storage.open()
        self.timer.timeout.connect(self.update)
        self.timer.start(500) # In miliseconds
        self.commands.start_telemetry_handler(self.xbee)

    def end_telemetry_wrapper(self):
        print(f"Telemetry ended")
        self.timer.stop()
        self.storage.close()
        self.commands.end_telemetry_handler(self.xbee)
