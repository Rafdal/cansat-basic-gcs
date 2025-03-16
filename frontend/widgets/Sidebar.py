import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Team ID: 3165

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.mission_time = ""
        self.packet_count = 0
        self.mode = ""
        self.state = ""
        self.altitude = 0
        self.temperature = 0
        self.pressure = 0
        self.voltage = 0
        self.gyro_r = 0
        self.gyro_p = 0
        self.gyro_y = 0
        self.accel_r = 0
        self.accel_p = 0
        self.accel_y = 0
        self.mag_r = 0
        self.mag_p = 0
        self.mag_y = 0
        self.autogyro_desc_rate = 0
        self.gps_time = ""
        self.gps_altitude = 0
        self.gps_latitude = 0
        self.gps_longitude = 0
        self.gps_sats = 0
        self.cmd_echo = ""

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

        self.label_altitude = QLabel(f"Altitude: {self.altitude}")
        self.label_altitude.setStyleSheet(text_style)

        self.label_temperature = QLabel(f"Temperature: {self.temperature}")
        self.label_temperature.setStyleSheet(text_style)

        self.label_pressure = QLabel(f"Pressure: {self.pressure}")
        self.label_pressure.setStyleSheet(text_style)

        self.label_voltage = QLabel(f"Voltage: {self.voltage}")
        self.label_voltage.setStyleSheet(text_style)

        self.label_gyro_r = QLabel(f"Gyro r: {self.gyro_r}")
        self.label_gyro_r.setStyleSheet(text_style)

        self.label_gyro_p = QLabel(f"Gyro p: {self.gyro_p}")
        self.label_gyro_p.setStyleSheet(text_style)

        self.label_gyro_y = QLabel(f"Gyro y: {self.gyro_y}")
        self.label_gyro_y.setStyleSheet(text_style)

        self.label_accel_r = QLabel(f"Accel r: {self.accel_r}")
        self.label_accel_r.setStyleSheet(text_style)

        self.label_accel_p = QLabel(f"Accel p: {self.accel_p}")
        self.label_accel_p.setStyleSheet(text_style)

        self.label_accel_y = QLabel(f"Accel y: {self.accel_y}")
        self.label_accel_y.setStyleSheet(text_style)

        self.label_mag_r = QLabel(f"Mag r: {self.mag_r}")
        self.label_mag_r.setStyleSheet(text_style)

        self.label_mag_p = QLabel(f"Mag p: {self.mag_p}")
        self.label_mag_p.setStyleSheet(text_style)

        self.label_mag_y = QLabel(f"Mag y: {self.mag_y}")
        self.label_mag_y.setStyleSheet(text_style)

        self.label_autogyro_desc_rate = QLabel(f"Autogyro descent rate: {self.autogyro_desc_rate}")
        self.label_autogyro_desc_rate.setStyleSheet(text_style)

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

        self.label_cmd_echo = QLabel(f"CMD Echo: {self.cmd_echo}")
        self.label_cmd_echo.setStyleSheet(text_style)

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
        self.sidebar_layout.addWidget(self.label_altitude)
        self.sidebar_layout.addWidget(self.label_temperature)
        self.sidebar_layout.addWidget(self.label_pressure)
        self.sidebar_layout.addWidget(self.label_voltage)
        self.sidebar_layout.addWidget(self.label_gyro_r)
        self.sidebar_layout.addWidget(self.label_gyro_p)
        self.sidebar_layout.addWidget(self.label_gyro_y)
        self.sidebar_layout.addWidget(self.label_accel_r)
        self.sidebar_layout.addWidget(self.label_accel_p)
        self.sidebar_layout.addWidget(self.label_accel_y)
        self.sidebar_layout.addWidget(self.label_mag_r)
        self.sidebar_layout.addWidget(self.label_mag_p)
        self.sidebar_layout.addWidget(self.label_mag_y)
        self.sidebar_layout.addWidget(self.label_autogyro_desc_rate)
        self.sidebar_layout.addWidget(self.label_gps_time)
        self.sidebar_layout.addWidget(self.label_gps_altitude)
        self.sidebar_layout.addWidget(self.label_gps_latitude)
        self.sidebar_layout.addWidget(self.label_gps_longitude)
        self.sidebar_layout.addWidget(self.label_gps_sats)
        self.sidebar_layout.addWidget(self.label_cmd_echo)

    def update(
            self, mission_time, packet_count, mode, state, altitude, 
            temperature, pressure, voltage, gyro_r, gyro_p, gyro_y, 
            accel_r, accel_p, accel_y, mag_r, mag_p, mag_y, 
            autogyro_desc_rate, gps_time, gps_altitude, 
            gps_latitude, gps_longitude, gps_sats, cmd_echo
        ):
        self.mission_time = mission_time
        self.packet_count = packet_count
        self.mode = mode
        self.state = state
        self.temperature = temperature
        self.pressure = pressure
        self.voltage = voltage
        self.gyro_r = gyro_r
        self.gyro_p = gyro_p
        self.gyro_y = gyro_y
        self.accel_r = accel_r
        self.accel_p = accel_p
        self.accel_y = accel_y
        self.mag_r = mag_r
        self.mag_p = mag_p
        self.mag_y = mag_y
        self.autogyro_desc_rate = autogyro_desc_rate
        self.gps_time = gps_time
        self.gps_altitude = gps_altitude
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.gps_sats = gps_sats
        self.cmd_echo = cmd_echo

        self.label_mission_time.setText(f"Mission Time: {self.mission_time}")
        self.label_packet_count.setText(f"Packet Count: {self.packet_count}")
        self.label_mode.setText(f"Mode: {self.mode}")
        self.label_state.setText(f"State: {self.state}")
        self.label_temperature.setText(f"Temperature: {self.temperature}")
        self.label_voltage.setText(f"Voltage: {self.voltage}")
        self.label_gyro_r.setText(f"Gyro r: {self.gyro_r}")
        self.label_gyro_p.setText(f"Gyro p: {self.gyro_p}")
        self.label_gyro_y.setText(f"Gyro y: {self.gyro_y}")
        self.label_accel_r.setText(f"Accel r: {self.accel_r}")
        self.label_accel_p.setText(f"Accel p: {self.accel_p}")
        self.label_accel_y.setText(f"Accel y: {self.accel_y}")
        self.label_mag_r.setText(f"Mag r: {self.mag_r}")
        self.label_mag_p.setText(f"Mag p: {self.mag_p}")
        self.label_mag_y.setText(f"Mag y: {self.mag_y}")
        self.label_autogyro_desc_rate.setText(f"Autogyro descent rate: {self.autogyro_desc_rate}")
        self.label_gps_time.setText(f"GPS Time: {self.gps_time}")
        self.label_gps_altitude.setText(f"GPS Altitude: {self.gps_altitude}")
        self.label_gps_latitude.setText(f"GPS Latitude: {self.gps_latitude}")
        self.label_gps_longitude.setText(f"GPS Longitude: {self.gps_longitude}")
        self.label_gps_sats.setText(f"GPS Sats: {self.gps_sats}")
        self.label_cmd_echo.setText(f"Cmd Echo: {self.cmd_echo}")

