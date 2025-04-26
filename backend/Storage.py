import csv
import os

class Storage():
    def __init__(self):
        self.file_path = "flight_3165.csv"
        # TODO: add a timestamp to the file name to avoid overwriting
    def open(self):
        file_number = 0
        while (os.path.exists(self.file_path)):
            file_number += 1
            self.file_path = f"flight_2099_{file_number}.csv"

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
