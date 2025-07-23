# ================================================================
# File: qr_scanner.py
# Description:
#   Simulates a QR code scanner.
#   In a real system, this would interface with hardware.
#
# SOLID:
# - SRP: Only responsible for simulating QR scanning.
# ================================================================

class QRScanner:
    def scan(self, qr_code: str) -> str:
        # In our simulation, the QR code is simply the item_id.
        print(f"Scanning QR code: {qr_code}")
        return qr_code