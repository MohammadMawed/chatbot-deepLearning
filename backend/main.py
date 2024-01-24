from flask import Flask, request, jsonify
import json
from data_preparation import load_data
from model import load_model
from chat_interaction import get_response  # Import the modified function

app = Flask(__name__)

# Load the model and other necessary data
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

if __name__ == '__main__':
    app.run(port=5000)
