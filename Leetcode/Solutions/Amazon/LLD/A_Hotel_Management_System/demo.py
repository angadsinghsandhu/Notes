# ================================================================
# File: hotelmanagement/hotel_management_system_demo.py
# Description:
#   Acts as the entry point for the Hotel Management System demo.
#   - Creates guests, rooms, and processes a room booking through check-in and check-out.
#   - Demonstrates system functionality and error handling.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from datetime import date
from hotel_management_system import HotelManagementSystem
from guest import Guest
from room import Room
from room_type import RoomType
from credit_card_payment import CreditCardPayment

class HotelManagementSystemDemo:
    @staticmethod
    def run():
        hotel_management_system = HotelManagementSystem()

        # Create guests
        guest1 = Guest("G001", "John Doe", "john@example.com", "1234567890")
        guest2 = Guest("G002", "Jane Smith", "jane@example.com", "9876543210")
        hotel_management_system.add_guest(guest1)
        hotel_management_system.add_guest(guest2)

        # Create rooms
        room1 = Room("R001", RoomType.SINGLE, 100.0)
        room2 = Room("R002", RoomType.DOUBLE, 200.0)
        hotel_management_system.add_room(room1)
        hotel_management_system.add_room(room2)

        # Book a room for guest1
        check_in_date = date.today()
        # For demo purposes, add 3 days to the check-in date.
        check_out_date = check_in_date.replace(day=check_in_date.day + 3)
        reservation1 = hotel_management_system.book_room(guest1, room1, check_in_date, check_out_date)
        if reservation1:
            print(f"Reservation created: {reservation1.id}")
        else:
            print("Room not available for booking.")

        # Check-in using the reservation id
        hotel_management_system.check_in(reservation1.id)
        print(f"Checked in: {reservation1.id}")

        # Check-out and process payment using a credit card
        payment = CreditCardPayment()
        hotel_management_system.check_out(reservation1.id, payment)
        print(f"Checked out: {reservation1.id}")

        # Optionally cancel a reservation (if needed)
        # hotel_management_system.cancel_reservation(reservation1.id)
        # print(f"Reservation cancelled: {reservation1.id}")

if __name__ == "__main__":
    HotelManagementSystemDemo.run()