FROM python:3.11-bullseye

# Set the working directory in the container
WORKDIR /galini-plus

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --retries 5 -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port that the app runs on
EXPOSE 8000

# Run migrations, collect static files, and start the server
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn seechat.wsgi:application --bind 0.0.0.0:8000"]