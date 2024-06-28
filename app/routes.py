from flask import render_template, flash, redirect, url_for, request, current_app as app, current_app
from flask_login import current_user, login_user, logout_user, login_required
from . import db
from .models import User, Movie, Showtime, Reservation, Seat
from .forms import LoginForm, RegistrationForm, MovieForm, ShowtimeForm, ReservationForm, ResetPasswordRequestForm, \
    ResetPasswordForm, ChangePasswordForm, EditProfileForm, AdminUpdateSeatForm
from .email import send_reset_password_email, send_cancellation_email, send_reservation_confirmation_email
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
import random
import string
import logging


def generate_random_password(length=12):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def generate_ticket_code(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(title=form.title.data, director=form.director.data,
                      release_date=form.release_date.data, genre=form.genre.data,
                      description=form.description.data)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!')
        return redirect(url_for('index'))
    return render_template('add_movie.html', form=form)


@app.route('/add_showtime', methods=['GET', 'POST'])
@login_required
def add_showtime():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    form = ShowtimeForm()
    if form.validate_on_submit():
        showtime = Showtime(movie_id=form.movie_id.data, showtime=form.showtime.data)
        db.session.add(showtime)
        db.session.commit()

        # Tworzenie miejsc dla nowego seansu
        showtime.create_seats_for_showtime()

        flash('Showtime added successfully!')
        return redirect(url_for('index'))
    return render_template('add_showtime.html', form=form)

@app.route('/make_reservation', methods=['GET', 'POST'])
@login_required
def make_reservation():
    form = ReservationForm()
    try:
        if form.validate_on_submit():
            showtime = Showtime.query.get(form.showtime_id.data)
            if showtime.showtime <= datetime.utcnow():
                flash('You cannot make a reservation for a showtime that has already occurred.')
                return redirect(url_for('make_reservation'))

            # Sprawdzenie dostępności miejsc
            requested_seats = request.form.get('selected_seats', '').split(',')
            reserved_seats = [f"{seat.row}-{seat.seat_number}" for seat in Seat.query.filter_by(showtime_id=showtime.id, status='reserved').all()]

            for seat in requested_seats:
                if seat in reserved_seats:
                    flash(f'Seat {seat} is already reserved.')
                    return redirect(url_for('make_reservation'))

            reservation = Reservation(user_id=current_user.id, showtime_id=form.showtime_id.data, seats=','.join(requested_seats))
            db.session.add(reservation)

            # Aktualizacja statusu miejsc
            for seat in requested_seats:
                row, seat_num = seat.split('-')
                seat_obj = Seat.query.filter_by(showtime_id=showtime.id, row=row, seat_number=seat_num).first()
                if seat_obj:
                    seat_obj.status = 'reserved'
                else:
                    seat_obj = Seat(showtime_id=showtime.id, row=row, seat_number=seat_num, status='reserved')
                    db.session.add(seat_obj)

            db.session.commit()
            ticket_code = generate_ticket_code()
            send_reservation_confirmation_email(current_user, reservation, ticket_code)
            flash('Reservation made successfully! Check your email for the confirmation and ticket code.')
            return redirect(url_for('index'))
    except Exception as e:
        current_app.logger.error(f"Error making reservation: {e}")
        flash('An error occurred while making the reservation.')

    showtime_id = form.showtime_id.data
    seats = Seat.query.filter_by(showtime_id=showtime_id).all()
    seating_chart = []
    for row in range(1, 11):
        seat_row = []
        for col in range(1, 19):
            seat_number = f"{row}-{col}"
            seat = next((seat for seat in seats if seat.row == str(row) and seat.seat_number == str(col)), None)
            seat_status = 'available' if seat is None else seat.status
            seat_row.append({'number': seat_number, 'status': seat_status})
        seating_chart.append(seat_row)

    return render_template('make_reservation.html', form=form, seating_chart=seating_chart)

@app.route('/admin_update_seat/<int:showtime_id>', methods=['GET', 'POST'])
@login_required
def admin_update_seat(showtime_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))

    form = AdminUpdateSeatForm()
    showtime = Showtime.query.get_or_404(showtime_id)

    if form.validate_on_submit():
        seat_number = form.seat_number.data
        status = form.status.data
        row, seat_num = seat_number.split('-')
        seat = Seat.query.filter_by(showtime_id=showtime.id, row=row, seat_number=seat_num).first()
        if seat:
            seat.status = status
        else:
            seat = Seat(showtime_id=showtime.id, row=row, seat_number=seat_num, status=status)
            db.session.add(seat)
        db.session.commit()
        flash('Seat status updated successfully.')
        return redirect(url_for('admin_update_seat', showtime_id=showtime_id))

    seats = Seat.query.filter_by(showtime_id=showtime.id).all()
    seating_chart = []
    for row in range(1, 11):
        seat_row = []
        for col in range(1, 19):
            seat_number = f"{row}-{col}"
            seat = next((seat for seat in seats if seat.row == str(row) and seat.seat_number == str(col)), None)
            seat_status = 'available' if seat is None else seat.status
            seat_row.append({'number': seat_number, 'status': seat_status})
        seating_chart.append(seat_row)

    return render_template('admin_update_seat.html', form=form, seating_chart=seating_chart, showtime_id=showtime.id)


@app.route('/movies')
def movies():
    all_movies = Movie.query.all()
    return render_template('movies.html', movies=all_movies)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            new_password = generate_random_password()
            user.set_password(new_password)
            db.session.commit()
            send_reset_password_email(user, new_password)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('new_password.html', form=form)


class DummyForm(FlaskForm):
    pass


@app.route('/profile')
@login_required
def profile():
    try:
        now = datetime.utcnow()
        active_reservations = Reservation.query.filter_by(user_id=current_user.id, status='active').filter(
            Reservation.showtime.has(Showtime.showtime > now)).all()
        past_reservations = Reservation.query.filter_by(user_id=current_user.id, status='active').filter(
            Reservation.showtime.has(Showtime.showtime <= now)).all()
        canceled_reservations = Reservation.query.filter_by(user_id=current_user.id, status='canceled').all()

        # Logowanie do konsoli dla diagnostyki
        current_app.logger.info(f"Active reservations: {active_reservations}")
        current_app.logger.info(f"Past reservations: {past_reservations}")
        current_app.logger.info(f"Canceled reservations: {canceled_reservations}")

        return render_template('profile.html', active_reservations=active_reservations,
                               past_reservations=past_reservations, canceled_reservations=canceled_reservations,
                               form=DummyForm())
    except Exception as e:
        # Logowanie błędu do konsoli
        current_app.logger.error(f"Error in profile view: {e}")
        flash('An error occurred while loading the profile.')
        return redirect(url_for('index'))


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        if reservation.user_id != current_user.id:
            flash('You cannot cancel this reservation.')
            return redirect(url_for('profile'))
        if reservation.showtime.showtime <= datetime.utcnow() + timedelta(minutes=45):
            flash('You can only cancel reservations up to 45 minutes before the showtime.')
            return redirect(url_for('profile'))

        # Update seat status
        seats = reservation.seats.split(',')
        for seat in seats:
            row, seat_num = seat.split('-')
            seat_obj = Seat.query.filter_by(showtime_id=reservation.showtime_id, row=row, seat_number=seat_num).first()
            if seat_obj:
                seat_obj.status = 'available'
                db.session.add(seat_obj)

        reservation.status = 'canceled'
        db.session.commit()
        send_cancellation_email(current_user, reservation)
        flash('Reservation canceled successfully.')
    except Exception as e:
        current_app.logger.error(f"Error canceling reservation: {e}")
        flash('An error occurred while canceling the reservation.')
    return redirect(url_for('profile'))


@app.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(movie_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        form.populate_obj(movie)
        db.session.commit()
        flash('Movie updated successfully!')
        return redirect(url_for('movies'))
    return render_template('add_movie.html', form=form)


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!')
    return redirect(url_for('movies'))


@app.route('/update_showtime/<int:showtime_id>', methods=['GET', 'POST'])
@login_required
def update_showtime(showtime_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    showtime = Showtime.query.get_or_404(showtime_id)
    form = ShowtimeForm(obj=showtime)
    if form.validate_on_submit():
        form.populate_obj(showtime)
        db.session.commit()
        flash('Showtime updated successfully!')
        return redirect(url_for('index'))
    return render_template('add_showtime.html', form=form)


@app.route('/delete_showtime/<int:showtime_id>', methods=['POST'])
@login_required
def delete_showtime(showtime_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    showtime = Showtime.query.get_or_404(showtime_id)
    db.session.delete(showtime)
    db.session.commit()
    flash('Showtime deleted successfully!')
    return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Invalid old password.')
            return redirect(url_for('change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('profile'))
    return render_template('change_password.html', form=form)