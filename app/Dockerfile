# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV DB_HOST=localhost
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=todo_list

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the application with Gunicorn, binding to port 5000 and using 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
