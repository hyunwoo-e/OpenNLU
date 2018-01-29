# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from api.entity import *
from api.intent import *
from api.synonym import *
import jpype

def message(data):
    jpype.attachThreadToJVM()

    text = data["text"]
    text = transform_synonym(text)

    entities = []
    labeled_text = transform_entity(text, entities)

    intents = []
    vectorized_text = vect.transform([stemming(labeled_text)]).toarray()


    response = {}
    response["text"] = text
    response["intents"] = [{
        "intent" : mlp.predict(vectorized_text)[0],
        "score" : max(mlp.predict_proba(vectorized_text)[0])
    }]
    response["entities"] = entities

    return response