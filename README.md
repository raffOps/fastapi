# FastAPI Project

This is a project to learn FastAPI. It implements a simple CRUD using FastAPI, Pytest, Postgres, Alembic and Docker. The project follows the Test Driven Development (TDD) approach, which helps in building robust and maintainable code, facilitating refactoring and bug fixing.


# Environment Variables
The application uses the following DEV environment variables, used ONLY FOR LOCAL DEVELOPMENT, which are stored in the .env file:  
  - POSTGRES_USER: The username for the Postgres database.
  - POSTGRES_PASSWORD: The password for the Postgres database.
  - POSTGRES_DB: The name of the Postgres database.
  - DB_URL: The URL for the main database.
  - DB_URL_TEST: The URL for the test database.
  - DB_URL_TEST_MIGRATIONS: The URL for the test database during migrations.
  - TEST_MODE: A boolean indicating whether the application is in test mode.
  - SECRET_KEY: The secret key used for JWT authentication.
  - ALGORITHM: The algorithm used for JWT authentication.

## Setup

1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/)
2. Install [Poetry](https://python-poetry.org/docs/#installation)
3. Install the python dependencies
    ```bash
    poetry install
    ```
4. Install Postgres using Docker
    ```bash
    make build
    ```
5. Run the migrations
    ```bash
    make init migrate
    make migration MESSAGE='init'
    ```

## Running the Application

1. Run the app after the migrations
    ```bash
    make build
    ```
2. Test if the app is running. If ok will return true with status code 200
    ```bash
    curl http://localhost:8000/health-check
    ```

## API Documentation

You can access the API documentation at `http://localhost:8000/docs`.

## Testing

To run the tests, use the following command:

```bash
make test
```

## License
This project is open source and available under the MIT License.