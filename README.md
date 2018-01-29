## OpenBot [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hyunwoo9301/OpenBot/blob/master/LICENSE)

Web-based API Server like 'IBM Watson Conversation API', 'Microsoft Language Understanding Intelligence Service'

OpenBot & OpenNLU provides what you need to build retrieval-based korean chatbot.

OpenBot is able to configure dialog to response message.

OpenNLU is able to process korean natural language using pre-built or custom-trained language models.

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
### [KONKUK BOT](https://www.youtube.com/watch?v=se6ngTUQdxk)
