from typing import List
from enum import Enum
from dataclasses import dataclass

# Define the enumeration for DispenserOptions
class DispenserOptions(Enum):
    OPTIMAL = 0
    PARTIAL = 1
    BLOCKAGE = 2

# Define the enumeration for LightStatus
class LightStatus(Enum):
    GOOD = 0
    BAD = 1

# Define the enumeration for SensorStatus
class SensorStatus(Enum):
    GOOD = 0
    BAD = 1

# Define the data class for Health
@dataclass
class HealthMessage:
    seq_no: int
    ts: float
    name: str
    data: List[int]
    dispenser: DispenserOptions
    icemaker: int
    lightbulb: LightStatus
    fridge_temp: int
    freezer_temp: int
    sensor_status: SensorStatus
    humidity: float
    door_openings: int
