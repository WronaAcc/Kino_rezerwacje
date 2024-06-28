from app import create_app, db
from app.models import Seat, Reservation

# Utwórz aplikację i ustaw kontekst aplikacji
app = create_app()
app.app_context().push()

# Zapytaj o wszystkie anulowane rezerwacje
canceled_reservations = Reservation.query.filter_by(status='canceled').all()

# Zaktualizuj statusy miejsc dla wszystkich anulowanych rezerwacji
for reservation in canceled_reservations:
    seats = reservation.seats.split(',')
    for seat in seats:
        seat_obj = Seat.query.filter_by(showtime_id=reservation.showtime_id, seat_number=seat).first()
        if seat_obj:
            seat_obj.status = 'available'
            db.session.add(seat_obj)

db.session.commit()
print("Seat statuses for canceled reservations have been reset.")
