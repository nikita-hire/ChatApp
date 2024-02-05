import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
#from profanity_check import predict, predict_prob
from keras.models import load_model
model = load_model('model.h5')
import json
import random
import csv
import itertools
import pandas as panda
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

from flask import Flask, flash, redirect,render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test_user_response")
def test_user_response():
    userText = request.args.get('msg')
    stri = "Sorry"
    res = final(userText)
    if(res == userText):
        return res
    else:
        return stri


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list  


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def final(msgtxt):
    try:
        dataset = panda.read_csv("datasets/test.csv")
        file = open("datasets/test.csv")
        type(file)
        #print(dataset)
        csvr = csv.reader(file)
        rows=[]
        x = None
        test =  msgtxt
        word = test.replace(" ","")
        str1 = "i am in else!"
        #abuse = ['bc','you are a lesbo','gay','xxx','suck','ganja','behenchod','madarachod','mc','Ghatiya insaan','Randwa','Raand','Madarjaat','Bhosdike','asshole','bitch','erotic','masturbation','lust','bhadkhau']
        for i in range(1,50):
            for row in dataset.abuse:
                if( row == word ):    
                    return row
                    break;
                elif( row != word ):
                    #return str1
                    continue;
                else:    
                    return x              
    except:
        print("something is wrong")       

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


if __name__ == "__main__":
    app.run()