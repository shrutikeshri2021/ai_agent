# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the frontend directory contents into the container at /app/frontend
COPY frontend/ /app/frontend/

# Install Streamlit and other dependencies
# Note: We might need requests here if it's not in a requirements file for frontend
RUN pip install streamlit requests

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
WORKDIR /app/frontend
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
