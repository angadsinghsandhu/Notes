# ================================================================
# File: parkinglot/vehicle.py
# Description:
#   Abstract base class for all vehicles.
#   - Defines the common interface and attributes for vehicles.
#   Represents a Truck in the parking lot system.
#   - Extends the abstract Vehicle class.
#   Represents a Motorcycle in the parking lot system.
#   - Inherits from the abstract Vehicle class.
#   Represents a Car in the parking lot system.
#   - Implements the Vehicle interface using inheritance.
#   - Follows the Single Responsibility Principle.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from abc import ABC
from vehicle_type import VehicleType

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

    def get_type(self) -> VehicleType:
        # Step 4: Provides a method to retrieve the vehicle type.
        return self.type

### Vehicle Subclasses ###

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        # Step 3: Set attributes for the Motorcycle instance.
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        # Step 3: Set attributes for the Car instance.
        super().__init__(license_plate, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        # Step 3: Set attributes for the Truck instance.
        super().__init__(license_plate, VehicleType.TRUCK)

