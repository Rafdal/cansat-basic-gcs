import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

### TODO: Modify parameters

# TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
# TEMPERATURE, PRESSURE, VOLTAGE, GYRO_R, GYRO_P, GYRO_Y, ACCEL_R,
# ACCEL_P, ACCEL_Y, MAG_R, MAG_P, MAG_Y, AUTO_GYRO_ROTATION_RATE,
# GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS,
# CMD_ECHO [,,OPTIONAL_DATA]

# Team ID: 3165

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.mission_time = ""
        self.packet_count = 0
        self.mode = ""
        self.state = ""
        self.hs_deployed = 0
        self.pc_deployed = 0
        self.gps_time = ""
        self.gps_altitude = 0
        self.gps_latitude = 0
        self.gps_longitude = 0
        self.gps_sats = 0
        self.tilt_x = 0
        self.tilt_y = 0
        self.rot_z = 0
        self.cmd_echo = ""
        self.voltage = 0
        self.altitude = 0

        text_style = '''QLabel{font-size:20px; font-weight:600;}'''

        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)

        self.sidebar_widget.setStyleSheet("background-color: #FFFFFF;")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 200, 200)
        pixmap = QPixmap("frontend/assets/logo.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(190, 190)
            self.image_label.setPixmap(pixmap)

        self.label_team_number = QLabel("Team ITBA - 3165")
        self.label_team_number.setStyleSheet(text_style)

        self.label_mission_time = QLabel(f"Mission Time: {self.mission_time}")
        self.label_mission_time.setStyleSheet(text_style)

        self.label_packet_count = QLabel(f"Packet Count: {self.packet_count}")
        self.label_packet_count.setStyleSheet(text_style)

        self.label_mode = QLabel(f"Mode: {self.mode}")
        self.label_mode.setStyleSheet(text_style)

        self.label_state = QLabel(f"State: {self.state}")
        self.label_state.setStyleSheet(text_style)

        self.label_hs_deployed = QLabel(f"HS Deployed: {self.hs_deployed}")
        self.label_hs_deployed.setStyleSheet(text_style)

        self.label_pc_deployed = QLabel(f"PC Deployed: {self.pc_deployed}")
        self.label_pc_deployed.setStyleSheet(text_style)

        self.label_gps_time = QLabel(f"GPS Time: {self.gps_time}")
        self.label_gps_time.setStyleSheet(text_style)

        self.label_gps_altitude = QLabel(f"GPS Altitude: {self.gps_altitude}")
        self.label_gps_altitude.setStyleSheet(text_style)

        self.label_gps_latitude = QLabel(f"GPS Latitude: {self.gps_latitude}")
        self.label_gps_latitude.setStyleSheet(text_style)

        self.label_gps_longitude = QLabel(f"GPS Longitude: {self.gps_longitude}")
        self.label_gps_longitude.setStyleSheet(text_style)

        self.label_gps_sats = QLabel(f"GPS Sats: {self.gps_sats}")
        self.label_gps_sats.setStyleSheet(text_style)

        self.label_tilt_x = QLabel(f"Ax: {self.tilt_x}")
        self.label_tilt_x.setStyleSheet(text_style)

        self.label_tilt_y = QLabel(f"Ay: {self.tilt_y}")
        self.label_tilt_y.setStyleSheet(text_style)

        self.label_rot_z = QLabel(f"Az: {self.rot_z}")
        self.label_rot_z.setStyleSheet(text_style)

        self.label_cmd_echo = QLabel(f"Cmd Echo: {self.cmd_echo}")
        self.label_cmd_echo.setStyleSheet(text_style)

        self.label_voltage = QLabel(f"Battery Voltage: {self.voltage}")
        self.label_voltage.setStyleSheet(text_style)

        self.label_altitude = QLabel(f"Altitude: {self.altitude}")
        self.label_altitude.setStyleSheet(text_style)

        self.sidebar_widget.setStyleSheet("width: 200px;")

        # adding widgets to sidebar layout
        if not pixmap.isNull():
            self.sidebar_layout.addWidget(self.label_team_number)
        self.sidebar_layout.addWidget(self.image_label)
        self.sidebar_layout.addWidget(self.label_team_number)
        self.sidebar_layout.addWidget(self.label_mission_time)
        self.sidebar_layout.addWidget(self.label_packet_count)
        self.sidebar_layout.addWidget(self.label_mode)
        self.sidebar_layout.addWidget(self.label_state)
        self.sidebar_layout.addWidget(self.label_hs_deployed)
        self.sidebar_layout.addWidget(self.label_pc_deployed)
        self.sidebar_layout.addWidget(self.label_gps_time)
        self.sidebar_layout.addWidget(self.label_gps_altitude)
        self.sidebar_layout.addWidget(self.label_gps_latitude)
        self.sidebar_layout.addWidget(self.label_gps_longitude)
        self.sidebar_layout.addWidget(self.label_gps_sats)
        self.sidebar_layout.addWidget(self.label_tilt_x)
        self.sidebar_layout.addWidget(self.label_tilt_y)
        self.sidebar_layout.addWidget(self.label_rot_z)
        self.sidebar_layout.addWidget(self.label_cmd_echo)
        self.sidebar_layout.addWidget(self.label_voltage)
        self.sidebar_layout.addWidget(self.label_altitude)

    def update(self, mission_time, packet_count, mode, state, hs_deployed, pc_deployed, gps_time, gps_altitude, gps_latitude, gps_longitude, gps_sats, tilt_x, tilt_y, rot_z, cmd_echo, voltage, altitude):
        self.mission_time = mission_time
        self.packet_count = packet_count
        self.mode = mode
        self.state = state
        self.hs_deployed = hs_deployed
        self.pc_deployed = pc_deployed
        self.gps_time = gps_time
        self.gps_altitude = gps_altitude
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.gps_sats = gps_sats
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.rot_z = rot_z
        self.cmd_echo = cmd_echo
        self.voltage = voltage
        self.altitude = altitude

        self.label_mission_time.setText(f"Mission Time: {self.mission_time}")
        self.label_packet_count.setText(f"Packet Count: {self.packet_count}")
        self.label_mode.setText(f"Mode: {self.mode}")
        self.label_state.setText(f"State: {self.state}")
        self.label_hs_deployed.setText(f"HS Deployed: {self.hs_deployed}")
        self.label_pc_deployed.setText(f"PC Deployed: {self.pc_deployed}")
        self.label_gps_time.setText(f"GPS Time: {self.gps_time}")
        self.label_gps_altitude.setText(f"GPS Altitude: {self.gps_altitude}")
        self.label_gps_latitude.setText(f"GPS Latitude: {self.gps_latitude}")
        self.label_gps_longitude.setText(f"GPS Longitude: {self.gps_longitude}")
        self.label_gps_sats.setText(f"GPS Sats: {self.gps_sats}")
        self.label_tilt_x.setText(f"Ax: {self.tilt_x}")
        self.label_tilt_y.setText(f"Ay: {self.tilt_y}")
        self.label_rot_z.setText(f"Az: {self.rot_z}")
        self.label_cmd_echo.setText(f"Cmd Echo: {self.cmd_echo}")
        self.label_voltage.setText(f"Battery Voltage: {voltage}")
        self.label_altitude.setText(f"Altitude: {self.altitude}")