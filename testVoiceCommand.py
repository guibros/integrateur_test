from fuzzywuzzy import fuzz
from fuzzywuzzy import process

phrases = [u"quelle heure est-il?",
           u"il est quelle heure?",
           u"quelle heure il est?",
           
           u"quel temps fait-il?",
           u"quel est la température?",
           u"quel est la météo?",
           u"quelles sont les prévision météo?",
           u"quelles sont les prévisions de la météo?",
           u"quelle temperature fait-il?",
           u"dis moi la météo",
           u"dis moi la temperature"
           
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


def analyze(text):           
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