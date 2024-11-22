# Use a slim base image to reduce size
FROM --platform=linux/amd64 python:3.8-slim

# Set environment variables to improve performance
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install only the necessary system dependencies and clean up immediately
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn
RUN pip install "jinja2<3.1"


# Copy only requirements first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Install Python dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the application port
EXPOSE 5001

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
