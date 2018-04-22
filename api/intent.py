# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer

import tensorflow as tf
import numpy as np
import math

from api.common import *

intent_data_file = 'intent.txt'

def stemming(text):
    stemmed_text = ""
    twitter = Twitter()
    tagged_text = twitter.pos(text)
    for token in tagged_text:
        stemmed_text += token[0] + " "

    return stemmed_text[:-1]

intent_data = [(row[0], stemming(row[1])) for row in read_data(intent_data_file)]


docMap = {}
for intent, words in intent_data:
    if docMap.get(intent) == None:
        docMap[intent] = ""

    docMap[intent] += words + " "

docs = []
for intent in docMap.keys():
    docs.append(docMap[intent][:-1])

#print(docs)

wordMap = {}
word_count = 0
for doc in docs:
    for word in doc.split(' '):
        if wordMap.get(word) == None:
            wordMap[word] = word_count
            word_count += 1

print(wordMap)

tfidfVectorizer = [0 for i in range(word_count)]
for word in wordMap.keys():
    for doc in docs:
        if word in doc:
            tfidfVectorizer[wordMap[word]] += 1

for i in range(word_count):
    tfidfVectorizer[i] = math.log(docs.__len__() / tfidfVectorizer[i], docs.__len__())

train_x = []
for intent, words in intent_data:
    temp = [0 for i in range(word_count)]
    for word in words.split(' '):
        temp[wordMap[word]] = math.pow(tfidfVectorizer[wordMap[word]], 5)

    train_x += [temp]

train_x = train_x + [[0 for i in range(word_count)]]
print(train_x)

count_vector = CountVectorizer()
count_vector.fit([intent for intent, words in intent_data] + ["None"])
intent_count = len(count_vector.transform([""]).toarray()[0])

train_y = [np.ndarray.tolist(count_vector.transform([intent]).toarray()[0]) for intent, words in intent_data]
train_y = train_y + [np.ndarray.tolist(count_vector.transform(["#None"]).toarray()[0])]
print(train_y)

intentDictionary = {}
intentDictionary[np.argmax(np.ndarray.tolist(count_vector.transform(["#None"]).toarray()[0]))] = "#None"
for intent, words in intent_data:
    intentDictionary[np.argmax(np.ndarray.tolist(count_vector.transform([intent]).toarray()[0]))] = intent
#print(intentDictionary)

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# 가중치의 차원은 [이전 레이어의 뉴런 갯수, 다음 레이어의 뉴런 갯수]
W1 = tf.Variable(tf.random_uniform([word_count, 10], -1., 1.))
W2 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W3 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W4 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W5 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W6 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W7 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W8 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W9 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W10 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W11 = tf.Variable(tf.random_uniform([10, 10], -1., 1.))
W12 = tf.Variable(tf.random_uniform([10, intent_count], -1., 1.))

# 편향을 각각 각 레이어의 아웃풋 갯수로 설정합니다.
b1 = tf.Variable(tf.zeros([10]))
b2 = tf.Variable(tf.zeros([10]))
b3 = tf.Variable(tf.zeros([10]))
b4 = tf.Variable(tf.zeros([10]))
b5 = tf.Variable(tf.zeros([10]))
b6 = tf.Variable(tf.zeros([10]))
b7 = tf.Variable(tf.zeros([10]))
b8 = tf.Variable(tf.zeros([10]))
b9 = tf.Variable(tf.zeros([10]))
b10 = tf.Variable(tf.zeros([10]))
b11 = tf.Variable(tf.zeros([10]))
b12 = tf.Variable(tf.zeros([intent_count]))

# 신경망의 히든 레이어에 가중치 W와 편향 b을 적용합니다
L1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1))
L2 = tf.nn.relu(tf.add(tf.matmul(L1, W2), b2))
L3 = tf.nn.relu(tf.add(tf.matmul(L2, W3), b3))
L4 = tf.nn.relu(tf.add(tf.matmul(L3, W4), b4))
L5 = tf.nn.relu(tf.add(tf.matmul(L4, W5), b5))
L6 = tf.nn.relu(tf.add(tf.matmul(L5, W6), b6))
L7 = tf.nn.relu(tf.add(tf.matmul(L6, W7), b7))
L8 = tf.nn.relu(tf.add(tf.matmul(L7, W8), b8))
L9 = tf.nn.relu(tf.add(tf.matmul(L8, W9), b9))
L10 = tf.nn.relu(tf.add(tf.matmul(L9, W10), b10))
L11 = tf.nn.relu(tf.add(tf.matmul(L10, W11), b11))

# 최종적인 아웃풋을 계산합니다.
model = tf.add(tf.matmul(L11, W12), b12)

# 활성화 함수로 소프트 맥스, 손실 함수로 크로스 엔트로피 함수를 이용합니다.
cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model))

optimizer = tf.train.AdamOptimizer(learning_rate=0.002)
train_op = optimizer.minimize(cost)

# 신경망 모델 학습
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for step in range(1000):
    sess.run(train_op, feed_dict={X: train_x, Y: train_y})
    #if (step + 1) % 10 == 0:
        #print(step + 1, sess.run(cost, feed_dict={X: train_x, Y: train_y}))

# 결과 확인
prediction = tf.argmax(model, 1)
target = tf.argmax(Y, 1)
print('예측값:', sess.run(model, feed_dict={X: train_x}))
print('예측값:', sess.run(prediction, feed_dict={X: train_x}))
print('실제값:', sess.run(target, feed_dict={Y: train_y}))

is_correct = tf.equal(prediction, target)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('정확도: %.2f' % sess.run(accuracy * 100, feed_dict={X: train_x, Y: train_y}))