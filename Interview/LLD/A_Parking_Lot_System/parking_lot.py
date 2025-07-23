# ================================================================
# File: parkinglot/parking_lot.py
# Description:
#   The central class representing the Parking Lot.
#   - Manages multiple levels.
#   - Uses the Singleton pattern to ensure only one instance exists.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 9. Apply Design Patterns (Singleton Pattern).
# ================================================================

from typing import List
from level import Level
from vehicle import Vehicle

class ParkingLot:
    _instance = None

    def __init__(self):
        if ParkingLot._instance is not None:
            return ParkingLot._instance
        else:
            ParkingLot._instance = self
            self.levels: List[Level] = []

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            ParkingLot()
        return ParkingLot._instance

    def add_level(self, level: Level) -> None:
        # Step 4: Method to add a level.
        self.levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        # Step 4: Iterate through levels to park a vehicle.
        for level in self.levels:
            if level.park_vehicle(vehicle):
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.unpark_vehicle(vehicle):
                return True
        return False

    def display_availability(self) -> None:
        for level in self.levels:
            level.display_availability()
