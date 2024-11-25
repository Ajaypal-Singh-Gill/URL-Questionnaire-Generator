FROM --platform=linux/amd64 python:3.8-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn
RUN pip install "jinja2<3.1"
RUN pip install psutil
RUN pip install tld

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5001

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
