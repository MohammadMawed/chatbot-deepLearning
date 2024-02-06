import json
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Initializing the PorterStemmer
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    # Tokenize
    words = word_tokenize(text)
    # Remove stopwords and stem the words
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)

def process_feedback_data(file_path):
    processed_data = []
    try:
        with open(file_path, 'r') as file:
            feedback_list = json.load(file)
            for feedback in feedback_list:
                # Clean and preprocess user input and bot response
                feedback['userInput'] = clean_text(feedback.get('userInput', ''))
                feedback['botResponse'] = clean_text(feedback.get('botResponse', ''))
                # Add processed data to processed_data list
                processed_data.append(feedback)
    except Exception as e:
        print(f"Error processing feedback data: {e}")
    return processed_data


def save_processed_data(processed_data, output_file_path):
    try:
        # Read existing data from the file
        existing_data = []
        try:
            with open(output_file_path, 'r') as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]  # Convert to list if it's not
        except json.JSONDecodeError:
            # If the file is empty or not in json format, start with an empty list
            existing_data = []
        except FileNotFoundError:
            # If the file does not exist, it will be created
            pass

        # Combine existing data with new processed data
        combined_data = existing_data + processed_data

        # Save the combined data to the file
        with open(output_file_path, 'w') as file:
            json.dump(combined_data, file, indent=4)
    except Exception as e:
        print(f"Error saving processed data: {e}")



feedback_logs_path = 'feedback_logs.json'
processed_data_path = 'processed_feedback_data.json'

# Process the feedback data and save the results
processed_data = process_feedback_data('feedback_logs.json')
print(f"Processed {len(processed_data)} feedback records.")

save_processed_data(processed_data, processed_data_path)
