import json
from model import load_model, retrain_model
from utilities import bag_of_words
from data_preparation import load_data

def load_processed_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def convert_feedback_to_training_format(processed_data, words, labels, feedback_to_label_map):
    train_x, train_y = [], []
    for feedback in processed_data:
        bow = bag_of_words(feedback['userInput'], words)
        train_x.append(bow)
        
        mapped_label = feedback_to_label_map.get(feedback['feedback'], None)
        print(f"Feedback: {feedback['feedback']}, Mapped Label: {mapped_label}, Available Labels: {labels}")

        if mapped_label not in labels:
            print(f"Label {mapped_label} not recognized in the available labels.")
            continue
        
        output_row = [0] * len(labels)
        output_row[labels.index(mapped_label)] = 1
        train_y.append(output_row)
    return train_x, train_y

def manual_retrain(processed_data_file, model_file, updated_model_file, words, labels, feedback_to_label_map):
    processed_data = load_processed_data(processed_data_file)
    train_x, train_y = convert_feedback_to_training_format(processed_data, words, labels, feedback_to_label_map)

    if not train_y:
        print("No valid training data found.")
        return

    model = load_model(model_file, train_x, train_y)
    updated_model = retrain_model(model, train_x, train_y, updated_model_file)
    print("Model retraining complete.")
    return updated_model

if __name__ == '__main__':
    data_file = 'intents.json'
    pickle_file = 'data.pickle'
    processed_data_file = 'processed_feedback_data.json'
    model_file = 'model.tflearn'
    updated_model_file = 'updated_model.tflearn'

    words, labels, _, _ = load_data(data_file, pickle_file)

    feedback_to_label_map = {
        'positive': 'greeting',  # Map 'positive' feedback to 'greeting' label
        'negative': 'goodbye'    # Map 'negative' feedback to 'goodbye' label
    }

    manual_retrain(processed_data_file, model_file, updated_model_file, words, labels, feedback_to_label_map)
