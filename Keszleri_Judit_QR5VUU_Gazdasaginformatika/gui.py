import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('model.h5')
import json
import random
import os
thisFolder = os.path.dirname(os.path.abspath(__file__))
intentsFile = os.path.join(thisFolder, 'intents.json')
intents = json.loads(open(intentsFile).read())
words = pickle.load(open('words.txt','rb'))
classes = pickle.load(open('classes.txt','rb'))

##########################################################################
# Kommunikátor

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    return_list = []

    if len(results) == 0:
        return_list.append({"intent": 2, "probability": 4})
    else :
        results.sort(key=lambda x: x[1], reverse=True)
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    result = "I do not understand"
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


##########################################################################################################
# GUI

import tkinter
from tkinter import *

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        res = chatbot_response(msg)
        ChatLog.insert(END, "ANN: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title("Chat")
base.geometry("600x700")
base.resizable(width=FALSE, height=FALSE)

ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#323dde", activebackground="#050dfa",fg='#ffffff',
                    command= send )

EntryBox = Text(base, bd=0, bg="white",width="59", height="5", font="Arial")

scrollbar.place(x=576,y=6, height=586)
ChatLog.place(x=6,y=6, height=586, width=570)
EntryBox.place(x=150, y=601, height=90, width=440)
SendButton.place(x=6, y=601, height=90)

base.mainloop()
