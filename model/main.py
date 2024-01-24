import json
from data_preparation import load_data
from model import load_model
from chat_interaction import chat

def main():
    data_file = 'intents.json'
    pickle_file = 'data.pickle'
    model_file = 'model.tflearn'

    words, labels, train_x, train_y = load_data(data_file, pickle_file)
    model = load_model(model_file, train_x, train_y)

    with open(data_file) as file:
        data = json.load(file)

    chat(model, words, labels, data)

if __name__ == "__main__":
    main()
