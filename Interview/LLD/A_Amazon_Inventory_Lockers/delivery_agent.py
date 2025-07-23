# ================================================================
# File: delivery_agent.py
# Description:
#   Represents a Delivery Agent.
#   The agent brings a package near the system and scans its QR code
#   to retrieve product/item information, and then places the item into
#   an appropriate locker.
#
# SOLID:
# - SRP: Focused on delivery agent operations.
# - DIP: Uses abstractions from QRScanner and DeliverySystem.
# ================================================================

from qr_scanner import QRScanner

class DeliveryAgent:
    def __init__(self, name: str, system):
        self.name = name
        self.system = system  # DeliverySystem instance
        self.qr_scanner = QRScanner()

    def deliver_package(self, qr_code: str):
        # Step 1: Agent scans the QR code.
        scanned_code = self.qr_scanner.scan(qr_code)
        # Step 2: Retrieve item information using the system.
        item = self.system.scan_qr(scanned_code)
        print(f"Delivery Agent {self.name} retrieved {item}.")
        # The system has already onboarded the item (placed in a locker).
        # The agent may now proceed with further actions (if needed).

    def onboard_new_package(self, item):
        """
        When a new product arrives and is listed,
        the agent can onboard the item into the system.
        """
        self.system.onboard_item(item)