# Employee Manager

This is a simple Employee Manager application built with Flask. It allows you to manage employees, track their attendance, and perform clock in/out operations.

## Features

- Add new employees
- Employee login
- Clock in/out functionality
- Admin panel to view employees and attendance records

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/employeemanager.git
    cd employeemanager
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: Main application file
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript)
- `models.py`: Database models
- `requirements.txt`: List of dependencies

## License

This project is licensed under the MIT License.