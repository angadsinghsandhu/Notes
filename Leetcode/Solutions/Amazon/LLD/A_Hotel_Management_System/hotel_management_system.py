# ================================================================
# File: hotelmanagement/hotel_management_system.py
# Description:
#   Core class managing guests, rooms, and reservations.
#   - Implements booking, check-in, check-out, and cancellation operations.
#   - Uses a singleton pattern to ensure only one instance of the system exists.
#   - Uses locking to ensure thread-safety for concurrent operations.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 4. Determine Core Methods Based on Use Cases.
# 6. Implement Necessary Methods.
# 7. Exception Handling and Edge Cases.
# 9. Apply Design Patterns (Singleton, Dependency Injection via Payment).
# ================================================================

from threading import Lock
from typing import Dict, Optional
from guest import Guest
from datetime import date
from room import Room, RoomStatus
from reservation import Reservation
from reservation_status import ReservationStatus
from payment import Payment
import uuid

class HotelManagementSystem:
    _instance = None  # type: HotelManagementSystem
    guests: Dict[str, Guest]
    rooms: Dict[str, Room]
    reservations: Dict[str, Reservation]
    lock: Lock

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.guests = {}
            cls._instance.rooms = {}
            cls._instance.reservations = {}
            cls._instance.lock = Lock()
        return cls._instance

    def add_guest(self, guest: Guest):
        self.guests[guest.id] = guest

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        return self.guests.get(guest_id)

    def add_room(self, room: Room):
        self.rooms[room.id] = room

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def book_room(self, guest: Guest, room: Room, check_in_date: date, check_out_date: date) -> Optional[Reservation]:
        with self.lock:
            if room.status == RoomStatus.AVAILABLE:
                room.book()
                reservation_id = self._generate_reservation_id()
                reservation = Reservation(reservation_id, guest, room, check_in_date, check_out_date)
                self.reservations[reservation_id] = reservation
                return reservation
            return None

    def cancel_reservation(self, reservation_id: str):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation:
                reservation.cancel()
                del self.reservations[reservation_id]

    def check_in(self, reservation_id: str):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                reservation.room.check_in()
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def check_out(self, reservation_id: str, payment: Payment):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                room = reservation.room
                # Calculate amount based on room price and duration of stay.
                amount = room.price * (reservation.check_out_date - reservation.check_in_date).days
                if payment.process_payment(amount):
                    room.check_out()
                    del self.reservations[reservation_id]
                else:
                    raise ValueError("Payment failed.")
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def _generate_reservation_id(self) -> str:
        # Generate a unique reservation id using uuid.
        return f"RES{uuid.uuid4().hex[:8].upper()}"