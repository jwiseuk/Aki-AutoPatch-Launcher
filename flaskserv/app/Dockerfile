# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ALLOWED_IPS=YOURIP1, YOURIP2

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the apache directory
RUN mkdir -p /var/www/html

# Set permissions for the apache folder
RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html

# Expose port 5000
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
