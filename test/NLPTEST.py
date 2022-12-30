from speech_recognition import Recognizer, Microphone
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PicoTTS import TTS_engine
from tkinter import *
from gtts import gTTS
import os
from threading import Thread

# instanciation des modules vocaux
recognizer = Recognizer()
tts = TTS_engine()
nom = "Guillaume"

#SYSTEME VOX
def speak(text):
    tts1 = gTTS(text=text, lang='fr')
    audio = "audio.mp3"
    tts1.save(audio)
    os.system('mpg321 audio.mp3')

# fonction d'ecoute de langage naturel       
def listening():
    global text
    global nom
    text = ""
    speak(f"Comment aller vous aujourd'hui, {nom} ?")
    with Microphone() as source:
        print("Réglage du bruit ambiant... Patientez...")
        #recognizer.adjust_for_ambient_noise(source)
        print("Vous pouvez parler...")
        try:
            recorded_audio = recognizer.listen(source, 10)
            print("Enregistrement terminé !")
            try:
                print("Reconnaissance du texte...")
                text = recognizer.recognize_google(recorded_audio,language="fr-FR")
                textSay = "Vous avez dit : {}".format(text)
                print(textSay)
                textlist = list(text.split())
                tts.say("commande détecté")
                tts.say(textSay)
                print (textSay)
                return text
            except Exception as ex:
                print(ex)
                print("cant return text")        
        except:
            tts.say("Aucune commande détecté")
            print("no command detected")
            
          #SYSTEME GUI 
# fonction de commande associer au bouton commande vocale
def commande_vocal():
    listening()      
            
#GUI
# initialisation de la fenetre d'affichage principale
f = Tk()
f.protocol("WM_DELETE_WINDOW")
f.title("Console")
f.geometry("200x120")

wf = 300
hf = 200            

# mise en place des frame d'affichage principaux
labelframetitre = LabelFrame(f,text="test", width=wf, height=hf)
labelframetitre.grid(column=0, row=0, columnspan=6)


# element du premier frame d'affichage
l0 = Label(labelframetitre, text = "CONSOLE", font=("Comic", 25))
l0.grid(row= 0, columnspan= 6)

button_commande = Button(labelframetitre, text= "COMMANDE VOCAL",width=16, height=2, command=commande_vocal)
button_commande.grid(row= 1, columnspan= 6)


f.mainloop()
