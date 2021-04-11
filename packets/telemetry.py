import struct
import ctypes

from . import header


class CarTelemetryData:
    
    def __init__(self):
        self.m_speed = ctypes.c_uint16(0)
        self.m_throttle = ctypes.c_float(0)
        self.m_steer = ctypes.c_float(0)
        self.m_brake = ctypes.c_float(0)
        self.m_cluth = ctypes.c_uint8(0)
        self.m_gear = ctypes.c_int8
        self.m_engineRPM = ctypes.c_uint16(0)
        self.m_drs = ctypes.c_uint8(0)
        self.m_revLightsPercent = ctypes.c_uint8(0)
        self.m_brakesTemperature = [ctypes.c_uint16(0) for i in range(4)]
        self.m_tyresSurfaceTemperature = [ctypes.c_uint8(0) for i in range(4)]
        self.m_tyresInnerTemperature = [ctypes.c_uint8(0) for i in range(4)]
        self.m_engineTemperature = ctypes.c_uint16(0)
        self.m_tyrePressure = [ctypes.c_float(0) for i in range(4)]
        self.m_surfaceType = [ctypes.c_uint8(0) for i in range(4)]
        
        
    def update(self, data):
        self.m_speed = ctypes.c_uint16(data[0])
        self.m_throttle = ctypes.c_float(data[1])
        self.m_steer = ctypes.c_float(data[2])
        self.m_brake = ctypes.c_float(data[3])
        self.m_cluth = ctypes.c_uint8(data[4])
        self.m_gear = ctypes.c_int8(data[5])
        self.m_engineRPM = ctypes.c_uint16(data[6])
        self.m_drs = ctypes.c_uint8(data[7])
        self.m_revLightsPercent = ctypes.c_uint8(data[8])
        self.m_brakesTemperature = [ctypes.c_uint16(data[i]) for i in range(9, 13)]
        self.m_tyresSurfaceTemperature = [ctypes.c_uint8(data[i]) for i in range(13, 17)]
        self.m_tyresInnerTemperature = [ctypes.c_uint8(data[i]) for i in range(17, 21)]
        self.m_engineTemperature = ctypes.c_uint16(data[22])
        self.m_tyrePressure = [ctypes.c_float(data[i]) for i in range(23, 27)]
        self.m_surfaceType = [ctypes.c_uint8(data[i]) for i in range(27, 31)]


# b = int8
# B = uint8
# H = uint16
# L = uint32
# Q = uint64
# f = float


class PacketCarTelemetryData:

    def __init__(self):
        self.car_telemetry_data_format = "HfffBbHBBHHHHBBBBBBBBHffffBBBB"
        self.extra_telemetry_data_format = "LBBb"

        self.m_carTelemetryData = [CarTelemetryData for x in range(22)]
        
        self.packet_format = "".join(self.car_telemetry_data_format * 22) + self.extra_telemetry_data_format
        
        self.m_buttonStatus = ctypes.c_uint32(0)
        self.m_mfdPanelIndex = ctypes.c_uint8(0)
        self.m_mfdPanelIndexSecondaryPlayer = ctypes.c_uint8(0)
        self.m_suggestedGear = ctypes.c_int8(0)
        
        
    def unpack_struct(self, format, data):
        # Unpack packet with provided format and data.
        unpacked = struct.unpack_from(format, data)

        # Set length to size of header packet.
        data_buffer = len(header.packet_header_format)

        # Remove header from unpacked packet.
        unpacked = unpacked[data_buffer::]

        car_data_buffer = len(self.car_telemetry_data_format)
        number_of_cars = int((len(unpacked) - len(self.extra_telemetry_data_format)) / car_data_buffer)

        car_data_list = [unpacked[i*car_data_buffer:(i*car_data_buffer) + car_data_buffer] for i in range(number_of_cars)]
        
        print("Speed: " + str(car_data_list[0][0]))

        # for index, car in enumerate(self.m_carTelemetryData):
        #     car.update(car, car_data_list[index])
        
        return unpacked
        
        
header = header.Header()