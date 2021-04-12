import struct
import ctypes

from . import header


class CarMotionData:

    def __init__(self):
        self.m_worldPositionX = ctypes.c_float(0)
        self.m_worldPositionY = ctypes.c_float(0)
        self.m_worldPositionZ = ctypes.c_float(0)
        self.m_worldVelocityX = ctypes.c_float(0)
        self.m_worldVelocityY = ctypes.c_float(0)
        self.m_worldVelocityZ = ctypes.c_float(0)
        self.m_worldForwardDirX = ctypes.c_int16(0)
        self.m_worldForwardDirY = ctypes.c_int16(0)
        self.m_worldForwardDirZ = ctypes.c_int16(0)
        self.m_worldRightDirX = ctypes.c_int16(0)
        self.m_worldRightDirY = ctypes.c_int16(0)
        self.m_worldRightDirZ = ctypes.c_int16(0)
        self.m_gForceLateral = ctypes.c_float(0)
        self.m_gForceLongitudinal = ctypes.c_float(0)
        self.m_gForceVertical = ctypes.c_float(0)
        self.m_yaw = ctypes.c_float(0)
        self.m_pitch = ctypes.c_float(0)
        self.m_roll = ctypes.c_float(0)
        

    def update(self, data):
        self.m_worldPositionX = ctypes.c_float(data[0])
        self.m_worldPositionY = ctypes.c_float(data[1])
        self.m_worldPositionZ = ctypes.c_float(data[2])
        self.m_worldVelocityX = ctypes.c_float(data[3])
        self.m_worldVelocityY = ctypes.c_float(data[4])
        self.m_worldVelocityZ = ctypes.c_float(data[5])
        self.m_worldForwardDirX = ctypes.c_int16(data[6])
        self.m_worldForwardDirY = ctypes.c_int16(data[7])
        self.m_worldForwardDirZ = ctypes.c_int16(data[8])
        self.m_worldRightDirX = ctypes.c_int16(data[9])
        self.m_worldRightDirY = ctypes.c_int16(data[10])
        self.m_worldRightDirZ = ctypes.c_int16(data[11])
        self.m_gForceLateral = ctypes.c_float(data[12])
        self.m_gForceLongitudinal = ctypes.c_float(data[13])
        self.m_gForceVertical = ctypes.c_float(data[14])
        self.m_yaw = ctypes.c_float(data[15])
        self.m_pitch = ctypes.c_float(data[16])
        self.m_roll = ctypes.c_float(data[17])


class PacketMotionData:
    
    car_motion_data_format = "ffffffHHHHHHffffff"
    extra_player_car_format = "fffffffffffffff"

    def __init__(self):
        self.m_carMotionData = [CarMotionData() for x in range(22)]
        
        self.packet_format = "".join(self.car_motion_data_format * 22) + self.extra_player_car_format
        
        self.m_suspensionPosition = [ctypes.c_float(0) for x in range(0, 4)]
        self.m_suspensionVelocity = [ctypes.c_float(0) for x in range(0, 4)]
        self.m_suspensionAcceleration = [ctypes.c_float(0) for x in range(0, 4)]
        self.m_wheelSpeed = [ctypes.c_float(0) for x in range(0, 4)]
        self.m_wheelSlip = [ctypes.c_float(0) for x in range(0, 4)]
        self.m_localVelocityX = ctypes.c_float(0)
        self.m_localVelocityY = ctypes.c_float(0)
        self.m_localVelocityZ = ctypes.c_float(0)
        self.m_angularVelocityX = ctypes.c_float(0)
        self.m_angularVelocityY = ctypes.c_float(0)
        self.m_angularAccelerationX = ctypes.c_float(0)
        self.m_angularAccelerationY = ctypes.c_float(0)
        self.m_angularAccelerationZ = ctypes.c_float(0)
        self.m_frontWheelsAngle = ctypes.c_float(0)


    def unpack_struct(self, format, data):
        # Unpack packet with provided format and data.
        unpacked = struct.unpack_from(format, data)

        # Set length to size of header packet.
        data_buffer = len(header.packet_header_format)

        # Remove header from unpacked packet.
        unpacked = unpacked[data_buffer::]

        car_data_buffer = len(self.car_motion_data_format)
        number_of_cars = int((len(unpacked) - len(self.extra_player_car_format)) / car_data_buffer)

        car_data_list = [unpacked[i*car_data_buffer:(i*car_data_buffer) + car_data_buffer] for i in range(number_of_cars)]

        for index, car in enumerate(self.m_carMotionData):
            car.update(car_data_list[index])
        
        return unpacked

        
header = header.Header()