import struct


class Header:

    little_endian = "<"
    packet_header_format = "HBBBBQfLBB"
    packet_format = little_endian + packet_header_format

    m_packetFormat = 0
    m_gameMajorVersion = 0
    m_gameMinorVersion = 0
    m_packetVersion = 0
    m_packetId = 0
    m_sessionUID = 0
    m_sessionTime = 0
    m_frameIdentifier = 0
    m_playerCarIndex = 0
    m_secondaryPlayerCarIndex = 0


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
