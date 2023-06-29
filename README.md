# Workout App - Backend

This backend application was developed using Django rest framework with full TDD to allow the user to create their own exercise routines.

The MVP allows the user to perform CRUD operations for:

- exercises
- workout days, which can be populated using existing exercises
- full routines, which can be populated using existing workout days

The backend is hosted at https://oluc94.pythonanywhere.com/

## How to run this application locally

The minimum version of Python required is 3.10

1. Create a fork of this repository and then create a clone using the command `git clone <repo-url>`
2. Create a virtual environment using the command `python3 -m venv .venv`, than activate it by running `source .venv/bin/activate`
3. Run the command `pip install -r requirements.txt` to install all of the required dependencies
4. A SECRET_KEY is required in the settings.py file:

   - First, comment out line 3 of 15 of settings.py

   ```python
   from my_secrets import settings_secret_key
   ```

   - Then go to this link and follow the instructions to generate a secret key: https://codinggear.blog/django-generate-secret-key/
   - Go to line 25 in settings.py and replace the `settings_secret_key` variable with a string containig the generated secret key

5. Once the secret key has been added to settings.py, run the command `WorkoutAPI/manage.py runserver` in the root directory to start the server on the local host (port 8000)

To run the tests, cd into `WorkoutAPI` and run the command `python manage.py test ExercisesApp` while the venv is active
