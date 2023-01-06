from NLPclass import NLP
from mqttConfig import MQTTcontroller
from atlasProfil import RPA
from threading import Thread
from enum import Enum
from datetime import datetime as dt
import time


RPA_db = RPA()
nlp = NLP()

class STATE(Enum):
    baseState = "basestate"
    objectState = "objectState"
    identificationDelay = 'identificationDelay'
    unknownState = 'unknownstate'
    facialState = "facialstate"

class Scene(Enum):
    none = "none"
    first = "first"
    positive = "positive"
    neutral = "neutral" 
    negative = "negative"


class CommandCenter:
    def __init__(self):
        self.MQTTState = MQTTcontroller(default='Nothing')
        self.MQTTState.subscription('AHUNTSIC-PROJ-INT/identity')
        self.CurrentSTATE = self.MQTTState.message
        self.SceneSTATE = Scene.first
        self.running = True
        self.date = dt.now().strftime("%Y-%m-%d")
        self.time = dt.now().strftime("%I:%M:%S %p")
        self.main = 'Bonjour'
        self.secondary = 'Assistant RPA'

    def grabSpeechData(self, tryCount):
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
    
    def username(self, firstname, lastname, gender='M'):
        user = ""
        if gender == "M":
            user += f"Monsieur {lastname}"
        elif gender == "F":
            user += f"Madame {lastname}"
        else:
            user += firstname
        return user

    def runCommandCenter(self):
        while self.running:
            
            # lecture des signaux MQTT et ajustement de MQTTState
            if self.MQTTState.message == 'Nothing':  # What to do when nothing
                CurrentSTATE = STATE.baseState
                print(CurrentSTATE)
            elif self.MQTTState.message == 'Object':  # What to do when object
                CurrentSTATE = STATE.objectState
                print(CurrentSTATE)
            elif self.MQTTState.message == 'IdentificationDelay':  # What to do when face
                CurrentSTATE = STATE.identificationDelay
                print(CurrentSTATE)
            elif self.MQTTState.message == 'Unknown':  # What to do when face
                CurrentSTATE = STATE.unknownState 
                print(CurrentSTATE)
            elif 'Identified: ' in self.MQTTState.message:  # What to do when recognized face
                CurrentSTATE = STATE.facialState
                UserId = self.MQTTState.message.strip('Identified: ')
                CurrentUSER = RPA_db.findClient(UserId)
                print(CurrentSTATE, f'User: {UserId}')
                
            
            #######################
            # SECTION SCENE STATE #
            #######################
            
            if CurrentSTATE == STATE.baseState: #GUI vide
                self.main = ''
                self.secondary = ''
                self.date = ''
                self.time = ''
                print(CurrentSTATE)
            elif CurrentSTATE == STATE.objectState: #GUI vide
                self.main = ''
                self.secondary = 'Objet Présent'
                self.date = ''
                self.time = ''
                print(CurrentSTATE)
            elif CurrentSTATE == STATE.identificationDelay: #GUI gif
                self.main = ''
                self.secondary = 'identification en cours'
                self.date = ''
                self.time = ''
                print(CurrentSTATE)
            elif CurrentSTATE == STATE.unknownState: #GUI 'public'
                self.main = 'current activities'
                self.secondary = ''
                self.date = 'dt.now().strftime("%Y-%m-%d")'
                self.time = 'dt.now().strftime("%I:%M:%S %p")'
                print(CurrentSTATE)
            elif CurrentSTATE == STATE.facialState: #GUI 'public'
                
                self.date = 'dt.now().strftime("%Y-%m-%d")'
                self.time = 'dt.now().strftime("%I:%M:%S %p")'
                
                
                self.main = f'Bonjour {UserId}'
                userName = CurrentUSER['ClientInfo']['firstName']
                self.secondary = 'Comment te sens-tu ?'
                nlp.speak(f"Bonjour, comment aller vous aujourd'hui {userName}")
                data = self.grabSpeechData(3)
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
                
               
            
            
 
            time.sleep(0.5)
        print('Command Center Loop ending')

# if __name__ == '__main__':
#     try:
#         # Instanciation du module de langue naturel
#         nlp = NLP()
        
#         # Instanciation de la base de donnees
#         RPA_db = RPA()
        
#         # Run Command Center loop Thread
#         cc = CommandCenter()
#         commandCenterThread = Thread(target=cc.runCommandCenter)
#         commandCenterThread.start()

#     except KeyboardInterrupt:
#         cc.running = False