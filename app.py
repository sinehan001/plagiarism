from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)


# Step 1: Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


# Define the filename for the dataset JSON file
dataset_file = 'plagiarism_dataset.json'

# Check if the dataset JSON file exists
if os.path.exists(dataset_file):
    # If it exists, load the dataset from the file
    dataset = pd.read_json(dataset_file, orient='records')
else:
    # If it doesn't exist, create an empty dataset with the desired columns
    dataset = pd.DataFrame(columns=['text', 'original_filename', 'filename', 'project_name', 'college_name'])


# Function to add a document to the dataset
def add_document_to_dataset(document, original_filename, filename, project_name, college_name):
    global dataset
    new_data = pd.DataFrame(
        {'text': [preprocess_text(document)], 'original_filename': [original_filename], 'filename': [filename],
         'project_name': [project_name], 'college_name': [college_name]})
    dataset = pd.concat([dataset, new_data], ignore_index=True)


# Step 3: Compare Documents
def calculate_similarity(doc1, doc2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([doc1, doc2])
    return cosine_similarity(tfidf_matrix)[0][1]


# Function to check plagiarism and append to the dataset if similarity < 0.5
def check_plagiarism(new_document, original_filename, filename, project_name, college_name):
    new_text = preprocess_text(new_document)

    for index, row in dataset.iterrows():
        similarity = calculate_similarity(new_text, row['text'])
        if similarity >= 0.5:
            return f"Plagiarism detected (Similarity: {similarity:.2f})"

    # If no plagiarism detected, append to the dataset
    add_document_to_dataset(new_document, original_filename, filename, project_name, college_name)

    # Save the updated dataset to the JSON file
    dataset.to_json(dataset_file, orient='records')

    return "No plagiarism detected. Document added to the dataset."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism_route():
    document = request.form['document']
    original_filename = request.form['original_filename']
    filename = request.form['filename']
    project_name = request.form['project_name']
    college_name = request.form['college_name']

    result = check_plagiarism(document, original_filename, filename, project_name, college_name)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
