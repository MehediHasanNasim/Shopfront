# Shopfront

## About the Project
This project is a fully functional backend API built with Django and Django Rest Framework (DRF). It offers secure, scalable endpoints for web applications, leveraging DRF's Generic API Views for efficiency. The API includes features like filtering, searching, ordering, pagination, and nested routes, ensuring robust data management and ease of maintenance.

## Tools and Technologies
- **Languages:** Python
- **Framework:** Django Rest framework (DRF)
- **Database:** PostgreSQL

## Setup Instructions to Run
Follow these steps to set up the project on your local machine.

### Prerequisites (Install)
- Python 3.x
- Django 3.x
- A SQL database (e.g., SQLite, PostgreSQL)
- Git

### Run
1. **Clone the repository:**
    ```sh
    git clone https://github.com/MehediHasanNasim/Shopfront.git
    cd Shopfront
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate # (terminal)  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

6. **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/` #localhost.

7. **Api end points:**
   Products: `http://127.0.0.1:8000/store/products`
   collections: `http://127.0.0.1:8000/store/collections`
   carts: `http://127.0.0.1:8000/store/carts`


## Configuration
### Database setup
To set up built-in db.sqlite3, configure the database settings in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```


