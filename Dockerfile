# Use the official Python image from the DockerHub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose the port that Django's development server listens on
EXPOSE 8000


# Run the Django development server and apply migrations
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]