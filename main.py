import sock
import curses
import time

from packets import header
from packets import motion
from packets import telemetry

# b = int8
# B = uint8
# H = uint16
# L = uint32
# Q = uint64
# f = float

class Main:
    
    struct_size = 9914

    def __init__(self):
        self.sock = sock.Socket()
        self.obj_header = header.Header()
        self.obj_motion = motion.PacketMotionData()
        self.obj_telemetry = telemetry.PacketCarTelemetryData()

        self.run()

    
    def run(self):
        while True:
            data = self.sock.recv(self.struct_size)
            
            if data:
                self.obj_header.unpack_struct(self.obj_header.packet_format, data)

                if self.obj_header.m_packetId == 0: self.motion(data)
                if self.obj_header.m_packetId == 1: self.session(data)
                if self.obj_header.m_packetId == 2: self.lap(data)
                if self.obj_header.m_packetId == 3: self.event(data)
                if self.obj_header.m_packetId == 4: self.participants(data)
                if self.obj_header.m_packetId == 5: self.setups(data)
                if self.obj_header.m_packetId == 6: self.telemetry(data)
                if self.obj_header.m_packetId == 7: self.status(data)
                if self.obj_header.m_packetId == 8: self.classification
                if self.obj_header.m_packetId == 9: self.lobby(data)
                
                self.output()
                
    
    def output(self, stdscr=None):
        player_car_index = self.obj_header.m_playerCarIndex
        player_telemetry_data = self.obj_telemetry.m_carTelemetryData[player_car_index]
        
        display = ["Speed: " + str(player_telemetry_data.m_speed.value),
                   "Engine RPM: " + str(player_telemetry_data.m_engineRPM.value),
                   "Engine Temperature: " + str(player_telemetry_data.m_engineTemperature.value)]
        
        stdscr = curses.initscr()
        
        curses.curs_set(0)
        
        curses_h, curses_w = stdscr.getmaxyx()
        
        for index, row in enumerate(display):
            pos_x = curses_w//2 - len(row)//2
            pos_y = curses_h//2 - len(display)//2 + index
            stdscr.addstr(pos_y, pos_x, row)
        
        stdscr.refresh()  
        stdscr.clear()
            

    def motion(self, data):
        packet_format = self.obj_header.packet_format + self.obj_motion.packet_format
        self.obj_motion.unpack_struct(packet_format, data)


    def session(self, data):
        pass
        # print("Session Packet")


    def lap(self, data):
        pass
        # print("Lap Data Packet")


    def event(self, data):
        pass
        # print("Event Packet")


    def participants(self, data):
        pass
        # print("Participants Packet")   


    def setups(self, data):
        pass
        # print("Car Setups Packet")


    def telemetry(self, data):
        packet_format = self.obj_header.packet_format + self.obj_telemetry.packet_format
        self.obj_telemetry.unpack_struct(packet_format, data)


    def status(self, data):
        pass
        # print("Car Status Packet")


    def classification(self, data):
        pass
        # print("Final Classification Packet")


    def lobby(self, data):
        pass
        # print("Lobby Info Packet")


main = Main()