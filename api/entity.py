# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from api.common import *

import re
import datetime

entity_data_file = 'entity.txt'
entity_data = read_data(entity_data_file)
entity_dictionary = {}

for row in entity_data:
    for word in row[1].split(','):
        entity_dictionary[word] = row[0]

def insert_entity(entityMap, entity, value, start, end):
    if entityMap.get(entity) == None:
        entityMap[entity] = []
    entityMap[entity].append({"value": value, "start": start, "end": end})

def replace_text(blanked_text, labeled_text, entity, match):
    return blanked_text.replace(match, " " * len(match)), labeled_text.replace(match, entity, 1)

def transform_entity(text, entities):
    # 동의어 처리
    labeled_text = text
    blanked_text = text

    entityMap = {}

    # 유저 엔티티
    for word in entity_dictionary.keys():
        for match in re.finditer(word, text):
            insert_entity(entityMap, entity_dictionary[word], match.group(), match.start(), match.end())
            blanked_text, labeled_text = replace_text(blanked_text, labeled_text, entity_dictionary[word], word)

    # 시스템 엔티티
    for match in re.finditer("\d{4}-\d{1,2}-\d{1,2}", blanked_text):
        insert_entity(entityMap, "Date", str(datetime.datetime.strptime(match.group(), "%Y-%m-%d"))[:10], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("(\d{4})년[ ]*(\d{1,2})월[ ]*(\d{1,2})일", blanked_text):
        insert_entity(entityMap, "Date", str(datetime.datetime.strptime(match.group(1) + "-" + match.group(2) + "-" + match.group(3), "%Y-%m-%d"))[:10], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("(\d{4})년[ ]*(\d{1,2})월", blanked_text):
        insert_entity(entityMap, "Date", str(datetime.datetime.strptime(match.group(1) + "-" + match.group(2), "%Y-%m"))[:10], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("(\d{4})년", blanked_text):
        insert_entity(entityMap, "Date", str(datetime.datetime.strptime(match.group(1), "%Y"))[:10], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("(\d{1,2})월[ ]*(\d{1,2})일", blanked_text):
        insert_entity(entityMap, "Date", str(datetime.datetime.strptime(str(datetime.datetime.now().year)+"-"+match.group(1) + "-" + match.group(2), "%Y-%m-%d"))[:10], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("오늘", blanked_text):
        insert_entity(entityMap, "Date", datetime.datetime.now().strftime("%Y-%m-%d"), match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("내일", blanked_text):
        insert_entity(entityMap, "Date", (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d"), match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Date", match.group())

    for match in re.finditer("(\d{1,2})시[ ]*(\d{1,2})분[ ]*(\d{1,2})초", blanked_text):
        insert_entity(entityMap, "Time", str(datetime.datetime.strptime(match.group(1) + ":" + match.group(2) + ":" + match.group(3), "%H:%M:%S"))[11:], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Time", match.group())

    for match in re.finditer("(\d{1,2})시[ ]*(\d{1,2})분", blanked_text):
        insert_entity(entityMap, "Time", str(datetime.datetime.strptime(match.group(1) + ":" + match.group(2), "%H:%M"))[11:], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Time", match.group())

    for match in re.finditer("(\d{1,2})시", blanked_text):
        insert_entity(entityMap, "Time", str(datetime.datetime.strptime(match.group(1), "%H"))[11:], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Time", match.group())

    for match in re.finditer("[\d]+원", blanked_text):
        insert_entity(entityMap, "Currency", match.group()[:-1], match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Currency", match.group())

    for match in re.finditer("[\d]+", blanked_text):
        insert_entity(entityMap, "Number", match.group(), match.start(), match.end())
        blanked_text, labeled_text = replace_text(blanked_text, labeled_text, "Number", match.group())

    for key in entityMap.keys():
        entities.append({"entity": key, "values": entityMap.get(key)})

    return labeled_text