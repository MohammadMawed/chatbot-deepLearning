from flask import Flask, request, jsonify
import json
from data_preparation import load_data
from model import load_model
from flask_cors import CORS
from datetime import datetime
from chat_interaction import get_response 

app = Flask(__name__)
CORS(app)

data_file = 'intents.json'
pickle_file = 'data.pickle'
model_file = 'model.tflearn'
words, labels, train_x, train_y = load_data(data_file, pickle_file)
model = load_model(model_file, train_x, train_y)

with open(data_file) as file:
    data = json.load(file)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    response = get_response(model, words, labels, data, user_input)
    return jsonify({'response': response})

@app.route('/log_interaction', methods=['POST'])
def log_interaction():
    feedback_data = request.json  
    

    print("Received feedback data:", feedback_data)

    # Check if all required fields are in the feedback_data
    if not all(field in feedback_data for field in ['userInput', 'botResponse', 'feedback']):
        print("Missing fields in feedback data")
        return jsonify({'status': 'error', 'message': 'Feedback data is missing required fields'}), 400
    feedback_data['timestamp'] = datetime.now().isoformat()  # Add server-side timestamp

    # Log the feedback data
    try:
        with open('feedback_logs.json', 'r+') as file:
            try:
                feedback_list = json.load(file)
                if not isinstance(feedback_list, list):
                    feedback_list = [feedback_list]  # Convert to list if it's not
            except json.JSONDecodeError:
                feedback_list = []  # Start with an empty list if the file is empty or not in json format
            
            feedback_list.append(feedback_data)  # Append the new feedback data
            
            file.seek(0)  # Go to the beginning of the file
            json.dump(feedback_list, file, indent=4)  # Write the updated list back to the file
            file.truncate()  # Remove any leftover content
    except Exception as e:
        print(f"Error logging feedback: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to log feedback'}), 500
    
    return jsonify({'status': 'success', 'message': 'Feedback logged successfully'})




if __name__ == '__main__':
    app.run(port=5000)
