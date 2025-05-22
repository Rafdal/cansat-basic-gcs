from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QPushButton
from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.Sidebar import Sidebar
from frontend.widgets.GraphWidget import GraphWidget, GraphWidgetMultiplot
from frontend.widgets.ButtonsGroup import ButtonsGroup
from frontend.widgets.CommandLine import CommandLine

from PyQt5.QtGui import QColor

import pyqtgraph as pg

from backend.Commands import Commands
from backend.SimulationMode import SimulationMode

## Solo para test
from numpy import random, round
import time

class MainPage(BaseClassPage):
    title = "Dashboard"

    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar()

        self.graph_altitude = GraphWidget("Altitude", "Time", "s", "", "m")
        self.graph_rpm = GraphWidget("RPM", "Time", "s", "", "deg/s")
        self.graph_temperature = GraphWidget("Temperature", "Time", "s", "", "C")
        self.graph_pressure = GraphWidget("Pressure", "Time", "s", "", "Pa")
        self.graph_voltage = GraphWidget("Voltage", "Time", "s", "", "V")
        self.graph_accel = GraphWidgetMultiplot("Acceleration", "Time", "s", "", "m/s²")

        self.graph_accel.add_plot("X", QColor(255, 0, 0))
        self.graph_accel.add_plot("Y", QColor(0, 150, 0))
        self.graph_accel.add_plot("Z", QColor(0, 0, 255))

        self.simulation = SimulationMode()
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
        graph_layout.addWidget(self.graph_altitude, 0, 0)
        graph_layout.addWidget(self.graph_rpm, 0, 1)
        graph_layout.addWidget(self.graph_temperature, 0, 2)
        graph_layout.addWidget(self.graph_pressure, 1, 0)
        graph_layout.addWidget(self.graph_voltage, 1, 1)
        graph_layout.addWidget(self.graph_accel, 1, 2)

        center_layout.addLayout(graph_layout)
        self.init_signals()

    def init_signals(self):
        self.model.on_data_received.connect(self.on_cansat_data_received)

    def on_cansat_data_received(self, data: str, mac: bytearray):
        # print(f"\tMainPage -> Data received \'{data}\'")
        if ("3165," in data[0:6]):
            parsed_data = self.parse_cansat_data(data)
            # Process the parsed data as needed
            # print(f"Parsed data: {parsed_data}")
            self.update_plot_with_data(parsed_data)

    def parse_cansat_data(self, data_str: str) -> dict:
        fields = data_str.strip().split(",")
        cansat_data = {
            "mission_time": fields[1],
            "packet_count": int(fields[2]),
            "mode": fields[3],
            "state": fields[4],
            "altitude": float(fields[5]),
            "temperature": float(fields[6]),
            "pressure": float(fields[7]),
            "voltage": float(fields[8]),
            "gyro_r": float(fields[9]),
            "gyro_p": float(fields[10]),
            "gyro_y": float(fields[11]),
            "accel_r": float(fields[12]),
            "accel_p": float(fields[13]),
            "accel_y": float(fields[14]),
            "mag_r": float(fields[15]),
            "mag_p": float(fields[16]),
            "mag_y": float(fields[17]),
            "autogyro_rot_rate": float(fields[18]),
            "gps_time": fields[19],
            "gps_altitude": float(fields[20]),
            "gps_latitude": float(fields[21]),
            "gps_longitude": float(fields[22]),
            "gps_sats": int(fields[23]),
            "cmd_echo": fields[24]
        }
        # set time from actual time, not from fields
        cansat_data["mission_time"] = time.strftime("%H:%M:%S", time.gmtime())
        return cansat_data

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
            "autogyro_rot_rate": random_float(0.0, 5.0),
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
        
        self.update_plot_with_data(data)


    def update_plot_with_data(self, data: dict):
        self.sidebar.update(data['mission_time'], data['packet_count'], data['mode'], data['state'], data['altitude'], data['temperature'], data['pressure'], data['voltage'], data['gyro_r'], data['gyro_p'], data['gyro_y'], data['accel_r'], data['accel_p'], data['accel_y'], data['mag_r'], data['mag_p'], data['mag_y'], data['autogyro_rot_rate'], data['gps_time'], data['gps_altitude'], data['gps_latitude'], data['gps_longitude'], data['gps_sats'], data['cmd_echo'])
        self.graph_altitude.update(data['altitude'])
        self.graph_rpm.update(data['autogyro_rot_rate'])
        self.graph_temperature.update(data['temperature'])
        self.graph_pressure.update(data['pressure'])
        self.graph_voltage.update(data['voltage'])    

        self.graph_accel.update('X', data['accel_r'])
        self.graph_accel.update('Y', data['accel_p'])
        self.graph_accel.update('Z', data['accel_y'])

        self.model.storage.write(data.values()) # TODO: change to the actual data format (CSV)


    def start_telemetry_wrapper(self):
        print(f"Telemetry started")
        self.model.storage.open()
        # self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.update_test_hardcodeado)
        self.timer.start(1000) # In milliseconds
        self.commands.start_telemetry_handler()

    def end_telemetry_wrapper(self):
        print(f"Telemetry ended")
        self.timer.stop()
        self.commands.end_telemetry_handler()

    
    def update_test_hardcodeado(self):
        self.on_cansat_data_received(self.test_data[self.test_data_index], None)
        self.test_data_index += 1
        if self.test_data_index >= len(self.test_data):
            self.test_data_index = 0

    test_data_index = 0
    test_data = [
        "3165,HH:MM:SS,2,F,LAUNCH_PAD,-93.0,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,3,F,LAUNCH_PAD,-93.2,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,4,F,LAUNCH_PAD,-93.0,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,5,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,6,F,LAUNCH_PAD,-93.0,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,7,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,8,F,LAUNCH_PAD,-92.9,29.1,102.4,8.2,18.0,21.0,20.0,-0.6,9.5,1.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,9,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-1.0,9.6,1.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,10,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.3,4.7,5.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,11,F,LAUNCH_PAD,-93.0,29.0,102.4,8.2,18.0,21.0,20.0,-0.2,-0.4,9.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,12,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.0,0.3,9.7,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,13,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.0,0.3,9.7,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,14,F,LAUNCH_PAD,-92.7,29.0,102.4,8.2,18.0,21.0,20.0,0.0,0.4,10.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,15,F,LAUNCH_PAD,-92.7,29.0,102.4,8.2,18.0,21.0,20.0,0.6,-0.1,10.3,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,16,F,LAUNCH_PAD,-92.6,29.0,102.4,8.2,18.0,21.0,20.0,0.9,-0.3,10.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,17,F,LAUNCH_PAD,-92.2,29.0,102.4,8.2,18.0,21.0,20.0,1.2,-3.4,8.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,18,F,LAUNCH_PAD,-92.1,29.0,102.4,8.2,18.0,21.0,20.0,0.8,-3.5,9.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,19,F,LAUNCH_PAD,-92.1,29.0,102.4,8.2,18.0,21.0,20.0,0.1,-2.8,9.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,20,F,LAUNCH_PAD,-92.0,29.0,102.4,8.2,18.0,21.0,20.0,1.3,-1.8,9.5,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,21,F,LAUNCH_PAD,-92.1,29.0,102.4,8.2,18.0,21.0,20.0,2.6,-1.2,8.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,22,F,LAUNCH_PAD,-92.6,29.0,102.4,8.2,18.0,21.0,20.0,0.9,-0.3,9.2,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,23,F,LAUNCH_PAD,-92.8,29.0,102.4,8.2,18.0,21.0,20.0,0.3,1.3,10.3,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,24,F,LAUNCH_PAD,-92.9,29.0,102.4,8.2,18.0,21.0,20.0,-0.5,0.5,9.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,25,F,LAUNCH_PAD,-93.1,29.0,102.4,8.2,18.0,21.0,20.0,1.4,-0.7,9.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,26,F,LAUNCH_PAD,-93.1,29.0,102.4,8.2,18.0,21.0,20.0,1.8,-0.5,9.7,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,27,F,LAUNCH_PAD,-93.3,29.0,102.5,8.2,18.0,21.0,20.0,1.9,0.1,9.7,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,28,F,LAUNCH_PAD,-93.2,29.0,102.4,8.2,18.0,21.0,20.0,1.8,1.2,9.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,29,F,LAUNCH_PAD,-93.3,29.0,102.5,8.2,18.0,21.0,20.0,1.9,1.0,9.5,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,30,F,LAUNCH_PAD,-93.0,28.9,102.4,8.2,18.0,21.0,20.0,3.1,1.0,8.9,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,31,F,LAUNCH_PAD,-92.4,28.9,102.4,8.2,18.0,21.0,20.0,2.7,-0.5,8.0,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,32,F,LAUNCH_PAD,-92.4,28.9,102.4,8.2,18.0,21.0,20.0,-0.2,2.8,9.7,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,33,F,LAUNCH_PAD,-92.3,28.9,102.4,8.2,18.0,21.0,20.0,-6.9,-1.9,10.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,34,F,LAUNCH_PAD,-92.2,28.8,102.4,8.2,18.0,21.0,20.0,-9.1,-1.6,8.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,35,F,LAUNCH_PAD,-92.4,28.8,102.4,8.2,18.0,21.0,20.0,-9.5,-2.2,4.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,36,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,-11.4,-0.1,9.0,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,37,F,LAUNCH_PAD,-92.4,28.8,102.4,8.2,18.0,21.0,20.0,-24.6,-0.6,11.0,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,38,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,-14.4,0.1,8.5,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,39,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,0.3,0.5,6.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,40,F,LAUNCH_PAD,-92.5,28.8,102.4,8.2,18.0,21.0,20.0,5.4,-1.2,4.2,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,41,F,LAUNCH_PAD,-92.6,28.8,102.4,8.2,18.0,21.0,20.0,-0.1,-2.5,-4.0,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,42,F,LAUNCH_PAD,-92.5,28.8,102.4,8.2,18.0,21.0,20.0,-4.8,-4.7,-0.6,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,43,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,-15.2,-5.3,-6.4,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,44,F,LAUNCH_PAD,-92.5,28.8,102.4,8.2,18.0,21.0,20.0,-19.8,1.2,5.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,45,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,-16.0,-2.8,-8.5,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,46,F,LAUNCH_PAD,-92.3,28.8,102.4,8.2,18.0,21.0,20.0,-4.0,-1.0,1.0,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,47,F,LAUNCH_PAD,-92.7,28.8,102.4,8.2,18.0,21.0,20.0,-2.2,-3.0,9.8,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,48,F,LAUNCH_PAD,-92.7,28.8,102.4,8.2,18.0,21.0,20.0,0.4,-8.9,2.5,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,49,F,LAUNCH_PAD,-92.8,28.8,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.2,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,50,F,LAUNCH_PAD,-92.8,28.9,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,51,F,LAUNCH_PAD,-92.8,28.9,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,52,F,LAUNCH_PAD,-92.7,28.9,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,53,F,LAUNCH_PAD,-92.8,28.8,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,54,F,LAUNCH_PAD,-92.8,28.9,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
        "3165,HH:MM:SS,55,F,LAUNCH_PAD,-92.8,28.9,102.4,8.2,18.0,21.0,20.0,0.4,-9.5,1.1,0.2,0.0,0.1,0.0,0.0:0.0:0.0,0.0,0.0,0.0,0,ST 12:30:45,",
    ]