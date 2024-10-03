# 🎬 Kino_Rezerwacje - Cinema Ticket Reservation System

## 📜 Project Description

**Kino_Rezerwacje** is a cinema ticket reservation system built in Python using Flask and SQLAlchemy. The application allows users to browse available movies, select showtimes, book tickets, and manage reservations. The primary goal is to streamline the process of reserving cinema tickets and provide a user-friendly interface for moviegoers.

### Key Features

- 📅 **Movie Schedule Viewing**: Users can view available movies and showtimes.
- 🪑 **Seat Selection**: Allows users to see the seating layout and select specific seats.
- 🎫 **Ticket Booking**: Facilitates booking of tickets and provides a confirmation for the same.
- 📊 **Reservation Management**: Enables users to view, modify, and delete their reservations.
- 🛠️ **Admin Panel** (Optional): If implemented, provides functionalities for managing movies, showtimes, and reservations.

## 🏗️ Installation and Setup

### Prerequisites
Make sure you have the following installed on your system:

- **Python 3.11** or newer
- **MySQL** or any other SQL-compatible database

### 1. Clone the Repository


git clone https://github.com/WronaAcc/Kino_rezerwacje
cd kino_rezerwacje


### 2. Set Up the Virtual Environment

#### Create a virtual environment
python -m venv venv

#### Activate the virtual environment
#### Windows:
venv\Scripts\activate
#### Linux/Mac:
source venv/bin/activate

### 3. Install Dependencies

#### Install all required libraries and dependencies listed in requirements.txt:

pip install -r requirements.txt

### 4. Configure the Database

- Create a new MySQL database for the application.
- Update the SQLALCHEMY_DATABASE_URI variable in the configuration file (config.py or app/__init__.py) with your database details:

  **SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/db_name'**

- Run the database migrations to set up the initial schema:

flask db init

flask db migrate

flask db upgrade

### 5. Running the Application

After the setup is complete, you can run the Flask development server:

flask run

**The application will be available at http://127.0.0.1:5000/.**

# 🚀 Usage

- Navigate to the home page to view the movie schedule.
- Select a movie and desired showtime.
- Choose your seats and proceed to book the tickets.
- View or manage your reservations in the user dashboard.

## 🗃️ Folder Structure

kino_rezerwacje/
```plaintext

├── app/                      # Main application package

│    ├── __init__.py          # Application factory and configuration

│    ├── models.py            # Database models

│    ├── routes.py            # Route handlers for Flask

│    ├── static/              # Static files (CSS, JavaScript, images)

│         └── templates/      # HTML templates for the web application

├── migrations/               # Database migration files

├── venv/                     # Virtual environment files

├── wsgi.py                   # WSGI entry point for the application

├── config.py                 # Application configuration file

└── requirements.txt          # Project dependencies
```
## ⚙️ Technologies Used

- Backend: Python, Flask, SQLAlchemy
- Database: MySQL
- Frontend: HTML, CSS, JavaScript (Flask Jinja templates)
- Other: Flask-Migrate, Flask-Login

## 👥 Contributors

**Feel free to contribute to this project by forking the repository and making a pull request with your changes.**

## 📝 License

**This project is licensed under the MIT License **
