# ================================================================
# File: elevatorsystem/elevator.py
# Description:
#   Represents an individual elevator in the system.
#   - Maintains its current floor, direction, capacity and pending requests.
#   - Uses thread-safe mechanisms (Lock and Condition) to safely manage concurrent requests.
#   - Processes requests in FIFO order.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Concurrency (thread safety).
# ================================================================

import time
from threading import Lock, Condition
from request import Request
from direction import Direction

class Elevator:
    def __init__(self, id: int, capacity: int):
        self.id = id                              # Unique identifier for the elevator.
        self.capacity = capacity                  # Maximum number of concurrent requests.
        self.current_floor = 1                    # Starting floor.
        self.current_direction = Direction.UP     # Initial direction.
        self.requests = []                        # List to hold pending requests.
        self.lock = Lock()                        # Lock for thread safety.
        self.condition = Condition(self.lock)     # Condition variable for waiting on requests.

    def add_request(self, request: Request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(f"Elevator {self.id} added request: {request.source_floor} -> {request.destination_floor}")
                self.condition.notify_all()  # Notify waiting thread that a new request is available.
            else:
                print(f"Elevator {self.id} is at full capacity; cannot add new request.")

    def get_next_request(self) -> Request:
        with self.lock:
            while not self.requests:
                self.condition.wait()  # Wait until a request is available.
            return self.requests.pop(0)  # Retrieve the next request in FIFO order.

    def process_requests(self):
        # Continuously process available requests.
        while True:
            request = self.get_next_request()  # Wait until there's a request.
            self.process_request(request)

    def process_request(self, request: Request):
        start_floor = self.current_floor
        end_floor = request.destination_floor

        if start_floor < end_floor:
            self.current_direction = Direction.UP
            # Move up one floor at a time.
            for floor in range(start_floor, end_floor + 1):
                self.current_floor = floor
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulate time delay for moving between floors.
        elif start_floor > end_floor:
            self.current_direction = Direction.DOWN
            # Move down one floor at a time.
            for floor in range(start_floor, end_floor - 1, -1):
                self.current_floor = floor
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulate time delay for moving between floors.

    def run(self):
        # Entry point for the elevator thread.
        self.process_requests()