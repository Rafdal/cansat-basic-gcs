from PyQt5.QtWidgets import QPushButton, QGridLayout

class ButtonsGroup():
    def __init__(self, center_widget):
       
        # Create a grid layout for the buttons
        button_style = '''QPushButton{font-size:20px; margin:5px; padding:10px; height:20px; width:175px;}'''
        self.button_layout = QGridLayout()
       
        # Set time button
        set_time_btn = QPushButton("SET TIME", center_widget)
        set_time_btn.setStyleSheet(button_style)
        set_time_btn.clicked.connect(lambda: self.set_time())
        self.button_layout.addWidget(set_time_btn, 0, 0)

        # Start telemetry button
        start_telemetry_btn = QPushButton("START TELEMETRY", center_widget)
        start_telemetry_btn.setStyleSheet(button_style)
        start_telemetry_btn.clicked.connect(lambda: self.start_telemetry())
        self.button_layout.addWidget(start_telemetry_btn, 0, 1)

        # End telemetry button
        end_telemetry_btn = QPushButton("END TELEMETRY", center_widget)
        end_telemetry_btn.setStyleSheet(button_style)
        end_telemetry_btn.clicked.connect(lambda: self.end_telemetry())
        self.button_layout.addWidget(end_telemetry_btn, 0, 2)

        # Calibrate altitude to zero button
        calibrate_altitude_to_zero_btn = QPushButton("CAL ALTITUDE", center_widget)
        calibrate_altitude_to_zero_btn.setStyleSheet(button_style)
        calibrate_altitude_to_zero_btn.clicked.connect(lambda: self.cal)
        self.button_layout.addWidget(calibrate_altitude_to_zero_btn, 0, 3)

        # Set pitch, yaw, roll button
        set_pitch_yaw_roll_btn = QPushButton("SET PYR", center_widget)
        set_pitch_yaw_roll_btn.setStyleSheet(button_style)
        set_pitch_yaw_roll_btn.clicked.connect(lambda: self.pyr)
        self.button_layout.addWidget(set_pitch_yaw_roll_btn, 0, 4)

        # Enable sim mode button
        enable_sim_mode_btn = QPushButton("ENABLE SIM", center_widget)
        enable_sim_mode_btn.setStyleSheet(button_style)
        enable_sim_mode_btn.clicked.connect(lambda: self.enable_sim)
        self.button_layout.addWidget(enable_sim_mode_btn, 1, 0)

        # Activate sim mode button
        activate_sim_mode_btn = QPushButton("ACTIVATE SIM", center_widget)
        activate_sim_mode_btn.setStyleSheet(button_style)
        activate_sim_mode_btn.clicked.connect(lambda: self.activate_sim)
        self.button_layout.addWidget(activate_sim_mode_btn, 1, 1)

        # Deactivate sim mode button
        deactivate_sim_mode_btn = QPushButton("DEACTIVATE SIM", center_widget)
        deactivate_sim_mode_btn.setStyleSheet(button_style)
        deactivate_sim_mode_btn.clicked.connect(lambda: self.deactivate_sim)
        self.button_layout.addWidget(deactivate_sim_mode_btn, 1, 2)

        # Activate audio beacon button
        activate_audio_beacon_btn = QPushButton("ACTIVATE BCN", center_widget)
        activate_audio_beacon_btn.setStyleSheet(button_style)
        activate_audio_beacon_btn.clicked.connect(lambda: self.actbcn)
        self.button_layout.addWidget(activate_audio_beacon_btn, 1, 3)

        # Deactivate audio beacon button
        deactivate_audio_beacon_btn = QPushButton("DEACTIVATE BCN", center_widget)
        deactivate_audio_beacon_btn.setStyleSheet(button_style)
        deactivate_audio_beacon_btn.clicked.connect(lambda: self.debcn)
        self.button_layout.addWidget(deactivate_audio_beacon_btn, 1, 4)

        # Start recording button
        start_recording_button = QPushButton("START RECORDING", center_widget)
        start_recording_button.setStyleSheet(button_style)
        start_recording_button.clicked.connect(lambda: self.rec)
        self.button_layout.addWidget(start_recording_button, 2, 0)

        # Stop recording button
        stop_recording_button = QPushButton("STOP RECORDING", center_widget)
        stop_recording_button.setStyleSheet(button_style)
        stop_recording_button.clicked.connect(lambda: self.stopr)
        self.button_layout.addWidget(stop_recording_button, 2, 1)                