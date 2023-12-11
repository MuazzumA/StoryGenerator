from flask import Flask, render_template, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate a story based on genre
def generate_story_by_genre(genre):
    # Define URLs for novels
    novel_urls = {
        'fantasy': 'https://www.gutenberg.org/cache/epub/11/pg11.txt',  # Alice's Adventures in Wonderland
        'mystery': 'https://www.gutenberg.org/cache/epub/5200/pg5200.txt',  # Metamorphosis by Franz Kafka
    }

    genre_url = novel_urls.get(genre.lower())
    if genre_url:
        response = requests.get(genre_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            novel_text = soup.get_text()
            # Tokenize the novel text into sentences
            sentences = novel_text.split('.')
            # Remove empty lines and leading/trailing whitespaces
            dataset = [sentence.strip() for sentence in sentences if sentence.strip()]
        else:
            dataset = ["Failed to fetch the novel. Status Code: {}".format(response.status_code)]
    else:
        dataset = ["No specific novel found for the chosen genre: {}".format(genre)]

    # Randomly select a sentence from the chosen dataset
    generated_sentence = random.choice(dataset)

    return generated_sentence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateStory', methods=['POST'])
def generate_story():
    genre = request.form['genre']

    # Generate story based on the input genre
    generated_sentence = generate_story_by_genre(genre)

    return render_template('index.html', genre=genre, generated_sentence=generated_sentence)

if __name__ == '__main__':
    app.run(debug=True)
