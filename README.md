# URL-Questionnaire-Generator

A tool that takes a website URL as input, scrapes its content and generates a dynamic questionnaire to classify users based on their interests or industry. This application is built with a React/Redux frontend and a Python/Flask backend.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Future Work](#future-work)

## Technologies Used

- **Frontend**: React, Redux
- **Backend**: Python, Flask, Scrapy (for scraping), OpenAI (for question generation)
- **Database**: Postgresql (for storing questions),

## Features

- **Dynamic Question Generation**: Uses scraped website content to generate relevant questions.
- **Progress Tracking**: Displays a progress bar as users complete questions.
- **Responsive Design**: Designed for desktop and mobile with flexible styling.

## Getting Started

### Prerequisites

- **Node.js** and **npm** for the frontend.
- **Python 3.8+** and **pip** for the backend.

### Installation

#### Backend

Navigate to the backend directory:

```bash
cd backend
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
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

### Environment Variables

Set up the following environment variables for the backend directly in your system environment:

- **OPENAI_API_KEY**: API key for OpenAI for generating questions.

## Usage

1. Open the app in the browser.
2. Enter a website URL to start the questionnaire generation process.
3. Answer the generated questions.

## Project Structure

### Frontend

```plaintext
frontend/
├── src/
│   ├── components/
│   │   └── Questionnaire.js       # Main questionnaire component
│   ├── redux/
│   │   ├── actions.js             # Redux actions for question management
│   │   ├── questionReducer.js     # Reducer for question data
│   │   ├── rootReducer.js         # Root reducer
│   │   └── store.js               # Redux store
│   ├── App.js                     # Main application component
│   └── App.css                    # Main CSS for the app
```

### Backend

```plaintext
backend/
├── db/                            # Database connection and setup
├── routes/                        # API routes
├── services/                      # Core backend services
│   ├── db_service.py              # Database service for CRUD operations
│   ├── intent_question_generator.py  # For generating questions based on intent
│   └── question_service.py        # Main logic for handling question processing
├── app.py                         # Flask application entry point
└── requirements.txt               # Python dependencies
```

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

## Future Work

- **Real-Time Questionnaire Injection**: Develop a browser extension or embeddable JavaScript to allow questionnaires to pop up automatically when a user visits a specific website.

- **Async Web Scraping**: Implement asynchronous web scraping capabilities, allowing scraping tasks to run in the background and return results as they complete.
