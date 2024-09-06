FROM ghcr.io/osgeo/gdal:ubuntu-small-3.9.2

# Set the working directory in the container
WORKDIR /app

# Update package list and install system dependencies, Python, and pip
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    sudo \
    --fix-missing

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment and install Python packages
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["/app/venv/bin/python", "app.py"]
