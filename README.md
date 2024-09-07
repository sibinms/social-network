# Social Network Project

This is a social networking application built with Django and Django REST Framework. The project includes core features like user registration, searching for users, sending/accepting/rejecting friend requests, and listing friends.

## Features
- User registration and authentication
- Search users by email or name
- Send, accept, or reject friend requests
- List friends and pending friend requests
- Rate limiting for sending friend requests (3 requests per minute)

## API Documentation
The API documentation is available at:
[Swagger API Documentation](http://0.0.0.0:8000/swagger/#/)

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sibinms/social-network.git
    cd social-network
    ```

2. **Build and run the project using Docker**:
    ```bash
    docker-compose up -d
    ```

    This command will build the Docker containers, apply migrations automatically, and start the project.

3. **Create a superuser**:
    To create a superuser, use the following command:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

4. **Access the application**:
    The app will be available at `http://0.0.0.0:8000/`.

