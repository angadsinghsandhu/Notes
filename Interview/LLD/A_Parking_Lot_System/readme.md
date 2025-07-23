# Parking Lot System

## Problem Statement

Design a parking lot system where you have to park multiple vehicles. This parking lot has multiple levels. Each level has multiple rows of spots. Each row has a specific number of spots such as motorcycles, cars, and large cars. You have to implement the following functions:

1. `ParkVehicle(vehicle: Vehicle): bool`: This function is called when a vehicle enters the parking lot. The vehicle can be a motorcycle, car, or large car. The function should return true if the vehicle can be parked in the parking lot. Else, it should return false.

2. `RemoveVehicle(vehicle: Vehicle): bool`: This function is called when a vehicle exits the parking lot. The function should return true if the vehicle was parked in the parking lot. Else, it should return false.

3. `GetParkingSpot(vehicle: Vehicle): ParkingSpot`: This function is called when a vehicle enters the parking lot. The function should return the parking spot where the vehicle is parked. If the vehicle is not parked in the parking lot, return null.

## Directory Structure

```text
parkinglot/
├── level.py
├── parking_lot.py
├── parking_lot_demo.py
├── parking_spot.py
├── vehicle.py
└── vehicle_type.py
```

## Design

The parking lot system is designed using the following classes:

1. `VehicleType`: This class is an enum that defines the type of vehicle. The vehicle can be a motorcycle, car, or large car.

2. `Vehicle`: This class represents a vehicle. It has the following attributes:
    - `license_plate`: The license plate of the vehicle.
    - `vehicle_type`: The type of the vehicle.

3. `ParkingSpot`: This class represents a parking spot. It has the following attributes:

    - `spot_number`: The spot number of the parking spot.
    - `level`: The level of the parking spot.
    - `row`: The row of the parking spot.
    - `vehicle`: The vehicle parked in the parking spot.

4. `Level`: This class represents a level in the parking lot. It has the following attributes:

    - `level_number`: The level number.
    - `rows`: The rows of parking spots in the level.

5. `ParkingLot`: This class represents the parking lot. It has the following attributes:

    - `levels`: The levels in the parking lot.

The parking lot system has the following functions:
