from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from flask import current_app as app
from app import db


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='ratings')
    movie = db.relationship('Movie', back_populates='ratings')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))  # Zwiększ długość tej kolumny
    is_admin = db.Column(db.Boolean, default=False)
    loyalty_points = db.Column(db.Integer, default=0)
    ratings = db.relationship('Rating', order_by=Rating.timestamp, back_populates='user')
    reservations = db.relationship('Reservation', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    director = db.Column(db.String(128))
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(64))
    description = db.Column(db.Text)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)
    ratings = db.relationship('Rating', order_by=Rating.timestamp, back_populates='movie')

    def average_rating(self):
        total_score = sum(rating.rating for rating in self.ratings)
        if len(self.ratings) > 0:
            return total_score / len(self.ratings)
        return 0

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    showtime = db.Column(db.DateTime, nullable=False)
    seats = db.relationship('Seat', backref='showtime', lazy=True)
    reservations = db.relationship('Reservation', back_populates='showtime')

    def create_seats_for_showtime(self):
        for row in range(1, 11):  # Assuming 10 rows
            for seat_number in range(1, 19):  # Assuming 18 seats per row
                seat = Seat(showtime_id=self.id, row=row, seat_number=seat_number, status='available')
                db.session.add(seat)
        db.session.commit()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    seats = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(32), default='active')
    user = db.relationship('User', back_populates='reservations')
    showtime = db.relationship('Showtime', back_populates='reservations')

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    row = db.Column(db.String(4), nullable=False)
    seat_number = db.Column(db.String(4), nullable=False)
    status = db.Column(db.String(16), default='available')

class LoyaltyPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, default=0)