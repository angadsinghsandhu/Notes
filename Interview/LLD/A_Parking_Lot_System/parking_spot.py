# ================================================================
# File: parkinglot/parking_spot.py
# Description:
#   Represents an individual parking spot.
#   - Manages the state of a parking spot (occupied or available).
#   - Determines if a vehicle can be parked in this spot.
#
# Steps Covered:
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling (throws error if spot is invalid).
# ================================================================

from vehicle_type import VehicleType
from vehicle import Vehicle

class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type: VehicleType = VehicleType.CAR):
        self.spot_number = spot_number
        # For simplicity, we assign the default spot type as CAR. 
        # In a more robust design, the spot type might be configurable.
        self.vehicle_type = vehicle_type 
        self.parked_vehicle = None

    def is_available(self) -> bool:
        return self.parked_vehicle is None

    def park_vehicle(self, vehicle: Vehicle) -> None:
        # Step 7: Validate before parking.
        if self.is_available() and vehicle.get_type() == self.vehicle_type:
            self.parked_vehicle = vehicle
        else:
            raise ValueError("Invalid vehicle type or spot already occupied.")

    def unpark_vehicle(self) -> None:
        self.parked_vehicle = None

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type

    def get_parked_vehicle(self) -> Vehicle:
        return self.parked_vehicle

    def get_spot_number(self) -> int:
        return self.spot_number
