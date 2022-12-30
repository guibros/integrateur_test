# PROJET2
# objet Intelligent :
# mis en relation de protocole reseau mqtt, interface graphique,
# base de donnees mongodb, api meteo, gpio et traitement language naturel



from speech_recognition import Recognizer, Microphone
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PicoTTS import TTS_engine
from PIL import Image as IMG, ImageTk
from time import sleep
import paho.mqtt.client as mqtt
import datetime
import pymongo
from RPiSim import GPIO
from tkinter import *
from project2_mongoconsole import *
from threading import Thread
import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config
import os

# constante du programme
pin_lum1 = 18 # lumiere entree
pin_lum2 = 17 # lumiere salone
pin_alarm = 15 # sys alarme
pin_porte = 13 # porte

etat_lum1 = "OFF"
etat_lum2 = "OFF"
etat_alarm = "DISARMED"
etat_porte = "CLOSE"
running = True
channel_gpio = "eventdevice"

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

# instanciation du module integrant mongodb
mong = MongoConsole("localhost", "evenement", "historique")

# instanciation des modules vocaux
recognizer = Recognizer()
tts = TTS_engine()

# initialisation du protocole mqtt
host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
client_id     = "telephone"
user_name     = "popocoagul"
password      = "Popo21popo21ecole"

client = mqtt.Client(client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)
client.connect (host, port)


# initialisation du protocole gpio
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_lum1,GPIO.MODE_OUT, initial=GPIO.LOW) #lumiere 1
GPIO.setup(pin_lum2,GPIO.MODE_OUT, initial=GPIO.LOW) #lumiere 2
GPIO.setup(pin_alarm,GPIO.MODE_OUT, initial=GPIO.LOW) #alarme 
GPIO.setup(pin_porte,GPIO.MODE_OUT, initial=GPIO.LOW) #alarme 



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
                    publicate(channel_gpio, "lumiere1_ON")
                    mong.push("lumiere1", "ON")
                    compute("allumage lumière de l'entrer")
                    print("sys_vox lumiere entree on")
                    
                elif modele in {"fermer la lumière de l'entrer",
                                "ferme la lumière de l'entrer",
                                "eteindre la lumière de l'entrer"}:
                    publicate(channel_gpio,"lumiere1_OFF")
                    mong.push("lumiere1","OFF")
                    compute("fermeture lumière de l'entrer")
                    print("sys_vox lumiere entre off")
                    
                elif modele in {"ouvrir la porte",
                                "ouvre la porte",
                                "ouverture de la porte"}:
                    publicate(channel_gpio, "porte_ON")
                    mong.push("porte", "OUVERTURE")
                    compute("ouverture porte")
                    print("sys_vox porte ouverture")
                    
                elif modele in {"fermer la porte",
                                "ferme la porte",
                                "fermeture de la porte"}:
                    publicate(channel_gpio, "porte_OFF")
                    mong.push("porte", "FERMETURE")
                    compute("fermeture porte")
                    print("sys_vox porte fermeture")
                    
                elif modele in {"ouvrir la lumière du salon",
                                "ouvre la lumière du salon",
                                "allumer la lumière du salon"}:
                    publicate(channel_gpio,"lumiere2_ON")
                    mong.push("lumiere2", "ON")
                    compute("allumage lumière du salon")
                    print("sys_vox lumiere salon, allumage")
                    
                elif modele in {"fermer la lumière du salon",
                                "ferme la lumière du salon",
                                "eteindre la lumière du salon"}:
                    publicate(channel_gpio,"lumiere2_OFF")
                    mong.push("lumiere2", "OFF")
                    compute("fermeture lumière du salon")
                    print("sys_vox lumiere salon off")
                    
                elif modele in {"ouvrir la porte",
                                "ouvre la porte",
                                "ouverture de la porte"}:
                    publicate(channel_gpio, "porte_ON")
                    mong.push("porte", "OUVERTURE")
                    compute("ouverture porte")
                    print("sys_vox porte ouverture")
                    
                elif modele in {"fermer la porte",
                                "ferme la porte",
                                "fermeture de la porte"}:
                    publicate(channel_gpio, "porte_OFF")
                    mong.push("porte", "FERMETURE")
                    compute("fermeture porte")
                    print("sys_vox porte fermeture")
                    
                elif modele in {"fermer le système d'alarme",
                                "ferme le système d'alarme",
                                "éteindre le système d'alarme",
                                "arreter le système d'alarme",
                                "désarmer le système d'alarme"}:
                    publicate(channel_gpio,"alarme_OFF")
                    mong.push("alarme","DISARMED")
                    compute("désactivation systeme d'alarme")
                    print("sys_vox alarm off")
                    
                elif modele in {"allumer le système d'alarme",
                                "ouvrir le système d'alarme",
                                "ouvre le système d'alarme",
                                "démarrer le système d'alarme",
                                "armer le système d'alarme"}:
                    publicate(channel_gpio,"alarme_ON")
                    mong.push("alarme","ARMED")
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

# fonction de recuperation et vocalisation de la meteo
def meteo_vox():
    txtMeteo = "la Temperature est de " + str(meteo.temperature('celsius')['temp']) + "celsiusse et le temps est " + meteo.detailed_status
    print(txtMeteo)
    tts.say(txtMeteo)
    
# fonction de vocalisation d'un message   
def compute(msg):
    tts.say(msg)
    print(msg)
    
# fonction de vocalisation d'un message d'erreur        
def no_compute():
    tts.say(u"la commande n'est pas clair, pouvez vous répété")
    print("la commande n'est pas clair, pouvez vous répété")




#SYSTEME MQTT
# fonction de recuperation et d'association de message publier sur mqtt
def on_message(client, userdata, message):
    print("on_msg received message: " ,str(message.payload.decode("utf-8")))
    
    event=str(message.payload.decode("utf-8"))
    global etat_lum1
    global etat_lum2 
    global etat_alarm
    global etat_porte
    # reception et declenchement des pin du gpio par le systeme GUI ou VOX 
    if "lumiere1_ON" in event:
        print("mqtt_onmsg_checked  lumiere1 on!")   
        GPIO.output(pin_lum1, GPIO.HIGH)
    elif "lumiere1_OFF" in event:
        print("mqtt_onmsg_checked  lumiere1 off!")        
        GPIO.output(pin_lum1, GPIO.LOW) 
    elif "lumiere2_ON" in event:
        print("mqtt_onmsg_checked  lumiere 2 on!")        
        GPIO.output(pin_lum2, GPIO.HIGH)
    elif "lumiere2_OFF" in event:
        print("mqtt_onmsg_checked  lumiere 2 off!")        
        GPIO.output(pin_lum2, GPIO.LOW)
    elif "alarme_ON" in event:
        print("mqtt_onmsg_checked  alarme on!")        
        GPIO.output(pin_alarm, GPIO.HIGH)
    elif "alarme_OFF" in event:
        print("mqtt_onmsg_checked  alarme off!")        
        GPIO.output(pin_alarm, GPIO.LOW)
    elif "porte_ON" in event:
        print("mqtt_onmsg_checked  porte on!")        
        GPIO.output(pin_porte, GPIO.HIGH)
    elif "porte_OFF" in event:
        print("mqtt_onmsg_checked  porte off!")        
        GPIO.output(pin_porte, GPIO.LOW)
        
    # reception et declenchement de l'affichage declencher par gpio
    elif "lumière d'entrer on"in event:
        etat_lum1 = "ON"
        l1_etat.config(text= etat_lum1, fg = "green")
        print("mqtt_onmsg_checked pin_lum1-on")
    elif "lumière d'entrer off"in event:
        etat_lum1 = "OFF"
        l1_etat.config(text= etat_lum1, fg = "red")
        print("mqtt_onmsg_checked pin_lum1-off")
    elif "lumière du salon on"in event:
        etat_lum2 = "ON"
        l2_etat.config(text= etat_lum2, fg = "green")
        print("mqtt_onmsg_checked pin_lum2-on")
    elif "lumière du salon off"in event:
        etat_lum2 = "OFF"
        l2_etat.config(text= etat_lum2, fg = "red")
        print("mqtt_onmsg_checked pin_lum2-off")
    elif "alarme on"in event:
        etat_alarm = "ARMED"
        l3_etat.config(text= etat_alarm, fg = "red")
        print("mqtt_onmsg_checked pin_alarm-on")
    elif "alarme off"in event:
        etat_alarm = "DISARMED"
        l3_etat.config(text= etat_alarm, fg = "green")
        print("mqtt_onmsg_checked pin_alarm-off")
    elif "porte on"in event:
        etat_porte = "OPEN"
        porte_etat.config(text= etat_porte)
        print("mqtt_onmsg_checked porte on")
    elif "porte off"in event:
        etat_porte = "CLOSE"
        porte_etat.config(text= etat_porte)
        print("mqtt_onmsg_checked porte off")
        

# fonction de publication de message sur mqtt
def publicate(channel, msg):
    client.publish(channel, msg)
    print(f"publicate: {msg} on {channel}")

# fonction d'ecoute et de publication du gpio sur mqtt   
def gpio_listen(pin, channel, msg):
    msg_original = msg
    print(f"gpio_listen {pin} start")
    while running:
        gpio_read_1 = GPIO.input(pin)
        sleep(0.2)
        gpio_read_2 = GPIO.input(pin)
        if gpio_read_1 != gpio_read_2:
            print(f"gpio_listen {pin} read change")
            if GPIO.input(pin):
                print("gpio_on")
                msgvox = f"{msg}, ouverte"
                msg = str(msg+" on")
                publicate(channel, msg)
                sleep(1.4)
                tts.say(msgvox)
            if not GPIO.input(pin):
                print("gpio_OFF")
                msgvox = f"{msg}, fermer"
                msg = str(msg+" off")
                publicate(channel, msg)
                sleep(1.4)
                tts.say(msgvox)
            msg = msg_original
        #print(etat_lum1)   
    print(f"gpio_listen {pin} out")




#SYSTEME GUI 
# fonction de commande associer au bouton commande vocale
def commande_vocal():
    listening()
    analyze()

# fonction de commande associer au bouton lumiere1 on
def lumiere1_ON():
    mong.push("lumiere1", "ON")
    publicate(channel_gpio, "lumiere1_ON")
    compute("allumage lumière de l'entrer")

# fonction de commande associer au bouton lumiere1 off
def lumiere1_OFF():
    mong.push("lumiere1","OFF")
    publicate(channel_gpio, "lumiere1_OFF")
    compute("fermeture lumière de l'entrer")

# fonction de commande associer au bouton lumiere2 on
def lumiere2_ON():
    mong.push("lumiere2", "ON")
    publicate(channel_gpio, "lumiere2_ON")
    compute("allumage lumière du salon")


# fonction de commande associer au bouton lumiere2 off
def lumiere2_OFF():
    mong.push("lumiere2","OFF")
    publicate(channel_gpio, "lumiere2_OFF")
    compute("fermeture lumière du salon")

# fonction de commande associer au bouton alarme armed
def alarme_ON():
    mong.push("alarme","ARMED")
    publicate(channel_gpio, "alarme_ON")
    compute("activation système d'alarme")

# fonction de commande associer au bouton alarme disarmed
def alarme_OFF():
    mong.push("alarme","DISARMED")
    publicate(channel_gpio, "alarme_OFF")
    compute("désactivation système d'alarme")
    
# fonction de commande associer au bouton porte open   
def porte_ON():
    publicate(channel_gpio, "porte_ON")
    mong.push("porte", "OUVERTURE")
    compute("ouverture porte")
                    
# fonction de commande associer au bouton porte close                    
def porte_OFF():
    mong.push("porte", "FERMETURE")
    publicate(channel_gpio, "porte_OFF")
    compute("fermeture porte")

# fonction de commande associer au bouton historique et affichage du log mongodb
def historique():
    global resultat
    global f1
    f1 = Tk()
    f1.title("Historique")
    f1.geometry("400x450")

    resultat = Text(f1)
    resultat.config(width=60, height=23)
    resultat.insert(INSERT, "")
    resultat.grid(row=2, column=0, columnspan=4)

    bouton = Button(f1, text="Quitter", command=f1.destroy)
    bouton.grid(row=10, column=2)
    
    bouton1 = Button(f1, text="Actualiser", command=actualiser)
    bouton1.grid(row=10, column=0)
    resultat.insert(INSERT, mon.retrieve(20))
    
    f1.mainloop()

# fonction de commande associer au bouton actualiser de la fenetre historique
# et actualisation du log mongodb   
def actualiser():
    resultat.delete("1.0","end")
    resultat.insert(INSERT, mon.retrieve(20))

# fonction de commande associer au bouton quitter et fermeture(x) de la fenetre
def destroy():
    global running
    print("Quitter proprement")
    running = False
    client.loop_stop()
    client.disconnect()
    f.destroy()
    try:
        f1.destroy()
    except:
        pass

#bloc-config de la fonction affichage horloge 
def clockTime():
    now = datetime.datetime.now()
    t = now.strftime(" %A  %-d %B \n %H:%M:%S")
    affiche_heure.config(text = t)
    affiche_heure.after(1000, clockTime)

#bloc-config de la fonction affichage meteo    
def getMeteo():
    global txtMeteo
    imageMeteo = f"http://openweathermap.org/img/wn/{meteo.weather_icon_name}.png"
    response = requests.get(imageMeteo)
    file = open("meteo_image.png", "wb")
    file.write(response.content)
    file.close()
    img = ImageTk.PhotoImage(IMG.open("meteo_image.png"))
    affiche_image.configure(image=img)
    affiche_image.image = img
    txtMeteo = "Temperature: " + str(meteo.temperature('celsius')['temp']) + " celsius" + "\n" + meteo.detailed_status
    affiche_meteo.config(text = txtMeteo)
    affiche_meteo.after(5000, getMeteo)   
    return txtMeteo



# activation du protocole mqtt
client.loop_start()

client.subscribe(channel_gpio)
client.on_message=on_message

# activation du des thread parallele pour l<ecoute des pins du gpio
gpio_thread1 = Thread(target = gpio_listen, args=(pin_lum1, channel_gpio, "lumière d'entrer"))
gpio_thread2 = Thread(target = gpio_listen, args=(pin_lum2, channel_gpio, "lumière du salon"))
gpio_thread3 = Thread(target = gpio_listen, args=(pin_alarm, channel_gpio, "alarme"))
gpio_thread4 = Thread(target = gpio_listen, args=(pin_porte, channel_gpio, "porte"))
gpio_thread1.start()
gpio_thread2.start()
gpio_thread3.start()
gpio_thread4.start()



#GUI
# initialisation de la fenetre d'affichage principale
f = Tk()
f.protocol("WM_DELETE_WINDOW", destroy)
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

# element du deuxieme frame d'affichage
button_lum1_on = Button(labelframelumiere1, text= "ON",width=w, height=h, command=lumiere1_ON)
button_lum1_on.grid(row= 0, column= 0)

button_lum1_off = Button(labelframelumiere1, text= "OFF",width=w, height=h, command=lumiere1_OFF)
button_lum1_off.grid(row= 0, column= 1)

frame_etat_lumiere1 = LabelFrame(labelframelumiere1 ,text="ETAT", width=1, height=1)
frame_etat_lumiere1.grid(row=0, column=2)

l1_etat = Label(frame_etat_lumiere1, text = etat_lum1, font=("Comic", 20),fg="red")
l1_etat.grid(row= 0, column= 0)

# element du troisieme frame d'affichage
button_lum2_on = Button(labelframelumiere2, text= "ON",width=w,height=h, command=lumiere2_ON)
button_lum2_on.grid(row= 0, column= 0)

button_lum2_off = Button(labelframelumiere2, text= "OFF",width=w,height=h, command=lumiere2_OFF)
button_lum2_off.grid(row= 0, column= 1)

frame_etat_lumiere2 = LabelFrame(labelframelumiere2 ,text="ETAT", width=1, height=1)
frame_etat_lumiere2.grid(row=0, column=2)

l2_etat = Label(frame_etat_lumiere2, text = etat_lum2, font=("Comic", 20),fg="red")
l2_etat.grid(row= 0, column= 3)

# element du quatrieme frame d'affichage
button_alarm_on = Button(labelframealarme, text= "ARMED",width=w, height=h, command=alarme_ON)
button_alarm_on.grid(row= 0, column= 0)

button_alarm_off = Button(labelframealarme, text= "DISARMED",width=w, height=h, command=alarme_OFF)
button_alarm_off.grid(row= 0, column= 1)

frame_etat_alarm = LabelFrame(labelframealarme ,text="ETAT", width=1, height=200)
frame_etat_alarm.grid(row=0, column=2)

l3_etat = Label(frame_etat_alarm, text = etat_alarm, font=("Comic", 15), fg="green")
l3_etat.grid(row= 0, column= 3)

# label d'affichage pour la meteo
affiche_meteo = Label(f, text = "meteo", font=("Comic", 12, "bold"))
affiche_meteo.grid(row= 6, column=3, sticky= W)

img = ImageTk.PhotoImage(IMG.open("meteo_image.png"))
affiche_image = Label(f, image=img)
affiche_image.grid(row= 7, column=3)



frame_porte = LabelFrame(f, text="PORTE", width=1, height=2)
frame_porte.grid(row= 8, columnspan= 6)



button_porte_on = Button(frame_porte, text= "OPEN",width=w, height=h, command=porte_ON)
button_porte_on.grid(row= 0, column= 0)

button_porte_off = Button(frame_porte, text= "CLOSE",width=w, height=h, command=porte_OFF)
button_porte_off.grid(row= 0, column= 1)


frame_etat_porte = LabelFrame(frame_porte, text="ETAT", width=1, height=2)
frame_etat_porte.grid(row= 0, column= 2)

porte_etat = Label(frame_etat_porte, text = etat_porte, font=("Comic", 15))
porte_etat.grid(row= 0, column= 0)


button_historique = Button(f, text= "AFFICHER HISTORIQUE", command = historique)
button_historique.grid(row= 9, columnspan= 6)

bouton = Button(f, text="Quitter", command=destroy)
bouton.grid(row=10, columnspan=6)


# initialisation des fonction d'affichage de la meteo et de l'heure
getMeteo()
clockTime()



f.mainloop()

