# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Prerequisites

1. Python 3
2. NPM
3. PIP
4. Docker
5. Docker Compose 

## Quick start

### Preparing Database with Docker

1. Clone the git repo: `git clone https://github.com/albertoivo/trivia-fullstacknd.git`
2. `cd trivia-fullstacknd`
3. `cd docker`
3. `docker-compose up`

### Backend

The `./backend` directory contains a Flask and SQLAlchemy server.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server.  

[View the README.md within ./frontend for more details.](./frontend/README.md)