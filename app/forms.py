from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from .models import User, Showtime, Movie
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

class ShowtimeForm(FlaskForm):
    movie_id = SelectField('Movie', coerce=int, validators=[DataRequired()])
    showtime = DateTimeField('Showtime', validators=[DataRequired()])
    submit = SubmitField('Add Showtime')

    def __init__(self, *args, **kwargs):
        super(ShowtimeForm, self).__init__(*args, **kwargs)
        self.movie_id.choices = [(movie.id, movie.title) for movie in Movie.query.all()]

class ReservationForm(FlaskForm):
    showtime_id = SelectField('Showtime', coerce=int, validators=[DataRequired()])
    selected_seats = HiddenField('Selected Seats', validators=[DataRequired()])
    submit = SubmitField('Make Reservation')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.showtime_id.choices = [(showtime.id, f"{showtime.movie.title} - {showtime.showtime}") for showtime in Showtime.query.filter(Showtime.showtime > datetime.utcnow()).all()]

class AdminUpdateSeatForm(FlaskForm):
    seat_number = StringField('Seat Number', validators=[DataRequired()])
    status = SelectField('Status', choices=[('available', 'Available'), ('reserved', 'Reserved'), ('excluded', 'Excluded')], validators=[DataRequired()])
    submit = SubmitField('Update Seat')


class EmptyForm:
    pass