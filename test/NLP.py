from speech_recognition import Recognizer, Microphone
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PicoTTS import TTS_engine
from tkinter import *
import datetime
from pyowm import OWM
from pyowm.utils.config import get_default_config


text = ""
phrases = [u"quelle heure est-il?",
           u"il est quelle heure?",
           u"quelle heure il est?",
           
           u"quel temps fait-il?",
           u"quel est la température?",
           u"quel est la météo?",
           u"quelles sont les prévision météo?",
           u"quelles sont les prévisions de la météo?",
           u"quelle temperature fait-il?",
           
           u"ouvrir la lumière de l'entrer",
           u"ouvre la lumière de l'entrer",
           u"ouvre la lumière d'entrer",
           u"allumer la lumière de l'entrer",
           u"fermer la lumière de l'entrer",
           u"ferme la lumière de l'entrer",
           u"éteindre la lumière de l'entrer",
           
           u"ouvrir la lumière du salon",
           u"ouvre la lumière du salon",
           u"allumer la lumière du salon",
           u"fermer la lumière du salon",
           u"éteindre la lumière du salon",
           
           u"ouvrir la porte",
           u"ouvre la porte",
           u"ouverture de la porte",
           u"fermer la porte",
           u"ferme la porte",
           u"fermeture de la porte",
           
           u"fermer le système d'alarme",
           u"ferme le système d'alarme",
           u"éteindre le système d'alarme",
           u"arreter le système d'alarme",
           u"désarmer le système d'alarme",
           u"allumer le système d'alarme",
           u"ouvrir le système d'alarme",
           u"ouvre le système d'alarme",
           u"démarrer le système d'alarme",
           u"armer le système d'alarme"
           ]

# instanciation des modules vocaux
recognizer = Recognizer()
tts = TTS_engine()

# initialisation du protocole openmediaweather
config_dict = get_default_config()
config_dict['language'] = 'fr'

owm = OWM('f29f5d4679785c63240b83b42f050dd8', config_dict)
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Montreal,CA')
meteo = observation.weather


#SYSTEME VOX
# fonction d'ecoute de langage naturel       
def listening():
    global text
    text = ""
    with Microphone() as source:
        print("Réglage du bruit ambiant... Patientez...")
        recognizer.adjust_for_ambient_noise(source)
        print("Vous pouvez parler...")
        try:
            recorded_audio = recognizer.listen(source, 10)
            print("Enregistrement terminé !")
            try:
                print("Reconnaissance du texte...")
                text = recognizer.recognize_google(recorded_audio,language="fr-FR")
                print("Vous avez dit : {}".format(text))
                textlist = list(text.split())
                tts.say("Aucune commande détecté")
                tts.say(textlist)
                print (textlist)
                return text
            except Exception as ex:
                print(ex)
                print("cant return text")        
        except:
            tts.say("Aucune commande détecté")
            print("no command detected")

# fonction d'analyse du texte recuperer lors de l'ecoute de langue naturel
def analyze():           
    if text == "":
        pass
    else:
        try:
            (modele, score) = process.extractOne(text, phrases)
            print(modele, score)
            if score >= 89:
                if modele in {"quelle heure est-il?",
                              "il est quelle heure?",
                              "quelle heure il est?"}:
                    clockwork()
                    print("sys_vox heure")
                    
                elif modele in {"quel temps fait-il?",
                                "quel est la température?",
                                "quel est la météo?",
                                "quelle temperature fait-il?",
                                "quelles sont les prévision météo?"}:
                    meteo_vox()
                    print("sys_vox meteo")
                    
                elif modele in {"ouvrir la lumière de l'entrer",
                                "ouvre la lumière de l'entrer",
                                "ouvre la lumière d'entrer",
                                "allumer la lumière de l'entrer"}:
                 
                    compute("allumage lumière de l'entrer")
                    print("sys_vox lumiere entree on")
                    
                elif modele in {"fermer la lumière de l'entrer",
                                "ferme la lumière de l'entrer",
                                "eteindre la lumière de l'entrer"}:
                  
                    compute("fermeture lumière de l'entrer")
                    print("sys_vox lumiere entre off")
                    
                elif modele in {"ouvrir la porte",
                                "ouvre la porte",
                                "ouverture de la porte"}:
                 
                    compute("ouverture porte")
                    print("sys_vox porte ouverture")
                    
                elif modele in {"fermer la porte",
                                "ferme la porte",
                                "fermeture de la porte"}:
                
                    compute("fermeture porte")
                    print("sys_vox porte fermeture")
                    
                elif modele in {"ouvrir la lumière du salon",
                                "ouvre la lumière du salon",
                                "allumer la lumière du salon"}:
                    
                    compute("allumage lumière du salon")
                    print("sys_vox lumiere salon, allumage")
                    
                elif modele in {"fermer la lumière du salon",
                                "ferme la lumière du salon",
                                "eteindre la lumière du salon"}:
                
                    compute("fermeture lumière du salon")
                    print("sys_vox lumiere salon off")
                    
                elif modele in {"ouvrir la porte",
                                "ouvre la porte",
                                "ouverture de la porte"}:
                    
                    compute("ouverture porte")
                    print("sys_vox porte ouverture")
                    
                elif modele in {"fermer la porte",
                                "ferme la porte",
                                "fermeture de la porte"}:
               
                    compute("fermeture porte")
                    print("sys_vox porte fermeture")
                    
                elif modele in {"fermer le système d'alarme",
                                "ferme le système d'alarme",
                                "éteindre le système d'alarme",
                                "arreter le système d'alarme",
                                "désarmer le système d'alarme"}:
                    
                    compute("désactivation systeme d'alarme")
                    print("sys_vox alarm off")
                    
                elif modele in {"allumer le système d'alarme",
                                "ouvrir le système d'alarme",
                                "ouvre le système d'alarme",
                                "démarrer le système d'alarme",
                                "armer le système d'alarme"}:
                    
                    compute("activation systeme d'alarme")
                    print("sys_vox alarm on")
                else:
                    print("cant associate model")
            else:
                no_compute()
                print("score<90")
        except:
            no_compute()
            print("cant extract model")


# fonction de recuperation et vocalisation du temps
def clockwork():
    time = datetime.datetime.now()
    time = time.strftime("%H:%M")
    h,m = time.split(":")
    tts.say(f"il est {h} heures {m} minutes")
    print(f"il est {h} heures {m} minutes")

        
# fonction de vocalisation d'un message   
def compute(msg):
    tts.say(msg)
    print(msg)
    
# fonction de vocalisation d'un message d'erreur        
def no_compute():
    tts.say(u"la commande n'est pas clair, pouvez vous répété")
    print("la commande n'est pas clair, pouvez vous répété")

# fonction de recuperation et vocalisation de la meteo
def meteo_vox():
    txtMeteo = "la Temperature est de " + str(meteo.temperature('celsius')['temp']) + "celsiusse et le temps est " + meteo.detailed_status
    print(txtMeteo)
    tts.say(txtMeteo)

    #SYSTEME GUI 
# fonction de commande associer au bouton commande vocale
def commande_vocal():
    listening()
    analyze()

    

#GUI
# initialisation de la fenetre d'affichage principale
f = Tk()
f.protocol("WM_DELETE_WINDOW")
f.title("Console")
f.geometry("300x600")

wf = 300
hf = 500
# mise en place des frame d'affichage principaux
labelframetitre = LabelFrame(f,text="test", width=wf, height=hf)
labelframetitre.grid(column=0, row=0, columnspan=6)

labelframelumiere1 = LabelFrame(f, text = "LUMIERE ENTREE", font=("Comic", 10), width=wf, height=hf)
labelframelumiere1.grid(column=0, row=3, columnspan=6)

labelframelumiere2 = LabelFrame(f, width=wf, height=hf, text= "LUMIERE SALON", font=("Comic", 10))
labelframelumiere2.grid(column=0, row=4, columnspan=6)

labelframealarme = LabelFrame(f, width=wf, height=hf, text = "ALARME", font=("Comic", 10))
labelframealarme.grid(column=0, row=5, columnspan=6)

# element du premier frame d'affichage
l0 = Label(labelframetitre, text = "CONSOLE", font=("Comic", 25))
l0.grid(row= 0, columnspan= 6)

button_commande = Button(labelframetitre, text= "COMMANDE VOCAL",width=16, height=2, command=commande_vocal)
button_commande.grid(row= 1, columnspan= 6)

# label d'affichage pour l'horloge
affiche_heure = Label(f, font=("Comic", 10, "bold"))
affiche_heure.grid(row= 2, column= 3)

# variable pour la grandeur des boutons
w=8
h=2





f.mainloop()

