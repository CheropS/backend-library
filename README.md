# backend-library
Flask Api endpoints and tests for the library project.

## Project Objectives
* Your project should have a functioning authentication system
* Your project should contain migration files for the different model structure
* Your project must have a user model
* Your project should produce an Api
* Your project should allow users to register
* Your project should allow users to login 
* Your project should allow users to create reviews.

## Live site 
[books-api](https://backend-lib.herokuapp.com/)


## Setup Instructions / Installation

### Getting Started

### Prerequisites

- Python and pip (I am currently using 3.9.7) Any version above 3.7 should work.
* Git installed on your machine
* Code editor/ IDE.

### Installation and Running the App

1. Clone the GitHub repository

    ```shell
    git clone https://github.com/CheropS/backend-library
    ```

2. Change into the folder

    ```shell
   cd backend-library
    ```

3. Create a virtual environment

   ```shell
      python3 -m venv venv 
   ```

    * Activate the virtual environment

   ```shell
   source ./bin/activate
   ```

* If you are using [pyenv](https://github.com/pyenv/pyenv):

  3a. Create a virtualenv

   ```
       pyenv virtualenv backend-library
   ```

  3b. Activate the virtualenv

   ```
   pyenv activate backend-library
   ```

4. Create a `.env` file and add your credentials

   ```
   touch .env 
   ```

   OR Copy the included example

    ```
    cp .env-example .env 
    ```

5. Add your credentials to the `.env` file


6. Install the required dependencies

   ```shell
   pip install -r requirements.txt
   ```

7. Export `manage.py` as the default flask app in your environment
    ```shell
    export FLASK_APP=manage.py 
    ```
8. Make the shell script executable

    ```shell
   chmod a+x ./run.sh
    ```
9. Migrate and Update the database
    ```shell
   flask db migrate
   flask db upgrade
    ```
11. Run the app

     ```shell
    ./run.sh
     ```

    OR
    run with the [flask-cli](https://flask.palletsprojects.com/en/2.0.x/cli/)

     ```shell
    flask run
     ```

## Tests

* To run the tests:

    ```shell
  flask tests
    ```

## Technologies used

* Python-3.9.7
* Flask web framework
* Postgresql

## Author

[Ken Mwaura](https://github.com/KenMwaura1)

## Available API Endpoints

| Endpoint | Description |
| --- | --- |
| POST /api/v1/books | Adds a New Book
| PUT /api/v1/books/<string:bookId> | Edits Individual Book Info
| DELETE /api/v1/books/<string:bookId> | Deletes A Book
| GET /api/v1/books | Retrieves All Books
| GET /api/v1/books?q | Search All Books
| GET /api/v1/books/<string: bookId> | Get Book by id
| POST /api/v1/users/books/<string: bookId> | Review a book
| POST /api/v1/auth/register | Register a New User
| POST /api/v1/users | Gets all Users
| POST /api/v1/auth/login | Logs in a registered User
| POST /api/v1/auth/logout | Logs Out a Logged in

## API Endpoints Documentation
Find API endpoints documentation while the app is running on [localhost:5000](http://localhost:5000/)

## Testing API Endpoints

Use Postman and the provided documentation to test the API endpoints
