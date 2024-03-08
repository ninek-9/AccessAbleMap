Repository Overview
This repository contains the microservice for handling looking up places and reviews, part of the AccessAble Maps web application. The microservice is designed to manage information related to various places and user-generated reviews associated with these places.

Features
Places Management: Add, update, retrieve, and delete information about different places taken from the Google Maps API.
Reviews Management: Allow users to post reviews, fetch reviews for a place, and manage user reviews using a PostgreSQL Database.

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8 or higher
pip (Python package manager)
Virtualenv (optional, but recommended for creating isolated Python environments)


Setup
Clone the repository:
git clone https://your-repository-url.git
cd your-repository-directory


Create and activate a virtual environment (optional):

For Unix/macOS:
python3 -m venv venv
source venv/bin/activate

For Windows:
python -m venv venv
.\venv\Scripts\activate


Install the requirements:
pip install -r requirements.txt

Environment Variables:
Copy the .env.example file to create your own .env file. Adjust the variables to fit your local setup.

cp .env.example .env
Your .env file should include the following variables:

GOOGLE_API_KEY: your google api key.
SECRET_KEY: your secret key.
DB_NAME: The name of your database.
DB_USER: Your database username.
DB_PASSWORD: Your database password.
DB_HOST: Hostname for the database connection.
DB_PORT: Port number for the database connection.
Ensure to fill in the values corresponding to your development environment.

Running the Application
Execute the following command to run the application:
flask run
The microservice will start, and you can interact with it using the defined API endpoints through a client like Postman or a browser.


Contributing
Contributions to enhance the Places and Reviews Microservice are welcomed. Before contributing, please check out our contributing guidelines.