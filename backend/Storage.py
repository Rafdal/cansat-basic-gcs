import csv
import os
from datetime import datetime

class Storage():
    def __init__(self):
        dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_path = f"flight_3165_{dt}.csv"

        # TODO: For the actual flight, remove the datetime

    def open(self):
        with open(self.file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "TEMPERATURE", 
                             "PRESSURE", "VOLTAGE", "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y", 
                             "MAG_R", "MAG_P", "MAG_Y", "AUTO_GYRO_ROTATION_RATE", "GPS_TIME", "GPS_ALTITUDE", 
                             "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"])
        print("Created file " + self.file_path)


    def write(self, data):
        with open(self.file_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            print("Data written to file")
