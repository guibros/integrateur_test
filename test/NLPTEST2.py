from gtts import gTTS
import os
import speech_recognition as speechRecognition
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
    
audio = speechRecognition.Recognizer()

class NLP:
    def __init__(self) -> None:
        pass
        
    def speak(self, text):
        tts = gTTS(text=text, lang='fr', tld='ca')
        audioFile = "audio.mp3"
        tts.save(audioFile)
        os.system('mpg321 audio.mp3')
        
    def listen(self):
        with speechRecognition.Microphone() as source:
            print("say somthing")
            audioData = audio.listen(source) 
            try:
                data = audio.recognize_google(audioData, language="fr-FR")
                print(data)
                #self.speak(data)
                return data
            except Exception as ex:
                print(ex)
                print("cant return text")    
                #self.speak("cant return text")      
                
    def sentimentAnalisys(self, data):
        pass




    
def username(gender, firstname, lastname):
    user = ""
    if gender == "M":
        user += f"Monsieur {lastname}"
    elif gender == "F":
        user += f"Madame {lastname}"
    else:
        user += firstname
    return user


# prefixe = "monsieur"
# nom = "guillaume"
# question1 = f"Comment aller vous aujourd'hui,{prefixe} {nom}"
# question2 = "Aliens, le retour (Aliens) est un film de science-fiction américano-britannique réalisé par James Cameron et sorti en 1986.Deuxième volet de la saga Alien, ce film est la suite d’Alien, le huitième passager (1979) et met en scène l'actrice Sigourney Weaver qui reprend son rôle d'Ellen Ripley, ainsi que les acteurs Michael Biehn, Bill Paxton, Lance Henriksen et Carrie Henn.Dans ce film, Ripley accompagne un détachement de Marines coloniaux qui se rendent sur la planète LV-426a, une colonie spatiale humaine terraformée qui ne donne plus de nouvelles et où la présence de la créature du premier film, l’Alien (désigné sous le terme de « xénomorphe »)b, est suspectée."


# thread1 = Thread(target = speak, args=(question1,))
# speak(question1)
# speak("Vous pouvez parler...")

# thread1.start()



userGenderDB = "M"
userFirstnameDB = "Ginette"
userLastnameDB = "Rancours"


mqtt = MQTTcontroller()
mqttProxi = mqtt.subscription('AHUNTSIC-PROJ-INT/proxi')
mqttFacial = mqtt.subscription('AHUNTSIC-PROJ-INT/facial')


MQTTState = MQTTsignal.baseState
state = Scene.none
running = True


while running:
    if not mqttProxi & mqttFacial == "none":
        MQTTState = MQTTsignal.baseState
    elif mqttProxi & mqttFacial == "none":
        MQTTState = MQTTsignal.proxiState
    elif mqttProxi & mqttFacial != "none":
        MQTTState = MQTTsignal.proxiState
        user = mqttFacial    
    
    #global stateScene
    if MQTTState == MQTTsignal.baseState:
        pass
    if MQTTState == MQTTsignal.proxiState:
        pass
    if MQTTState == MQTTsignal.facialState:
        userNameGreeting = username(userGenderDB, userFirstnameDB, userLastnameDB)
        if state == Scene.first:
            NLP.speak(f"Bonjour, comment aller vous aujourd'hui {userNameGreeting}")
            data = ""
            while data == "":
                data = NLP.listening()
            SentimentState = NLP.sentimentAnalysis(data)
            if SentimentState == "POS":
                state = Scene.positive
            elif SentimentState == "NEU":
                state = Scene.neutral
            elif SentimentState == "NEG":
                state = Scene.negative
        elif state == Scene.positive:
            pass
        elif state == Scene.neutral:
            pass
        elif state == Scene.negative:
            pass
        elif state == Scene.none:
            pass

                
        