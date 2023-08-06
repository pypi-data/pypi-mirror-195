from binascii import unhexlify
from enum import Enum
import struct

from attrs import define, field
from . import SensorType


SAMPLE = unhexlify("0dff5900035f3fbe42877ded2bc60302e5fe")


class Battery(Enum):
    CR2032 = 1


@define
class Mopeka:
    battery_volts: float
    tank_fill_mm: int
    tank_quality: int
    sensor_id: int
    temperature: int
    tank_height_mm: int = field(kw_only=True, default=0)
    battery_type: Battery = field(kw_only=True, default=Battery.CR2032)

    @classmethod
    def from_hex(cls, h):
        return cls.from_bytes(unhexlify(h))

    @staticmethod
    def tank_process(tank1, tank2, temp):
        """ Takes raw beacon value and calculates mm height and confidence"""
        raw = (tank2 * 256) + tank1
        raw = raw & 0x3fff
        tank_height = int(
            raw * (0.573045 + (-0.002822 * temp) + (-0.00000535 * temp**2)))
        tank_confidence = (tank2 >> 6) & 0x3
        return (tank_height, tank_confidence)

    @classmethod
    def from_bytes(cls, b: bytes):
        (batt, temp, tank1, tank2, sensor_id) = struct.unpack(
            "<BBBB3s", b[5:12])
        batt = (batt & 0x7f) / 32
        temp = temp & 0x7f
        (tank_fill_mm, tank_quality) = cls.tank_process(tank1, tank2, temp)
        sensor_id = int.from_bytes(sensor_id, "little")
        temp = temp - 40
        return cls(batt, tank_fill_mm, tank_quality, sensor_id, temp)

    def battery_pct(self):
        mvolts = int(self.battery_volts * 1000)
        batt_pct = 0
        if mvolts >= 3000:
            batt_pct = 100
        elif mvolts > 2900:
            batt_pct = 100 - ((3000 - mvolts) * 58) / 100
        elif mvolts > 2740:
            batt_pct = 42 - ((2900 - mvolts) * 24) / 160
        elif mvolts > 2440:
            batt_pct = 18 - ((2740 - mvolts) * 12) / 300
        elif mvolts > 2100:
            batt_pct = 6 - ((2440 - mvolts) * 6) / 340
        return int(batt_pct)

    def to_sensor(self):
        return [(SensorType.BatteryPercent,
                 self.battery_pct().to_bytes(1, 'little')),
                (SensorType.Temperature,
                 (self.temperature*10).to_bytes(2, 'little', signed=True)),
                (SensorType.TankHeight,
                 self.tank_fill_mm.to_bytes(2, 'little')),
                (SensorType.TankConfidence,
                 self.tank_quality.to_bytes(1, 'little'))]
