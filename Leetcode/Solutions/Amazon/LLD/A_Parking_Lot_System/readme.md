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