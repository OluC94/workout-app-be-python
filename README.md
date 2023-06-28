# Workout App - Backend

This backend appliaction was developed using Django rest framework with full TDD to allow the user to create their own exercise routines

The user can perform CRUD operations for:

- exercises
- workout days, which can be populated using existing exercises
- full routines, which can be populated using existing workout days

The backend is hosted at `<link when ready>`

## How to run this application locally

### Minimum version requirements

- Python: 3
- Django: 4
- Django Rest Framework: 3
- Database: sqlite3

### Instructions

1. Create a fork of this repository and then create a clone using the command `git clone <repo-url>`
2. Actiate the virtual environment using the command `source .venv/bin/activate`
3. Run the command `pip install -r requirements.txt` to install all of the required dependencies
4. In the root directory run the command `WorkoutAPI/manage.py runserver` to start the server on the local host (port 8000)

To run the tests, cd into `WorkoutAPI` and run the command `python manage.py test ExercisesApp` while the venv is active
