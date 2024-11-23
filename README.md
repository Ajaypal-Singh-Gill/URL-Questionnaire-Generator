# URL-Questionnaire-Generator

A tool that takes a website URL as input, scrapes its content and generates a dynamic questionnaire to classify users based on their interests or industry. This application is built with a React/Redux frontend and a Python/Flask backend.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#Screenshots)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Live Demo](#live-demo)

## Technologies Used

- **Frontend**: React, Redux
- **Backend**: Python, Flask, BeautifulSoup and Requests (for scraping), OpenAI (for question generation)
- **Database**: PostgreSQL (for storing questions)
- **Caching**: Redis (for caching repeated URL submissions)
- **Async Processing**: Celery (for task queuing)
- **Containerization**: Docker (for consistent deployment environments)

## Features

- **Dynamic Question Generation**: Uses scraped website content to generate relevant questions.
- **Progress Tracking**: Displays a progress bar as users complete questions.
- **Responsive Design**: Designed for desktop and mobile with flexible styling.
- **Task Queuing**: Web scraping and question generation tasks are queued using Celery for efficient processing.
- **URL Caching**: Redis ensures repeated URL submissions are cached to prevent redundant scraping.
- **Dockerized Deployment**: Easily set up and deploy the application in consistent environments using Docker.
- **Public Accessibility**: Host the project infra(Frontend, Backend, Redis, Postgresql) on render.

## Getting Started

### Prerequisites

- **Node.js** and **npm** for the frontend.
- **Python 3.8+** and **pip** for the backend.
- **Redis** for caching.
- **Docker** for containerized deployment.

### Installation

#### Backend

Navigate to the backend directory:

```bash
cd backend
```

Option 1: Run without docker

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
```

Option 2: Run with Docker

Ensure Docker is installed and running on your machine. Build the Docker image:

```bash
docker build -t backend-image .
```

Run the Docker container:

```bash
docker run -p 5001:5001 backend-image
```

#### Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the React application:

```bash
npm start
```

The app should be running with:

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend**: [http://localhost:5001](http://localhost:5001)

## Usage

1. Open the app in the browser.
2. Enter a website URL to start the questionnaire generation process.
3. Answer the generated questions.

## Screenshot

<img width="1435" alt="image" src="https://github.com/user-attachments/assets/ae547e95-cc07-44e0-b633-13d220b2b12f">

<img width="891" alt="image" src="https://github.com/user-attachments/assets/b21713f1-3d4e-4297-9b92-156fdb7df892">


## Project Structure

## API Documentation

The backend provides RESTful API endpoints for interaction:

### POST `/generate-question`

Accepts a URL, scrapes content, and generates a set of questions based on the content.

#### Request Body:

```json
{
  "url": "https://example.com",
  "save_to_db": true
}
```

#### Response:

```json
{
  "questions": [
    {
      "question": "What is your main purpose for visiting?",
      "options": ["Learning", "Shopping", "Research"]
    }
  ]
}
```

## Contributing

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Added new feature"
   ```

4. Push to your fork and submit a pull request.

## Live Demo

You can access the live version of the application here:

Frontend: https://url-questionnaire-generator-1.onrender.com/
