# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from api.entity import *
from api.intent import *
from api.synonym import *
import jpype
import math

def message(data):
    jpype.attachThreadToJVM()

    text = data["text"]
    text = transform_synonym(text)

    entities = []
    labeled_text = transform_entity(text, entities)
    stemmed_text = stemming(labeled_text)
    vectorized_text = [0 for i in range(word_count)]

    for word in stemmed_text.split(' '):
        if wordMap.get(word) != None:
           vectorized_text[wordMap[word]] = math.pow(tfidfVectorizer[wordMap[word]], 5)

    print(vectorized_text)
    intent_identifier = sess.run(prediction, feed_dict={X: [vectorized_text]})[0]

    print(sess.run(model, feed_dict={X: [vectorized_text]}))
    intent_confidence = np.max(sess.run(model, feed_dict={X: [vectorized_text]}))

    response = {}
    response["text"] = text
    response["intents"] = [{
        "intent" : intentDictionary[intent_identifier],
        "score" : intent_confidence
    }]
    response["entities"] = entities

    return response