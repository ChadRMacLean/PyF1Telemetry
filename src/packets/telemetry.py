import struct
import ctypes
import json

from . import header


class CarTelemetryData:
    
    def __init__(self):
        self.m_speed = ctypes.c_uint16(0)
        self.m_throttle = ctypes.c_float(0)
        self.m_steer = ctypes.c_float(0)
        self.m_brake = ctypes.c_float(0)
        self.m_clutch = ctypes.c_uint8(0)
        self.m_gear = ctypes.c_int8(0)
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
        self.m_clutch = ctypes.c_uint8(data[4])
        self.m_gear = ctypes.c_int8(data[5])
        self.m_engineRPM = ctypes.c_uint16(data[6])
        self.m_drs = ctypes.c_uint8(data[7])
        self.m_revLightsPercent = ctypes.c_uint8(data[8])
        self.m_brakesTemperature = [ctypes.c_uint16(data[i]) for i in range(9, 13)]
        self.m_tyresSurfaceTemperature = [ctypes.c_uint8(data[i]) for i in range(13, 17)]
        self.m_tyresInnerTemperature = [ctypes.c_uint8(data[i]) for i in range(17, 21)]
        self.m_engineTemperature = ctypes.c_uint16(data[21])
        self.m_tyrePressure = [ctypes.c_float(data[i]) for i in range(22, 26)]
        self.m_surfaceType = [ctypes.c_uint8(data[i]) for i in range(26, 30)]


class PacketCarTelemetryData:
    
    car_telemetry_data_format = "HfffBbHBBHHHHBBBBBBBBHffffBBBB"
    extra_telemetry_data_format = "LBBb"

    def __init__(self):
        self.m_carTelemetryData = [CarTelemetryData() for x in range(22)]
        
        self.packet_format = "".join(self.car_telemetry_data_format * 22) + self.extra_telemetry_data_format
        
        self.m_buttonStatus = ctypes.c_uint32(0)
        self.m_mfdPanelIndex = ctypes.c_uint8(0)
        self.m_mfdPanelIndexSecondaryPlayer = ctypes.c_uint8(0)
        self.m_suggestedGear = ctypes.c_int8(0)
        
    
    def get_telemetry(self, player_car_index):
        telemetry_data = {
            "m_speed" : self.m_carTelemetryData[player_car_index].m_speed.value,
            "m_throttle" : self.m_carTelemetryData[player_car_index].m_throttle.value,
            "m_steer" : self.m_carTelemetryData[player_car_index].m_steer.value,
            "m_brake" : self.m_carTelemetryData[player_car_index].m_brake.value,
            "m_clutch" : self.m_carTelemetryData[player_car_index].m_clutch.value,
            "m_gear" : self.m_carTelemetryData[player_car_index].m_gear.value,
            "m_engineRPM" : self.m_carTelemetryData[player_car_index].m_engineRPM.value,
            "m_drs" : self.m_carTelemetryData[player_car_index].m_drs.value,
            "m_revLightsPercent" : self.m_carTelemetryData[player_car_index].m_revLightsPercent.value,
            "m_brakesTemperature" : { 
                "RL" : self.m_carTelemetryData[player_car_index].m_brakesTemperature[0].value, 
                "RR" : self.m_carTelemetryData[player_car_index].m_brakesTemperature[1].value, 
                "FL" : self.m_carTelemetryData[player_car_index].m_brakesTemperature[2].value, 
                "FR" : self.m_carTelemetryData[player_car_index].m_brakesTemperature[3].value
            },
            "m_tyresSurfaceTemperature" : { 
                "RL" : self.m_carTelemetryData[player_car_index].m_tyresSurfaceTemperature[0].value, 
                "RR" : self.m_carTelemetryData[player_car_index].m_tyresSurfaceTemperature[1].value, 
                "FL" : self.m_carTelemetryData[player_car_index].m_tyresSurfaceTemperature[2].value, 
                "FR" : self.m_carTelemetryData[player_car_index].m_tyresSurfaceTemperature[3].value,
            },
            "m_tyresInnerTemperature" : { 
                "RL" : self.m_carTelemetryData[player_car_index].m_tyresInnerTemperature[0].value,
                "RR" : self.m_carTelemetryData[player_car_index].m_tyresInnerTemperature[1].value, 
                "FL" : self.m_carTelemetryData[player_car_index].m_tyresInnerTemperature[2].value,
                "FR" : self.m_carTelemetryData[player_car_index].m_tyresInnerTemperature[3].value
            },
            "m_engineTemperature" : self.m_carTelemetryData[player_car_index].m_engineTemperature.value,
            "m_tyrePressure" : { 
                "RL" : self.m_carTelemetryData[player_car_index].m_tyrePressure[0].value,
                "RR" : self.m_carTelemetryData[player_car_index].m_tyrePressure[1].value,
                "FL" : self.m_carTelemetryData[player_car_index].m_tyrePressure[2].value,
                "FR" : self.m_carTelemetryData[player_car_index].m_tyrePressure[3].value
            },
            "m_surfaceType" : { 
                "RL" : self.m_carTelemetryData[player_car_index].m_surfaceType[0].value,
                "RR" : self.m_carTelemetryData[player_car_index].m_surfaceType[1].value,
                "FL" : self.m_carTelemetryData[player_car_index].m_surfaceType[2].value,
                "FR" : self.m_carTelemetryData[player_car_index].m_surfaceType[3].value,
            }
        }
        
        json_telemetry = json.dumps(telemetry_data)
        
        return json_telemetry
        
        
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

        for index, car in enumerate(self.m_carTelemetryData):
            car.update(car_data_list[index])
        
        return unpacked
        
        
header = header.Header()