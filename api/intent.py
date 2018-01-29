# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from konlpy.tag import Twitter
import numpy as np
import itertools

from api.common import *

intent_data_file = 'intent.txt'
word_class_count = 2;

def stemming(text):
    stemmed_text = ""
    twitter = Twitter()
    tagged_text = twitter.pos(text)
    for token in tagged_text:
        if ((token[1] == 'Noun') or (token[1] == 'Verb')): # or (token[1] == 'Adjective')
            stemmed_text += token[0] + "/" + token[1] + " "

    return stemmed_text

intent_data = [(row[0], stemming(row[1])) for row in read_data(intent_data_file)]
vect = TfidfVectorizer()
vect.fit([row[1] for row in intent_data])

print([row[1] for row in intent_data])


nones = []
for tuple in itertools.product(range(2), repeat=word_class_count):
    none = []
    for i in tuple:
        none.append(i)

    none.extend([0 for i in range(len(vect.transform([""]).toarray()[0]) - word_class_count)])
    nones += [np.array(none)]

train_x = [vect.transform([words]).toarray()[0] for intent, words in intent_data]
train_x = train_x + nones
print(train_x)



train_y = [intent for intent, words in intent_data]
train_y = train_y + ["#None" for i in range(len(nones))]

mlp = MLPClassifier(solver='lbfgs', alpha=0.002, hidden_layer_sizes=(10, 10), random_state=1234)
mlp.fit(train_x, train_y)