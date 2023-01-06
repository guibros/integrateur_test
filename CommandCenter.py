from NLPclass import NLP
from mqttConfig import MQTTcontroller
from profilAtlas import Profil

from threading import Thread
from enum import Enum


class MQTTsignal(Enum):
    baseState = "basestate"
    proxiState = "proxistate"
    facialState = "facialstate"

class Scene(Enum):
    none = "none"
    first = "first"
    positive = "positive"
    neutral = "neutral" 
    negative = "negative"


def username(gender, firstname, lastname):
    user = ""
    if gender == "M":
        user += f"Monsieur {lastname}"
    elif gender == "F":
        user += f"Madame {lastname}"
    else:
        user += firstname
    return user

def grabSpeechData(tryCount):
    data = ""
    counter = 0
    while data == "" and counter != tryCount:
        if counter != 0:
            nlp.speak("Pouvez-vous répéter?")
        data = nlp.listen()
        print(f"while: {data}")
        print(type(data))
        counter += 1
    if data == "":
        nlp.speak("Passons a autre chose")
    print(f"done: {data}")
    return data

def analyzeSpeech(text):
    pass

class kivy(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1   

def call(number):
    pass


        

#Database setup
userGenderDB = "M"
userFirstnameDB = "Ginette"
userLastnameDB = "Rancours"

#instanciation du module de langue naturel
nlp = NLP()

#instanciation du module de communication mqtt
mqtt = MQTTcontroller()
mqttProxi = mqtt.subscription('AHUNTSIC-PROJ-INT/proxi')
mqttFacial = mqtt.subscription('AHUNTSIC-PROJ-INT/facial')

# initialisation des états
CurrentState = MQTTsignal.baseState
SceneState = Scene.none
running = True


while running:
    
    #kivypagerunning

    # lecture des signaux MQTT et ajustement de MQTTState
    if not mqttProxi & mqttFacial == "none":
        CurrentState = MQTTsignal.baseState
        print(MQTTsignal.baseState)
    elif mqttProxi & mqttFacial == "none":
        CurrentState = MQTTsignal.proxiState
        print(MQTTsignal.proxiState)
    elif mqttFacial != "none":
        CurrentState = MQTTsignal.facialState
        user = mqttFacial    
    
    # mise en marche des fonctions selon les MQTTState
    if CurrentState == MQTTsignal.baseState:
        pass
    if CurrentState == MQTTsignal.proxiState:
        #pymongo public grab
        #GUI public
        pass
    if CurrentState == MQTTsignal.facialState:
        #pymongo user grab and delegate
        userNameGreeting = username(userGenderDB, userFirstnameDB, userLastnameDB)
        if SceneState == Scene.first:
            #GUI greetings
            nlp.speak(f"Bonjour, comment aller vous aujourd'hui {userNameGreeting}")
            data = grabSpeechData(3)
            SentimentState = nlp.sentimentAnalysis(data)
            if SentimentState == "POS":
                SceneState = Scene.positive
                print(Scene.positive)
            elif SentimentState == "NEU":
                SceneState = Scene.neutral
                print(Scene.neutral)
            elif SentimentState == "NEG":
                SceneState = Scene.negative
                print(Scene.negative)
        elif SceneState == Scene.positive:
            nlp.speak("Content de voir que vous allez bien.  Puis-je vous aider aujourd'hui?")
            #GUI positif
            data = grabSpeechData(3)
            analyzeSpeech(data)
            pass
        elif SceneState == Scene.neutral:
            nlp.speak("Avez vous un besoin particulier aujourd'hui? Puis-je vous aider?")
            #GUI neutre
            data = grabSpeechData(3)
            analyzeSpeech(data)
            pass
        elif SceneState == Scene.negative:
            nlp.speak("Vous semblez en difficulté, comment puis-je vous aider?")
            #GUI negatif
            data = grabSpeechData(3)
            analyzeSpeech(data)
            pass
        elif SceneState == Scene.none:
            pass

                
        