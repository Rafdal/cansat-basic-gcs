import csv
import os

## TODO: Change team number
## TODO: Change headers
class Storage():
    def __init__(self):
        self.file_path = "flight_2099.csv"

    def open(self):
        file_number = 0
        while (os.path.exists(self.file_path)):
            file_number += 1
            self.file_path = f"flight_2099_{file_number}.csv"

        with open(self.file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "AIR_SPEED", "HS_DEPLOYED", "PC_DEPLOYED", "TEMPERATURE", "VOLTAGE", "PRESSURE", "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "TILT_X", "TILT_Y", "ROT_Z", "CMD_ECHO"])
        print("Created file " + self.file_path)
    
    def write(self, data):
        with open(self.file_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            print("Data written to file")
