# import re
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import os
#
#
# # Step 1: Preprocessing
# def preprocess_text(text):
#     text = text.lower()
#     text = re.sub(r'[^\w\s]', '', text)
#     return text
#
#
# # Define the filename for the dataset JSON file
# dataset_file = 'plagiarism_dataset.json'
#
# # Check if the dataset JSON file exists
# if os.path.exists(dataset_file):
#     # If it exists, load the dataset from the file
#     dataset = pd.read_json(dataset_file, orient='records')
# else:
#     # If it doesn't exist, create an empty dataset with the desired columns
#     dataset = pd.DataFrame(columns=['text', 'original_filename', 'filename', 'project_name', 'college_name'])
#
#
# # Function to add a document to the dataset
# def add_document_to_dataset(document, original_filename, filename, project_name, college_name):
#     global dataset
#     new_data = pd.DataFrame(
#         {'text': [preprocess_text(document)], 'original_filename': [original_filename], 'filename': [filename],
#          'project_name': [project_name], 'college_name': [college_name]})
#     dataset = pd.concat([dataset, new_data], ignore_index=True)
#
#
# # Step 3: Compare Documents
# def calculate_similarity(doc1, doc2):
#     tfidf_vectorizer = TfidfVectorizer()
#     tfidf_matrix = tfidf_vectorizer.fit_transform([doc1, doc2])
#     return cosine_similarity(tfidf_matrix)[0][1]
#
#
# # Function to check plagiarism and append to the dataset if similarity < 0.5
# def check_plagiarism(new_document, original_filename, filename, project_name, college_name):
#     new_text = preprocess_text(new_document)
#
#     for index, row in dataset.iterrows():
#         similarity = calculate_similarity(new_text, row['text'])
#         if similarity >= 0.5:
#             return f"Plagiarism detected (Similarity: {similarity:.2f})"
#
#     # If no plagiarism detected, append to the dataset
#     add_document_to_dataset(new_document, original_filename, filename, project_name, college_name)
#
#     # Save the updated dataset to the JSON file
#     dataset.to_json(dataset_file, orient='records')
#
#     return "No plagiarism detected. Document added to the dataset."
#
#
# # Example usage:
# document1 = "This is a sample document for testing."
# original_filename1 = "document1.txt"
# filename1 = "document1.txt"
# project_name1 = "Project A"
# college_name1 = "College X"
#
# document2 = "This is a test document for the example."
# original_filename2 = "document2.txt"
# filename2 = "document2.txt"
# project_name2 = "Project B"
# college_name2 = "College Y"
#
# document3 = "This is a completely different document."
# original_filename3 = "document3.txt"
# filename3 = "document3.txt"
# project_name3 = "Project C"
# college_name3 = "College Z"
#
# print(check_plagiarism(document1, original_filename1, filename1, project_name1, college_name1))
# print(check_plagiarism(document2, original_filename2, filename2, project_name2, college_name2))
# print(check_plagiarism(document3, original_filename3, filename3, project_name3, college_name3))
