from NLPclass import NLP
from mqttConfig import MQTTcontroller

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
MQTTState = MQTTsignal.baseState
state = Scene.none
running = True


while running:
    
    # lecture des signaux MQTT et ajustement de MQTTState
    if not mqttProxi & mqttFacial == "none":
        MQTTState = MQTTsignal.baseState
        print(MQTTsignal.baseState)
    elif mqttProxi & mqttFacial == "none":
        MQTTState = MQTTsignal.proxiState
        print(MQTTsignal.proxiState)
    elif mqttFacial != "none":
        MQTTState = MQTTsignal.facialState
        user = mqttFacial    
    
    # mise en marche des fonctions selon les MQTTState
    if MQTTState == MQTTsignal.baseState:
        pass
    if MQTTState == MQTTsignal.proxiState:
        #pymongo public grab
        #GUI public
        pass
    if MQTTState == MQTTsignal.facialState:
        #pymongo user grab and delegate
        userNameGreeting = username(userGenderDB, userFirstnameDB, userLastnameDB)
        if state == Scene.first:
            #GUI greetings
            nlp.speak(f"Bonjour, comment aller vous aujourd'hui {userNameGreeting}")
            data = ""
            while data == "":
                data = nlp.listening()
            SentimentState = nlp.sentimentAnalysis(data)
            if SentimentState == "POS":
                state = Scene.positive
                print(Scene.positive)
            elif SentimentState == "NEU":
                state = Scene.neutral
                print(Scene.neutral)
            elif SentimentState == "NEG":
                state = Scene.negative
                print(Scene.negative)
        elif state == Scene.positive:
            nlp.speak("Content de voir que vous allez bien.  Puis-je vous aider aujourd'hui?")
            #GUI positif
            data = ""
            while data == "":
                data = nlp.listening()
            pass
        elif state == Scene.neutral:
            nlp.speak("Avez vous un besoin particulier aujourd'hui? Puis-je vous aider?")
            #GUI neutre
            data = ""
            while data == "":
                data = nlp.listening()
            pass
        elif state == Scene.negative:
            nlp.speak("Vous semblez en difficulté, comment puis-je vous aider?")
            #GUI negatif
            data = ""
            while data == "":
                data = nlp.listening()
            pass
        elif state == Scene.none:
            pass

                
        