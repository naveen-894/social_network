## Requirements

- Python 3.9+
- Django 3.2+
- Django REST Framework
- Other dependencies as listed in `requirements.txt`

## Installation

1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply database migrations:
    ```bash
    python manage.py migrate # if new database
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the application at `http://127.0.0.1:8000/`.
