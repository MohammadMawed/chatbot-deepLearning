import random
import numpy as np
from utilities import bag_of_words

def get_response(model, words, labels, data, user_input):
    results = model.predict([bag_of_words(user_input, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in data['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return random.choice(responses)

    return "I didn't understand that." 

