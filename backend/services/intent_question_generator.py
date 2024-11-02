from bs4 import BeautifulSoup
from openai import OpenAI
import nltk
from tests.MockResponse import MockChatCompletion
import os
nltk.download('punkt')
nltk.download('stopwords')


def clean_scraped_content(scraped_content):
    """Clean the scraped content with BeautifulSoup to get the text."""
    soup = BeautifulSoup(scraped_content, 'html.parser')
    return ' '.join([tag.get_text() for tag in soup.find_all(['h1', 'h2', 'h3', 'p'])])

def generate_intent_based_questions(text_content):
    """
    Generate multiple questions to understand user intent.
    These questions are focused on categorizing the user's interest based on the entire content.
    """
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    prompt = (
        f"Generate a list of questions that help in categorizing user intent or interest based on the following content. "
        f"For each question, also provide a few options (choices) that a user might select in response. "
        f"The questions should guide the user to express their needs, interests, or purpose related to the content "
        f"without testing factual knowledge.\n\nContent: {text_content[:1000]}"
    )

    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]  # Correct format for `messages`
    )

    # For testing purposes
    # response = MockChatCompletion()

    print("response", response)
    
    response_message = response.choices[0].message.content.strip()
    
    return response_message

def parse_questions_and_options(generated_text):
    """
    Parse the generated text to separate questions and options.
    Returns a list of dictionaries with 'question' and 'options' keys.
    """
    parsed_data = []
    lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
    
    current_question = None
    options = []

    for line in lines:
        # Detect if the line is a question (assuming it starts with a number and a dot)
        if line[0].isdigit() and line[1] == '.':
            # If there's an existing question, add it to the parsed data
            if current_question:
                parsed_data.append({
                    "question": current_question,
                    "options": options
                })
            # Start a new question
            current_question = line
            options = []
        else:
            # Otherwise, it's an option; add it to the current options list
            options.append(line)

    # Add the last question to parsed data after loop
    if current_question:
        parsed_data.append({
            "question": current_question,
            "options": options
        })

    return parsed_data
