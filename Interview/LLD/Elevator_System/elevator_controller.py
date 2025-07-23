# ================================================================
# File: elevatorsystem/elevator_controller.py
# Description:
#   Manages multiple elevators and routes user requests to the optimal elevator.
#   - Finds the elevator that is closest to the source floor.
#   - Initiates elevator requests.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Concurrency: Delegates requests to running elevator threads.
# ================================================================

from threading import Thread
from elevator import Elevator
from request import Request

class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int):
        self.elevators = []
        # Initialize elevators and start each in its own thread.
        for i in range(num_elevators):
            elevator = Elevator(i + 1, capacity)
            self.elevators.append(elevator)
            Thread(target=elevator.run, daemon=True).start()

    def request_elevator(self, source_floor: int, destination_floor: int):
        # Find the optimal elevator to serve the request.
        optimal_elevator = self.find_optimal_elevator(source_floor)
        # Create a new request and add it to the chosen elevator.
        optimal_elevator.add_request(Request(source_floor, destination_floor))

    def find_optimal_elevator(self, source_floor: int) -> Elevator:
        optimal_elevator = None
        min_distance = float('inf')

        # Select the elevator closest to the source floor.
        for elevator in self.elevators:
            distance = abs(source_floor - elevator.current_floor)
            if distance < min_distance:
                min_distance = distance
                optimal_elevator = elevator

        return optimal_elevator