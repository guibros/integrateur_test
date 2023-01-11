from NLPclass import NLP
from mqttConfig import MQTTcontroller
from atlasProfilV2 import RPA
from threading import Thread
from enum import Enum
from datetime import datetime as dt
import time
import display


# Instantiation of DB and Natural Language Processing module
RPA_db = RPA()
nlp = NLP()

# Setting default MQTT Message
# DEFAULTMQTTMESSAGE = 'Nothing'
DEFAULTMQTTMESSAGE = 'Identified: ' # Also change "# Get UserId" for tests
DEFAULTUSER = 'Phil'

# Creating STATE state machine class
class STATE(Enum):
    baseState = "basestate"
    objectState = "objectState"
    identificationDelay = 'identificationDelay'
    unknownState = 'unknownstate'
    facialState = "facialstate"

# Creating SCENE state machine class
class Scene(Enum):
    none = "none"
    first = "first"
    positive = "positive"
    neutral = "neutral" 
    negative = "negative"

# Creating main CommandCenter class 
class CommandCenter:
    def __init__(self):
        self.MQTTState = MQTTcontroller(default=DEFAULTMQTTMESSAGE)
        self.MQTTState.subscription('AHUNTSIC-PROJ-INT/identity')
        self.CurrentSTATE = STATE.baseState
        self.SceneSTATE = Scene.none
        self.running = True
        
        # Kivy variables
        self.main = ''
        self.spinner = ''
        self.secondary = ''
        self.date = ''
        self.time = ''
        
        # User hook
        self.BUSY_WITH_USER = True

    def grabSpeechData(self, tryCount):
        data = ""
        counter = 0
        while data == "" and counter != tryCount:
            if counter != 0:
                nlp.speak("Pouvez-vous répéter?")
            data = nlp.listen()
            counter += 1
        if data == "":
            nlp.speak("Passons a autre chose")
            return
            # Put ending condition
        print(f"User's response: {data}")
        return data
    
    # This method starts the gTTS in a thread to allow quicker loading of the listening
    def speechThread(self, text):
        speechThread = Thread(target=nlp.speak, args=(text, ))
        speechThread.start()
     
    # This method restarts or ends an interaction loop after a complete interaction cycle 
    def postResponse(self):
        display.otherRequest(self)
        text = "Avez-vous besoin d'autres chose?"
        nlp.speak(text)
        data = nlp.listen() #does it grab listening error?
        if data == 'oui':
            return
        else:
            nlp.speak('Au revoir.')
            self.CurrentSTATE = STATE.baseState
            self.BUSY_WITH_USER = False    
            display.turnOff(self)
            time.sleep(5)
            display.showNothing(self)  
            time.sleep(10)  

    def runCommandCenter(self):
        while self.running:
            
            # lecture des signaux MQTT et ajustement de MQTTState
            if self.MQTTState.message == 'Nothing':  # What to do when nothing
                self.CurrentSTATE = STATE.baseState
                display.showNothing(self)
                print(self.CurrentSTATE)
            elif self.MQTTState.message == 'Object':  # What to do when object
                self.CurrentSTATE = STATE.objectState
                display.showNothing(self)
                print(self.CurrentSTATE)
            elif self.MQTTState.message == 'IdentificationDelay':  # What to do when face
                self.CurrentSTATE = STATE.identificationDelay
                display.identificationProcess(self)
                print(self.CurrentSTATE)
            elif self.MQTTState.message == 'Unknown':  # What to do when face
                self.CurrentSTATE = STATE.unknownState 
                display.unknownUser(self)
                print(self.CurrentSTATE)
            elif 'Identified: ' in self.MQTTState.message:  # What to do when recognized face
                self.CurrentSTATE = STATE.facialState
                
                # Get UserId
                UserID = self.MQTTState.message.strip('Identified: ')
                
                # Get User data
                CurrentUSER = RPA_db.findClient(UserID)
                
                # Failsafe if DB Returns None
                if CurrentUSER == None:
                    # FAKE UserID
                    UserID = DEFAULTUSER
                    CurrentUSER = RPA_db.findClient(DEFAULTUSER)
                    
                userFirstName = CurrentUSER['ClientInfo']['firstName']
                print(self.CurrentSTATE, f'User: {userFirstName}')
                
                # Display and Speak Greeting
                display.identifiedUser(self, userFirstName)
                
                # Lock below Scene state loop with identified user 
                self.BUSY_WITH_USER = True
                
                # Ask question (in a Thread for speed) and obtain response
                self.speechThread(f"Bonjour {userFirstName}, Comment vous sentez-vous?")
                time.sleep(2)
                data = self.grabSpeechData(3)
                 
                # Analyze response sentiment [what if we log response in database to compile data]
                SentimentState = nlp.sentimentAnalisys(data)
                if SentimentState == "POS":
                    self.SceneSTATE = Scene.positive
                    print(Scene.positive)
                elif SentimentState == "NEU":
                    self.SceneSTATE = Scene.neutral
                    print(Scene.neutral)
                elif SentimentState == "NEG":
                    self.SceneSTATE = Scene.negative
                    print(Scene.negative)
                
            
            #######################
            # SECTION SCENE STATE #
            #######################
            
            if self.SceneSTATE == Scene.positive:
                
                while self.BUSY_WITH_USER:
                    
                    display.positiveMenu(self, userFirstName)
                    self.speechThread(f'Ok {userFirstName}, Comment puis-je vous aider?')
                    time.sleep(2)
                    data = nlp.listen()
                    
                    # Computer response to user
                    userRequest = nlp.analyze(data)
                    print(f"User request subject: {userRequest}")
                    if userRequest == 'heure':
                        display.userRequest_time(self)
                        response = f"Il est présentement {dt.now().strftime('%I:%M')}"
                        nlp.speak(response)
                    elif userRequest == 'meteo':
                        nlp.speak("J'ai compris Information sur la meteo")
                        display.userRequest(self, "Information sur la meteo")
                    elif userRequest == 'meteo futur':
                        nlp.speak("J'ai compris Information sur les previsions")
                        display.userRequest(self, "Information sur les previsions")
                    elif userRequest == 'medicament':
                        medication = '\n'.join(CurrentUSER['Medication'].keys())
                        display.userRequest_medication(self, medication)
                        nlp.speak(f"Vous prenez les médicaments suivants: {medication}")
                        display.userRequest_medication(self, medication)
                    elif userRequest == 'meeting':
                        nlp.speak("J'ai compris Information sur rendez-vous")
                        display.userRequest(self, "Information sur rendez-vous")
                    elif userRequest == 'medecin':
                        nlp.speak("J'ai compris Information sur medecin")
                        display.userRequest(self, "Information sur medecin")
                    elif userRequest == 'contact':
                        nlp.speak("J'ai compris Information sur vos conacts")
                        display.userRequest(self, "Information sur vos conacts")
                    elif userRequest == 'appel':
                        nlp.speak("J'ai compris Information sur un appel")
                        display.userRequest(self, "Information sur un appel")
                    elif userRequest == 'activite':
                        nlp.speak("J'ai compris Information sur vos activiter")
                        display.userRequest(self, "Information sur vos activiter")
                
                    # Repeat or exit
                    self.postResponse()

            elif self.SceneSTATE == Scene.negative or self.SceneSTATE == Scene.neutral:
                
                while self.BUSY_WITH_USER:
                    
                    display.userAideMenu(self)
                    self.speechThread("Afin d'assurer votre bien-être, préférez-vous contacter un proche aidant ou spécialiste de la santé? Parler à l'infirmier ou infirmière en service? Ou Contacter les services d'urgence?")
                    time.sleep(3)
                    data = nlp.listen()
                    
                    # Computer response to user
                    userRequest = nlp.analyze(data)
                    print(f"User request subject: {userRequest}")
                    if userRequest == 'contact proche':
                        nlp.speak("Avec qui aimeriez vous parler?")
                        procheContacts = None  # get list of appropriate contacts
                        display.userAideMenu(self, procheContacts)
                        # return result of choice
                    elif userRequest == 'contact santé':
                        santeContacts = None  # get list of appropriate contacts
                        display.userAideMenu(self, santeContacts)
                        # return result of choice
                    elif userRequest == 'contact urgence':
                        nlp.speak(f"Je contacte immédiatement les serivices d'urgence {userFirstName}!")
                        display.emergency(self, "Je contacte immédiatement les serivices d'urgence {userName}")             
                    
                    # Repeat or exit
                    self.postResponse()
            
            
            # Close loop for testing purposes
            # self.running = False
 
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