# Full Stack Trivia
**Note:** Most of the contents in this project are based on Udacity's Full Stack Nanodegree Program, if you aim to know more about APIs considering enrolling in it.
## Requirements
Previously installed SQL database.
## Table of contents
* [Introduction](#introduction)
* [A. Backend](#a-backend)
    + [A.1. Installing Dependencies](#a1-installing-dependencies)
    + [A.2. Database Setup](#a2-database-setup)
    + [A.3. Running the server](#a3-running-the-server)
    + [A.4. API Documentation](#a4-api-documentation)
    + [A.5. Testing](#a5-testing)
* [B. Frontend](#b-frontend)
    + [B.1. Frontend Setup](#b1-frontend-setup)
    + [B.2  Running the Frontend in dev mode](#b2--running-the-frontend-in-dev-mode)

## Introduction
The following app is intended to work as a Trivia, so that players may test their knowledge in different areas. It is capable of:
1) Displaying questions - both all questions and by category. 
2) Adding and deleting questions.
3) Searching for questions based on a text query string.
4) Play the quiz game, randomizing either all questions or within a specific category. 

## A. Backend

The [/backend](./backend) directory contains a complete Flask and SQLAlchemy server. 


### A.1. Installing Dependencies

#### Python 3.7

This project is intended to work with Python 3.7. Follow instructions to install python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the [/backend](./backend) directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM that will be used to handle the database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### A.2. Database Setup
With Postgres, or any other RDBMS running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia_test
psql trivia < trivia.psql
```
Alternatively in Windows PS:
```shell
createdb -U postgres trivia_test
psql -U postgres -d trivia -f .\trivia.psql
```

### A.3. Running the server

From within the [/backend](./backend) directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Alternatively in Windows PS:
```terminal
$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### A.4. API Documentation

#### GET `/categories` 
Fetches a dictionary of all available categories.
- **Request arguments:** None 
- **Example response:**
```json
{
    "categories": {
        "0": "Science",
        "1": "Art",
        "2": "Geography",
        "3": "History",
        "4": "Entertainment",
        "5": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```

#### GET `/questions?page=<page_number>` 
Fetches a paginated dictionary of questions of all available categories.
- **Request arguments:**
  - (optional) page:int
- **Example response:**
```json
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 4,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        {
            "answer": "Agra",
            "category": 2,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 30
}
```

#### DELETE `/questions/<question_id>` 
Delete an existing question from the repository of available questions.
- **Request arguments:**
  - question_id:int
- **Example response:**
```json
{
    "deleted": "10",
    "success": true
}
```

#### POST `/questions` 
Add a new question to the repository of available questions.
- **Request body:** JSON
  - question:string 
  - answer:string 
  - difficulty:int
  - category:int
- **Example request:**
```json
{
    "question": "Howdy?",
    "answer": "How?",
    "difficulty": 1,
    "category": 1
}
```  
- **Example response:**
```json
{
    "created": 37,
    "success": true
}
```

#### POST `/questions/search` 
Fetches all questions where a substring matches the search term (not case-sensitive).
- **Request body:** JSON
  - searchTerm:string 
- **Example request:**
```json
{
    "searchTerm": "Giaconda"
}
```  
- **Example response:**
```json
{
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": 1,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
```

#### GET `/categories/<int:category_id>/questions`
Fetches a dictionary of questions for the specified category.
- **Request arguments:**
  - category_id:int
- **Example response:**
```json
{
    "currentCategory": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 1,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 1,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 1,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 1,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "totalQuestions": 4
}
```

#### POST `/quizzes`
Fetches one random question within a specified category. Previously asked questions are not asked again. 
- **Request body:** JSON
  - previous_questions: arr
  - quiz_category:
    - id:int 
    - type:string
- **Example request:**
```json
{
    "previous_questions": [1, 2, 3],
    "quiz_category": {"id": "1","type":"Art"}
}
```
- **Example response:**
```json
{
    "currentCategory": "1",
    "question": {
        "answer": "One",
        "category": 1,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
}
```

### A.5. Testing
To run the tests, run
```
dropdb -U postgres trivia_test
createdb -U postgres trivia_test
psql -U postgres trivia_test < .\trivia.psql
python test_flaskr.py
```

## B. Frontend

The [/frontend](./frontend) directory contains a complete React frontend to consume the data from the Flask server. 

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended to get the backend running first.
### B.1. Frontend Setup


#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```


### B.2  Running the Frontend in dev mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```
