# ================================================================
# File: parkinglot/level.py
# Description:
#   Represents a level or floor in the parking lot.
#   - Manages a collection of ParkingSpot objects.
#   - Handles the parking/unparking of vehicles on that level.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# ================================================================

from typing import List
from parking_spot import ParkingSpot
from vehicle import Vehicle

class Level:
    def __init__(self, floor: int, num_spots: int):
        # Step 3: Initialize attributes.
        self.floor = floor
        self.parking_spots: List[ParkingSpot] = [ParkingSpot(i) for i in range(num_spots)]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        # Step 4: Iterate over parking spots to park a vehicle.
        for spot in self.parking_spots:
            if spot.is_available() and spot.get_vehicle_type() == vehicle.get_type():
                spot.park_vehicle(vehicle)
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                return True
        return False

    def display_availability(self) -> None:
        # Step 7: Display the status of each spot.
        print(f"Level {self.floor} Availability:")
        for spot in self.parking_spots:
            status = 'Available' if spot.is_available() else 'Occupied'
            print(f"Spot {spot.get_spot_number()}: {status}")
