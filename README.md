## OpenBot [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hyunwoo9301/OpenBot/blob/master/LICENSE)

Web-based API Server like 'IBM Watson Conversation API', 'Microsoft Language Understanding Intelligence Service'

OpenBot & OpenNLU provides what you need to build retrieval-based korean chatbot. 

[OpenNLU](https://github.com/hyunwoo9301/OpenNLU) is able to recognize intent and entity using DNN models.

[OpenBot](https://github.com/hyunwoo9301/OpenBot) is able to configure dialog to response message, manage conversation information of user and handle exceptions.

## Overview
![default](https://user-images.githubusercontent.com/20318775/35503799-85a729aa-0524-11e8-8807-1cf3a6f11d63.png)

## Installation and Settings
### setting requirements
- intent.txt (write intents and sentences)
- entity.txt (write entities and values)
- synonym.txt (write words and synonyms)

### build requirements
- Python 3.5
- django, djangorestframework
- numpy
- gensim
- scipy
- sklearn
- tensorflow
- konlpy
- JPype

### execute requirements
- python manage.py runserver <ip>:<port>
- python manage.py runserver 0.0.0.0:8000 (ALL)

## Projects based on OpenBot & OpenNLU
### - [KONKUK BOT](https://www.youtube.com/watch?v=se6ngTUQdxk)

## Samples
### Sample Request
```json
{
	"text":"건대입구 위치 알려줘"
}
```

### Sample Response
```json
{
    "intents": [
        {
            "intent": "#Location",
            "score": 0.8604595835264408
        }
    ],
    "entities": [
        {
            "values": [
                {
                    "end": 4,
                    "start": 0,
                    "value": "건대입구"
                }
            ],
            "entity": "@장소"
        }
    ],
    "text": "건대입구 위치 알려줘"
}
```

### Sample Request
```json
{
	"text":"내일 시간표 알려줘"
}
```

### Sample Response
```json
{
    "entities": [
        {
            "entity": "Date",
            "values": [
                {
                    "end": 2,
                    "value": "2017-11-10",
                    "start": 0
                }
            ]
        }
    ],
    "intents": [
        {
            "score": 0.9976826419186618,
            "intent": "#Schedule"
        }
    ],
    "text": "내일 시간표 알려줘"
}
```
