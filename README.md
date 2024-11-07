# Hunter Algorithm API

## Overview

Hunter API is a Django-based RESTful API that allows users to manage aesthetic procedures, hit the recommendation endpoint and receive personalized procedures back. 
This project is designed with flexibility, scalability, and real-world application in mind, offering advanced recommendation logic and user authentication.

## Features

- **User Authentication**: Token-based authentication for secure access using JWT.
- **CRUD Operations**: Create, read, update, and delete procedures with ease.
- **Personalized Recommendations**: Recommends procedures based on user favorites using a combination of cosine similarity, cost normalization, and complaint-based scoring.
- **Detailed API Documentation**: Integrated Swagger UI for easy exploration of the API.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (for production), SQLite (for development)
- **Machine Learning**: Scikit-Learn for similarity calculations
- **API Documentation**: Swagger (using `drf-yasg`)
- **Hosting**: Suitable for Heroku, AWS, or other cloud platforms

## Prerequisites

- Python 3.12 or above
- `pip` for package management
- A virtual environment (`venv`) setup
