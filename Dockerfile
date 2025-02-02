# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the dependencies from requirements.txt (make sure you have one)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
# CMD ["uvicorn", "frontend_app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "testcode.py"]