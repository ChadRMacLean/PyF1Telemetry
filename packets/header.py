import struct


class Header:

    little_endian = "<"
    packet_header_format = "HBBBBQfLBB"
    packet_format = little_endian + packet_header_format

    def __init__(self): 
        self.m_packetFormat = 0
        self.m_gameMajorVersion = 0
        self.m_gameMinorVersion = 0
        self.m_packetVersion = 0
        self.m_packetId = 0
        self.m_sessionUID = 0
        self.m_sessionTime = 0
        self.m_frameIdentifier = 0
        self.m_playerCarIndex = 0
        self.m_secondaryPlayerCarIndex = 0
        

    def unpack_struct(self, format, data):
        unpacked = struct.unpack_from(format, data)
        
        self.m_packetFormat = unpacked[0]
        self.m_gameMajorVersion = unpacked[1]
        self.m_gameMinorVersion = unpacked[2]
        self.m_packetVersion = unpacked[3]
        self.m_packetId = unpacked[4]
        self.m_sessionUID = unpacked[5]
        self.m_sessionTime = unpacked[6]
        self.m_frameIdentifier = unpacked[7]
        self.m_playerCarIndex = unpacked[8]
        self.m_secondaryPlayerCarIndex = unpacked[9]

        return unpacked
