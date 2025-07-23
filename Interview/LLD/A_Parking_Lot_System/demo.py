# ================================================================
# File: parkinglot/parking_lot_demo.py
# Description:
#   Demonstrates the usage of the Parking Lot system.
#   - Acts as the client code to simulate parking and unparking vehicles.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from parking_lot import ParkingLot
from level import Level
from vehicle import Car, Motorcycle, Truck

class ParkingLotDemo:
    @staticmethod
    def run():
        # Step 1: Initialize the Parking Lot singleton.
        parking_lot = ParkingLot.get_instance()
        parking_lot.add_level(Level(1, 100))
        parking_lot.add_level(Level(2, 80))

        # Step 2: Create different vehicle types.
        car = Car("ABC123")
        truck = Truck("XYZ789")
        motorcycle = Motorcycle("M1234")

        # Step 6: Park vehicles.
        print("Parking vehicles...")
        parking_lot.park_vehicle(car)
        parking_lot.park_vehicle(truck)
        parking_lot.park_vehicle(motorcycle)

        # Step 7: Display current availability.
        print("\nAvailability after parking:")
        parking_lot.display_availability()

        # Unpark a vehicle.
        print("\nUnparking a motorcycle...")
        parking_lot.unpark_vehicle(motorcycle)

        # Display updated availability.
        print("\nAvailability after unparking:")
        parking_lot.display_availability()

if __name__ == "__main__":
    ParkingLotDemo.run()
