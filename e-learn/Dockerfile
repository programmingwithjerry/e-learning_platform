# Use the official Python 3.12.3 image as the base image for the Docker container.
FROM python:3.12.3

# Set environment variables to configure Python's behavior.
# Prevent Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent directly to the terminal without buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container to /code.
WORKDIR /code

# Upgrade pip to the latest version to ensure compatibility with the packages being installed.
RUN pip install --upgrade pip

# Copy the requirements file into the container's working directory.
COPY requirements.txt .

# Install the Python dependencies listed in the requirements file.
RUN pip install -r requirements.txt

# Copy the entire Django project into the container's working directory.
COPY . .
