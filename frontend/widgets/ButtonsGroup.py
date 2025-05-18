from PyQt5.QtWidgets import QPushButton, QGridLayout
from backend.Commands import Commands

class ButtonsGroup():
    def __init__(self, center_widget, xbee):

        commands = Commands()
       
        # Create a grid layout for the buttons
        button_style = '''QPushButton{font-size:20px; margin:5px; padding:10px; height:20px; width:175px;}'''
        self.button_layout = QGridLayout()
       
        # Set time button
        set_time_btn = QPushButton("SET TIME", center_widget)
        set_time_btn.setStyleSheet(button_style)
        set_time_btn.clicked.connect(lambda: commands.set_time_handler(xbee))
        self.button_layout.addWidget(set_time_btn, 0, 0)

        # Calibrate altitude to zero button
        calibrate_altitude_to_zero_btn = QPushButton("CAL ALTITUDE", center_widget)
        calibrate_altitude_to_zero_btn.setStyleSheet(button_style)
        calibrate_altitude_to_zero_btn.clicked.connect(lambda: commands.cal_altitude_handler(xbee))
        self.button_layout.addWidget(calibrate_altitude_to_zero_btn, 0, 1) 

        # Set pitch, roll button
        set_pitch_roll_btn = QPushButton("CAL PR", center_widget)
        set_pitch_roll_btn.setStyleSheet(button_style)
        set_pitch_roll_btn.clicked.connect(lambda: commands.set_pr_handler(xbee))
        self.button_layout.addWidget(set_pitch_roll_btn, 0, 2)

        # Enable sim mode button
        enable_sim_mode_btn = QPushButton("ENABLE SIM", center_widget)
        enable_sim_mode_btn.setStyleSheet(button_style)
        enable_sim_mode_btn.clicked.connect(lambda: commands.enable_sim_mode_handler(xbee))
        self.button_layout.addWidget(enable_sim_mode_btn, 1, 0)

        # Activate sim mode button
        activate_sim_mode_btn = QPushButton("ACTIVATE SIM", center_widget)
        activate_sim_mode_btn.setStyleSheet(button_style)
        activate_sim_mode_btn.clicked.connect(lambda: commands.activate_sim_mode_handler(xbee))
        self.button_layout.addWidget(activate_sim_mode_btn, 1, 1)

        # Deactivate sim mode button
        deactivate_sim_mode_btn = QPushButton("DEACTIVATE SIM", center_widget)
        deactivate_sim_mode_btn.setStyleSheet(button_style)
        deactivate_sim_mode_btn.clicked.connect(lambda: commands.deactivate_sim_mode_handler(xbee))
        self.button_layout.addWidget(deactivate_sim_mode_btn, 1, 2)

        # TODO: buttons for activate MEC and deactivate MEC with the number
        # TODO: ST requires more parameters, UTC time or GPS and the time