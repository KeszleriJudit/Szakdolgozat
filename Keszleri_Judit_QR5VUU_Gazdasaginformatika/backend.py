#################################################
#   Python 3.6.6                                #
#   pip install numpy                           #
#   pip install tensorflow                      #
#   pip install keras                           #
#   pip install nltk                            #
#   pip install pandas                          #
#   pip install spacy                           #
#   pip install cython                          #
#   python -m spacy download en_core_web_sm     #
#   pip install xlrd                            #
#################################################

import spacy
nlp = spacy.load('en_core_web_sm')
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import helpers
import os

############################################################
# JSON file-ok generálása excel fileból

xlsx = helpers.excelFileReader('Festekbolt.xlsx')
shopInfo = xlsx.getShopInfo()
openHours = xlsx.getOpenHours()
storeItems = xlsx.getStoreItems()
itemValuePair = xlsx.getItemValuePairs()

store = []

for i in shopInfo:
    store.append(i)

for i in openHours:
    store.append(i)

for i in storeItems:
    store.append(i)

for i in itemValuePair:
    store.append(i)

for i in store:
    print(i.getObjectAsJSON())

thisFolder = os.path.dirname(os.path.abspath(__file__))
jsonFile = os.path.join(thisFolder, 'base.json')
intentsFile = os.path.join(thisFolder, 'intents.json')
f = open(jsonFile,"rt", encoding="utf-8")
newFile = open(intentsFile,'wt')
for l in f:  
    newFile.write(l)   
newFile.close()
f.close()

newFile = open(intentsFile,'at')
counter = 0
for s in store:    
    newFile.write(s.getObjectAsJSON())
    if counter < len(store) - 1:
        newFile.write(",\n")
    counter += 1
      
newFile.write("\t]\n}")

newFile.close()

################################################################################################
# Háló betanítása

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open(intentsFile).read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique lemmatized words", words)

pickle.dump(words,open('words.txt','wb'))
pickle.dump(classes,open('classes.txt','wb'))

training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(train_y[0]), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

trained_model = model.fit(np.array(train_x), np.array(train_y), epochs=4500, batch_size=128, verbose=1)

model.save('model.h5', trained_model)
