# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from api.common import *

synonym_data_file = 'synonym.txt'
synonym_data = read_data(synonym_data_file)
synonym_dictionary = {}

for row in synonym_data:
    for word in row[1].split(','):
        synonym_dictionary[word] = row[0]

def transform_synonym(text):
    for word in synonym_dictionary.keys():
        text = text.replace(word, synonym_dictionary[word])

    return text