import nltk
import json
import pickle
import numpy as np
import random
from utilities import stemmer

def load_data(data_file, pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            words, labels, train_x, train_y = pickle.load(f)
    except:
        with open(data_file) as file:
            data = json.load(file)
        
        words, labels, docs = [], [], []
        for intent in data['intents']:
            for pattern in intent['patterns']:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs.append((wrds, intent['tag']))
                if intent['tag'] not in labels:
                    labels.append(intent['tag'])
    
        words = [stemmer.stem(w.lower()) for w in words if w != '?']
        words = sorted(list(set(words)))
        labels = sorted(labels)

        training, output = [], []
        out_empty = [0 for _ in range(len(labels))]

        for doc in docs:
            bag = []
            pattern_words = [stemmer.stem(word.lower()) for word in doc[0]]
            for w in words:
                bag.append(1 if w in pattern_words else 0)

            output_row = list(out_empty)
            output_row[labels.index(doc[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        with open(pickle_file, 'wb') as f:
            pickle.dump((words, labels, train_x, train_y), f)

    return words, labels, train_x, train_y
