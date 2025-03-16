from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLineEdit
from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button
from frontend.widgets.Sidebar import Sidebar
from frontend.widgets.GraphWidget import GraphWidget
from PyQt5.QtWidgets import QWidget

class MainPage(BaseClassPage):
    title = "Dashboard"

    def initUI(self, layout):

        hlayout = QHBoxLayout()

        # Sidebar
        sidebar = Sidebar()
        hlayout.addWidget(sidebar.sidebar_widget)

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        hlayout.addWidget(center_widget)

        text_style = '''QLabel{font-size:20px; font-weight:600;}'''
        button_style = '''QPushButton{font-size:20px; margin:5px; padding:10px; height:20px; width:175px;}'''
        title_style = '''QLabel{font-size:24px; margin:5px; font-weight:600;}'''

        text_command = QLabel('Commands', center_widget)
        text_command.setStyleSheet(title_style)
        center_layout.addWidget(text_command)

        # Create a grid layout for the buttons
        button_layout = QGridLayout()

        # Set time button
        set_time_btn = QPushButton("SET TIME", center_widget)
        set_time_btn.setStyleSheet(button_style)
        set_time_btn.clicked.connect(lambda: self.set_time())
        button_layout.addWidget(set_time_btn, 0, 0)

        # Start telemetry button
        start_telemetry_btn = QPushButton("START TELEMETRY", center_widget)
        start_telemetry_btn.setStyleSheet(button_style)
        start_telemetry_btn.clicked.connect(lambda: self.start_telemetry())
        button_layout.addWidget(start_telemetry_btn, 0, 1)

        # End telemetry button
        end_telemetry_btn = QPushButton("END TELEMETRY", center_widget)
        end_telemetry_btn.setStyleSheet(button_style)
        end_telemetry_btn.clicked.connect(lambda: self.end_telemetry())
        button_layout.addWidget(end_telemetry_btn, 0, 2)

        # Calibrate altitude to zero button
        calibrate_altitude_to_zero_btn = QPushButton("CAL ALTITUDE", center_widget)
        calibrate_altitude_to_zero_btn.setStyleSheet(button_style)
        calibrate_altitude_to_zero_btn.clicked.connect(lambda: self.cal)
        button_layout.addWidget(calibrate_altitude_to_zero_btn, 0, 3)

        # Set pitch, yaw, roll button
        set_pitch_yaw_roll_btn = QPushButton("SET PYR", center_widget)
        set_pitch_yaw_roll_btn.setStyleSheet(button_style)
        set_pitch_yaw_roll_btn.clicked.connect(lambda: self.pyr)
        button_layout.addWidget(set_pitch_yaw_roll_btn, 0, 4)

        # Enable sim mode button
        enable_sim_mode_btn = QPushButton("ENABLE SIM", center_widget)
        enable_sim_mode_btn.setStyleSheet(button_style)
        enable_sim_mode_btn.clicked.connect(lambda: self.enable_sim)
        button_layout.addWidget(enable_sim_mode_btn, 1, 0)

        # Activate sim mode button
        activate_sim_mode_btn = QPushButton("ACTIVATE SIM", center_widget)
        activate_sim_mode_btn.setStyleSheet(button_style)
        activate_sim_mode_btn.clicked.connect(lambda: self.activate_sim)
        button_layout.addWidget(activate_sim_mode_btn, 1, 1)

        # Deactivate sim mode button
        deactivate_sim_mode_btn = QPushButton("DEACTIVATE SIM", center_widget)
        deactivate_sim_mode_btn.setStyleSheet(button_style)
        deactivate_sim_mode_btn.clicked.connect(lambda: self.deactivate_sim)
        button_layout.addWidget(deactivate_sim_mode_btn, 1, 2)

        # Activate audio beacon button
        activate_audio_beacon_btn = QPushButton("ACTIVATE BCN", center_widget)
        activate_audio_beacon_btn.setStyleSheet(button_style)
        activate_audio_beacon_btn.clicked.connect(lambda: self.actbcn)
        button_layout.addWidget(activate_audio_beacon_btn, 1, 3)

        # Deactivate audio beacon button
        deactivate_audio_beacon_btn = QPushButton("DEACTIVATE BCN", center_widget)
        deactivate_audio_beacon_btn.setStyleSheet(button_style)
        deactivate_audio_beacon_btn.clicked.connect(lambda: self.debcn)
        button_layout.addWidget(deactivate_audio_beacon_btn, 1, 4)

        # Start recording button
        start_recording_button = QPushButton("START RECORDING", center_widget)
        start_recording_button.setStyleSheet(button_style)
        start_recording_button.clicked.connect(lambda: self.rec)
        button_layout.addWidget(start_recording_button, 2, 0)

        # Stop recording button
        stop_recording_button = QPushButton("STOP RECORDING", center_widget)
        stop_recording_button.setStyleSheet(button_style)
        stop_recording_button.clicked.connect(lambda: self.stopr)
        button_layout.addWidget(stop_recording_button, 2, 1)

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
        center_layout.addLayout(button_layout)
        center_layout.addWidget(custom_command_title)
        center_layout.addLayout(command_layout)
        center_layout.addWidget(graphs_title)
        center_layout.addLayout(graph_layout)

    def on_button_click(self):
        print("Button clicked")
        self.model.increment_count()
        self.label.setText(f"Count: {self.model.count}")