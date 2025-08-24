# Use an official, lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the package list into the container
COPY requirements.txt .

# Install all the packages from the list
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (main.py, .env) into the container
COPY . .

# Tell Docker that the container will listen on port 8000
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]