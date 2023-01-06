from NLPclass import NLP
from mqttConfig import MQTTcontroller
from atlasProfil import RPA
from threading import Thread
from enum import Enum
from datetime import datetime as dt
import time


RPA_db = RPA()
NLP = NLP()

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
                self.main = f''
                self.secondary = 'En veille'
                print(CurrentSTATE)
            elif self.MQTTState.message == 'Object':  # What to do when object
                CurrentSTATE = STATE.objectState
                self.main = f''
                self.secondary = 'Objet present'
                print(CurrentSTATE)
            elif self.MQTTState.message == 'IdentificationDelay':  # What to do when face
                CurrentSTATE = STATE.identificationDelay
                self.secondary = 'Identification en cours.'
                self.secondary = 'Identification en cours..'
                self.secondary = 'Identification en cours...'
                print(CurrentSTATE)
            elif self.MQTTState.message == 'Unknown':  # What to do when face
                CurrentSTATE = STATE.unknownState 
                self.main = f''
                self.secondary = 'Utilisateur inconnu'
                print(CurrentSTATE)
            elif 'Identified: ' in self.MQTTState.message:  # What to do when recognized face
                CurrentSTATE = STATE.facialState
                UserIdentity = self.MQTTState.message.strip('Identified: ')
                CurrentUSER = RPA_db.findClient(UserIdentity)
                print(CurrentSTATE, f'User: {UserIdentity}')
                self.main = f'Bonjour {UserIdentity}'
                self.secondary = 'Comment te sens-tu ?'
                
            self.date = dt.now().strftime("%Y-%m-%d")
            self.time = dt.now().strftime("%I:%M:%S %p")
            
            #######################
            # SECTION SCENE STATE #
            #######################
            
 
            time.sleep(0.5)
        print('Command Center Loop ending')

if __name__ == '__main__':
    try:
        # Instanciation du module de langue naturel
        nlp = NLP()
        
        # Instanciation de la base de donnees
        RPA_db = RPA()
        
        # Run Command Center loop Thread
        cc = CommandCenter()
        commandCenterThread = Thread(target=cc.runCommandCenter)
        commandCenterThread.start()

    except KeyboardInterrupt:
        cc.running = False