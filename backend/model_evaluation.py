import json
import numpy as np 
from sklearn.metrics import precision_score, recall_score, f1_score
from utilities import bag_of_words
from data_preparation import load_data
from model import load_model 

def evaluate_model(model, words, labels, intents, test_data):
    true_labels = []
    predicted_labels = []
    
    for test_item in test_data:
        user_input = test_item['userInput']
        true_label = test_item['label']
        
        # Get the index of the true label and append it to true_labels list
        true_label_index = labels.index(true_label) if true_label in labels else None
        if true_label_index is not None:
            true_labels.append(true_label_index)
        
            results = model.predict([bag_of_words(user_input, words)])
            results_index = np.argmax(results)
            
            # Append the predicted label index to predicted_labels list
            predicted_labels.append(results_index)
    
    if not true_labels or not predicted_labels:
        print("No labels found. Check your test data and label extraction.")
        return {}

    # Convert true and predicted labels to numpy arrays for vectorized operations
    true_labels = np.array(true_labels)
    predicted_labels = np.array(predicted_labels)

    # Calculate metrics
    accuracy = np.mean(predicted_labels == true_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

if __name__ == '__main__':
    data_file = 'intents.json'
    pickle_file = 'data.pickle'
    original_model_file = 'model.tflearn'
    updated_model_file = 'updated_model.tflearn'

    ## Load words, labels, and intents
    words, labels, train_x, train_y = load_data(data_file, pickle_file)
    with open(data_file) as file:
        intents = json.load(file)

    # Define Test Data
    test_data = [
        {'userInput': 'Can you provide your contact details?', 'label': 'contact_information'},
        {'userInput': 'Tell me more about your product features', 'label': 'software_inquiry'},
        {'userInput': 'How do I update my subscription details?', 'label': 'subscription_details'},
        {'userInput': 'I am not happy with the service', 'label': 'feedback'},
        {'userInput': 'How to get a custom solution for my business?', 'label': 'custom_solution'},
        {'userInput': 'Are there any new updates available?', 'label': 'promotion'},
        {'userInput': 'Goodbye, thanks for the assistance', 'label': 'goodbye'},
        {'userInput': 'How long does delivery take?', 'label': 'order_status'},
        {'userInput': 'What are your working hours?', 'label': 'contact_information'},
        {'userInput': 'I want to report a problem with my last order', 'label': 'feedback'},
        {'userInput': 'How do I get a refund?', 'label': 'refund'}
    ]

    # Load and evaluate the original model
    original_model = load_model(original_model_file, train_x, train_y)
    original_model_results = evaluate_model(original_model, words, labels, intents, test_data)

    # Load and evaluate the updated (retrained) model
    updated_model = load_model(updated_model_file, train_x, train_y)
    updated_model_results = evaluate_model(updated_model, words, labels, intents, test_data)

    # Compare the results
    print("Original Model Results:", original_model_results)
    print("Updated Model Results:", updated_model_results)
