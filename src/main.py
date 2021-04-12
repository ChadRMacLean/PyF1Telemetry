import curses
import time
import sys

import socketserver
import http.server
import socket
import json

from backend import data 

from packets import cmsocket
from packets import header
from packets import motion
from packets import telemetry

# b = int8
# B = uint8
# H = uint16
# L = uint32
# Q = uint64
# f = float

class Handler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/" : self.path = "/src/frontend/"
        
        if self.path == "/src/backend/data.py" : 
            self.respond(Main.get_telemetry(Main))
            return http.server.SimpleHTTPRequestHandler.do_HEAD(self)
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    
    def handle_http(self, data):
        self.send_response_only(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        print(data)
        
        return bytes(data, "utf8")
    
    
    def respond(self, data):
        response = self.handle_http(data)
        self.wfile.write(response)
        

class Main:
    
    port = 20775
    
    struct_size = 9914
    
    obj_sock = cmsocket.CMSocket()
    obj_header = header.Header()
    obj_motion = motion.PacketMotionData()
    obj_telemetry = telemetry.PacketCarTelemetryData()

    def __init__(self):
        self.handler = Handler
        self.run_server()
        self.main()
        
        
    def run_server(self):
        host_name = socket.gethostname()
        host_addr = socket.gethostbyname(host_name)
        
        with socketserver.TCPServer((host_addr, self.port), self.handler) as httpd:
            httpd.serve_forever()

    
    def main(self):
        while True:
            data = self.obj_sock.recv(self.struct_size)
            
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
        
        stdscr.clear()
        
        for index, row in enumerate(display):
            pos_x = curses_w//2 - len(row)//2
            pos_y = curses_h//2 - len(display)//2 + index
            stdscr.addstr(pos_y, pos_x, row)
        
        stdscr.refresh()  
            

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
        
    def get_telemetry(self):
        json_telemetry = self.obj_telemetry.get_telemetry(self.obj_header.m_playerCarIndex)
        return json_telemetry


main = Main()