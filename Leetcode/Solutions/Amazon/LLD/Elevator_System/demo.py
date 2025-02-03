# ================================================================
# File: elevatorsystem/elevator_system_demo.py
# Description:
#   Demonstrates the usage of the Elevator System.
#   - Creates an instance of ElevatorController.
#   - Simulates multiple elevator requests.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

import time
from elevator_controller import ElevatorController

class ElevatorSystemDemo:
    @staticmethod
    def run():
        # Create an ElevatorController with 3 elevators and each with a capacity of 5 requests.
        controller = ElevatorController(3, 5)
        time.sleep(3)  # Allow some time for elevators to initialize.

        # Simulate elevator requests.
        controller.request_elevator(10, 12)
        time.sleep(3)
        controller.request_elevator(1, 7)
        time.sleep(3)
        controller.request_elevator(2, 5)
        time.sleep(3)
        controller.request_elevator(1, 9)
        
        # Keep the main thread alive to allow elevator threads to process requests.
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Elevator system stopped.")

if __name__ == "__main__":
    ElevatorSystemDemo.run()