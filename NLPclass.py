from gtts import gTTS
import os
import speech_recognition as speechRecognition
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer


class NLP:
    def __init__(self):
        self.recognizer = speechRecognition.Recognizer()
        self.sia = SentimentIntensityAnalyzer()
        self.phrases = [ #heure
                        u"quelle heure est-il?",
                        u"Quelle heure est-il ?",
                        u"Donne-moi l'heure",
                        u"Quelle est l'heure actuelle ?",
                        u"Dis-moi l'heure",
                        u"Donne-moi l'heure actuelle"
                        u"il est quelle heure?",
                        u"quelle heure il est?",
                        u"Peux-tu me dire l'heure s'il te plaît?",
                        u"Pouvez-vous me dire quelle heure il est?",
                        u"Je voudrais savoir l'heure, s'il vous plaît.",
                        u"Est-ce que tu sais l'heure qu'il est?",
                        u"Peux-tu me donner l'heure?",
                        u"Pourrais-tu me dire l'heure, s'il te plaît?",
                        u"Est-ce que tu pourrais me donner l'heure actuelle?",
                        u"Quelle est l'heure exacte, s'il te plaît?",
                        u"Je voudrais savoir l'heure précise, si cela ne te dérange pas.",
                        u"Peux-tu me dire quelle heure il est en ce moment?",

                        #meteo
                        u"quel temps fait-il?",
                        u"quelle temperature fait-il?",
                        u"quelle est la température?",
                        u"quelle est la température aujourd'hui?",
                        u"quelle est la température ressentie?",
                        u"quelle est la température dehors?",
                        u"quelle est la température actuelle?",
                        u"quelle météo fait-il?",
                        u"quelle est la météo?",
                        u"quelle est la météo dehors?",
                        u"quelle est la météo actuelle?",
                        u"quelle est la météo aujourd'hui?",
                        u"quelles sont les prévisions météo?",
                        u"y a-t-il des prévisions de pluie pour aujourd'hui?",
                        u"y a-t-il de la pluie pour aujourd'hui?",
                        u"y a-t-il de la pluie?",
                        u"est-ce qu'il va pleuvoir?",
                        u"est-ce qu'il va pleuvoir aujourd'hui?",
                        u"Est-ce qu'il pleut?",
                        u"Est-ce qu'il pleut aujourd'hui?",
                        u"Est-ce qu'il pleut actuellement?",
                        u"Fera-t-il soleil aujourd'hui",
                        u"y a-t-il du soleil pour aujourd'hui?",
                        u"y a-t-il du soleil?",
                        u"est-ce qu'il va faire soleil?",
                        u"est-ce qu'il va faire soleil aujourd'hui?",
                        u"Est-ce qu'il fait soleil?",
                        u"Est-ce que ce sera nuageux aujourd'hui",
                        u"y aura-t-il des nuages aujourd'hui?",
                        u"fera-t-il nuageux aujourd'hui?",
                        u"Est-ce qu'il y a des nuages?",
                        u"Est-ce qu'il y a des nuages aujourd'hui?",
                        
                        #meteo futur
                        u"quelle sera la météo demain matin?",
                        u"quelle sera la météo pour les prochains jours?",
                        u"quelle sera la température demain matin?",
                        u"quelle sera la température pour les prochains jours?",
                        u"y a-t-il des prévisions de pluie dans les prochain jours?",
                        u"quelle sera la météo pour les prochains jours?",
                        u"comment sera la météo futures?",

                        #medicaments
                        u"Quelles sont les médicaments que je dois prendre?"
                        u"Quelles sont mes médicaments?"
                        u"C'est quoi mes médicaments?"
                        u"Est-ce que j'ai des médicaments?"
                        u"Quand je dois prendre mes médicaments?"
                        u"Est-ce que j'ai pris mes médicaments?"
                        u"Est-ce que j'ai une prescription?"
                        u"Quel est ma prescription?"
                        u"C'est quoi ma prescription?"
                        u"Est-ce que j'ai pris mes médicaments ce matin?"
                        u"Est-ce que je dois prendre mes médicaments avant ou après les repas?"
                        u"A quelle heure dois-je prendre mes médicaments?"
                        u"Combien de comprimés dois-je prendre?"
                        u"Combien de temps dois-je prendre ce médicament?"
                        u"Dois-je prendre des médicament?"
                        u"Quel médicament dois-je prendre?",
                        u"Donne-moi le nom de mon médicament.",
                        u"Dis-moi quel médicament je dois prendre.",
                        u"Quel est le nom de mon médicament?",
                        u"Pouvez-vous me dire quel médicament je dois prendre?",
                        u"Peux-tu me donner le nom de mon médicament?",
                        u"Je voudrais savoir quel médicament je dois prendre, s'il te plaît.",
                        u"Est-ce que tu sais quel médicament je dois prendre?",

                        #rendez-vous
                        u"quels sont mes rendez-vous?",
                        u"ai-je des rendez-vous",
                        u"a quel date j'ai des rendez-vous?"
                        u"a quelle heures mon rendez-vous?",
                        u"quel est mon agenda",
                        u"quand est mon prochain rendez vous",
                        u"quand es-ce que j'ai des rendez vous",
                        u"a quel moment j'ai un rendez vous",
                        u"Quel est mon horaire",
                        u"quels sont mes meeting",
                        u"ai-je des meeting",
                        u"a quelle heures mon meeting?",
                        u"Quel est mon prochain rendez-vous?",
                        u"Donne-moi la liste de mes rendez-vous.",
                        u"Dis-moi quand est mon prochain rendez-vous.",
                        u"Quel est le jour de mon prochain rendez-vous?",
                        u"Pouvez-vous me dire quand est mon prochain rendez-vous?",
                        u"Peux-tu me donner la liste de mes rendez-vous?",
                        u"Je voudrais savoir quel est mon prochain rendez-vous, s'il te plaît.",
                        u"Est-ce que tu sais quand est mon prochain rendez-vous?",
                        u"Peux-tu me dire à quel jour et à quelle heure j'ai mon prochain rendez-vous?",

                        #Medecin
                        u"Quel est mon médecin",
                        u"comment contacter mon médecin",
                        u"quel est le contact de mon médecin",
                        u"je veux voir mon médecin",
                        u"je veux consulter mon médecin",
                        u"comment contacter mon médecin",
                        u"Quel est mon docteur",
                        u"comment contacter mon docteur",
                        u"quel est le contact de mon docteur",
                        u"je veux voir mon docteur",
                        u"je veux consulter mon docteur",
                        u"comment contacter mon docteur",
                        u"Je voudrais prendre rendez-vous chez le médecin.",
                        u"Donne-moi les horaires de consultation du médecin.",
                        u"Dis-moi comment prendre rendez-vous chez le médecin.",
                        u"Quel est l'adresse du cabinet du médecin?",
                        u"Je voudrais prendre rendez-vous avec le médecin, s'il te plaît.",
                        u"Est-ce que tu sais comment prendre rendez-vous chez le médecin?",
                        u"Peux-tu me donner les horaires de consultation du médecin?",
                        u"Je voudrais savoir à quel moment je peux prendre rendez-vous chez le médecin.",
                        u"Pouvez-vous me dire comment prendre rendez-vous avec le médecin?",

                        #Contact
                        u"Quels est ma liste de contact",
                        u"quels sont mes contacts",
                        u"Comment puis-je acceder a mes contacts",
                        u"je veux voir mes contacts",
                        u"je veux acceder a mes contacts",
                        u"ou sont mes contacts",
                        u"Donne-moi la liste de mes contacts.",
                        u"Dis-moi comment accéder à mes contacts.",
                        
                        #appel
                        u"appel le centre",
                        u"appelle",
                        u"appeler",
                        u"telephoner",
                        u"telephone",
                        u"rejoins",
                        u"rejoindre",

                        #activités
                        u"quels sont mes activités?",
                        u"quels sont les activités?",
                        u"quand y a-t-il des activités",
                        u"y a-t-il des activités",
                        u"ai-je des activités",
                        u"a quel date j'ai des activités?"
                        u"a quelle heures mon activités?",
                        u"quel est mon activités",
                        u"quand est ma prochaine activités",
                        u"quand es-ce que j'ai des activités",
                        u"a quel moment j'ai une activités"
                        ]
        
    def speak(self, text):
        tts = gTTS(text=text, lang='fr', tld='ca')
        audioFile = "audio.mp3"
        tts.save(audioFile)
        os.system('mpg321 audio.mp3')
        
    def listen(self):
        with speechRecognition.Microphone() as source:
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            print("say somthing")
            audioData = self.recognizer.listen(source) 
            print("try something2323")
            try:
                print("try something")
                data = self.recognizer.recognize_google(audioData, language="fr-FR")
                print(data)
                #self.speak(data)
                return data
            except Exception as ex:
                print(ex)
                print("cant return text")    
                self.speak("Je comprend mal.")
                return ""      
                
    def sentimentAnalisys(self, data):
        score = self.sia.polarity_scores(data)
        # print(score)
        print(score['compound'])
        if score['compound'] >= 0.05:
            return "POS"
        elif score['compound'] > -0.05 and score['compound'] < 0.05:
            return "NEU"
        elif score['compound'] <= -0.05:
            return "NEG"

    def analyzeVariable(self, text, keyword):
        if keyword in text:
            return True
        else:
            return False

    def analyze(self, text):           
        if text == "":
            pass
        else:
            try:
                (modele, score) = process.extractOne(text, self.phrases)
                print(modele, score)
                if score >= 89:
                    if modele in {  "Quelle heure est-il ?",
                                    "Donne-moi l'heure",
                                    "Quelle est l'heure actuelle ?",
                                    "Dis-moi l'heure",
                                    "Donne-moi l'heure actuelle"
                                    "il est quelle heure?",
                                    "quelle heure il est?",
                                    "Peux-tu me dire l'heure s'il te plaît?",
                                    "Pouvez-vous me dire quelle heure il est?",
                                    "Je voudrais savoir l'heure, s'il vous plaît.",
                                    "Est-ce que tu sais l'heure qu'il est?",
                                    "Peux-tu me donner l'heure?",
                                    "Pourrais-tu me dire l'heure, s'il te plaît?",
                                    "Est-ce que tu pourrais me donner l'heure actuelle?",
                                    "Quelle est l'heure exacte, s'il te plaît?",
                                    "Je voudrais savoir l'heure précise, si cela ne te dérange pas.",
                                    "Peux-tu me dire quelle heure il est en ce moment?"
                                    }:
                        print("heure")
                        return "heure"
                        
                    elif modele in {"quel temps fait-il?",
                                    "quelle temperature fait-il?",
                                    "quelle est la température?",
                                    "quelle est la température aujourd'hui?",
                                    "quelle est la température ressentie?",
                                    "quelle est la température dehors?",
                                    "quelle est la température actuelle?",
                                    "quelle météo fait-il?",
                                    "quelle est la météo?",
                                    "quelle est la météo dehors?",
                                    "quelle est la météo actuelle?",
                                    "quelle est la météo aujourd'hui?",
                                    "quelles sont les prévisions météo?",
                                    "y a-t-il des prévisions de pluie pour aujourd'hui?",
                                    "y a-t-il de la pluie pour aujourd'hui?",
                                    "y a-t-il de la pluie?",
                                    "est-ce qu'il va pleuvoir?",
                                    "est-ce qu'il va pleuvoir aujourd'hui?",
                                    "Est-ce qu'il pleut?",
                                    "Est-ce qu'il pleut aujourd'hui?",
                                    "Est-ce qu'il pleut actuellement?",
                                    "Fera-t-il soleil aujourd'hui",
                                    "y a-t-il du soleil pour aujourd'hui?",
                                    "y a-t-il du soleil?",
                                    "est-ce qu'il va faire soleil?",
                                    "est-ce qu'il va faire soleil aujourd'hui?",
                                    "Est-ce qu'il fait soleil?",
                                    "Est-ce que ce sera nuageux aujourd'hui",
                                    "y aura-t-il des nuages aujourd'hui?",
                                    "fera-t-il nuageux aujourd'hui?",
                                    "Est-ce qu'il y a des nuages?",
                                    "Est-ce qu'il y a des nuages aujourd'hui?"
                                    }:
                        print("meteo")
                        return "meteo"
                        
                    elif modele in {"quelle sera la météo demain matin?",
                                    "quelle sera la météo pour les prochains jours?",
                                    "quelle sera la température demain matin?",
                                    "quelle sera la température pour les prochains jours?",
                                    "y a-t-il des prévisions de pluie dans les prochain jours?",
                                    "quelle sera la météo pour les prochains jours?",
                                    "comment sera la météo futures?"
                                    }:
                        print("météo futur")
                        return "meteo futur"
                        
                    elif modele in {"Quelles sont les médicaments que je dois prendre?",
                                    "Quelles sont mes médicaments?",
                                    "C'est quoi mes médicaments?",
                                    "Est-ce que j'ai des médicaments?",
                                    "Quand je dois prendre mes médicaments?",
                                    "Est-ce que j'ai pris mes médicaments?",
                                    "Est-ce que j'ai une prescription?",
                                    "Quel est ma prescription?",
                                    "C'est quoi ma prescription?",
                                    "Est-ce que j'ai pris mes médicaments ce matin?",
                                    "Est-ce que je dois prendre mes médicaments avant ou après les repas?",
                                    "A quelle heure dois-je prendre mes médicaments?",
                                    "Combien de comprimés dois-je prendre?",
                                    "Combien de temps dois-je prendre ce médicament?",
                                    "Dois-je prendre des médicament?",
                                    "Quel médicament dois-je prendre?",
                                    "Donne-moi le nom de mon médicament.",
                                    "Dis-moi quel médicament je dois prendre.",
                                    "Quel est le nom de mon médicament?",
                                    "Pouvez-vous me dire quel médicament je dois prendre?",
                                    "Peux-tu me donner le nom de mon médicament?",
                                    "Je voudrais savoir quel médicament je dois prendre, s'il te plaît.",
                                    "Est-ce que tu sais quel médicament je dois prendre?"
                                    }:
                        print("medicament")
                        return "medicament"
                        
                    elif modele in {"quels sont mes rendez-vous?",
                                    "ai-je des rendez-vous",
                                    "a quel date j'ai des rendez-vous?"
                                    "a quelle heures mon rendez-vous?",
                                    "quel est mon agenda",
                                    "quand est mon prochain rendez vous",
                                    "quand es-ce que j'ai des rendez vous",
                                    "a quel moment j'ai un rendez vous",
                                    "Quel est mon horaire",
                                    "quels sont mes meeting",
                                    "ai-je des meeting",
                                    "a quelle heures mon meeting?",
                                    "Quel est mon prochain rendez-vous?",
                                    "Donne-moi la liste de mes rendez-vous.",
                                    "Dis-moi quand est mon prochain rendez-vous.",
                                    "Quel est le jour de mon prochain rendez-vous?",
                                    "Pouvez-vous me dire quand est mon prochain rendez-vous?",
                                    "Peux-tu me donner la liste de mes rendez-vous?",
                                    "Je voudrais savoir quel est mon prochain rendez-vous, s'il te plaît.",
                                    "Est-ce que tu sais quand est mon prochain rendez-vous?",
                                    "Peux-tu me dire à quel jour et à quelle heure j'ai mon prochain rendez-vous?"
                                    }:
                        print("meeting")
                        return "meeting"
                        
                    elif modele in {"Quel est mon médecin",
                                    "comment contacter mon médecin",
                                    "quel est le contact de mon médecin",
                                    "je veux voir mon médecin",
                                    "je veux consulter mon médecin",
                                    "comment contacter mon médecin",
                                    "Quel est mon docteur",
                                    "comment contacter mon docteur",
                                    "quel est le contact de mon docteur",
                                    "je veux voir mon docteur",
                                    "je veux consulter mon docteur",
                                    "comment contacter mon docteur",
                                    "Je voudrais prendre rendez-vous chez le médecin.",
                                    "Donne-moi les horaires de consultation du médecin.",
                                    "Dis-moi comment prendre rendez-vous chez le médecin.",
                                    "Quel est l'adresse du cabinet du médecin?",
                                    "Je voudrais prendre rendez-vous avec le médecin, s'il te plaît.",
                                    "Est-ce que tu sais comment prendre rendez-vous chez le médecin?",
                                    "Peux-tu me donner les horaires de consultation du médecin?",
                                    "Je voudrais savoir à quel moment je peux prendre rendez-vous chez le médecin.",
                                    "Pouvez-vous me dire comment prendre rendez-vous avec le médecin?"
                                    }:
                        print("medecin")
                        return "medecin"
                        
                    elif modele in {"Quels est ma liste de contact",
                                    "quels sont mes contacts",
                                    "Comment puis-je acceder a mes contacts",
                                    "je veux voir mes contacts",
                                    "je veux acceder a mes contacts",
                                    "ou sont mes contacts",
                                    "Donne-moi la liste de mes contacts.",
                                    "Dis-moi comment accéder à mes contacts."
                                    }:
                        print("contact")
                        return "contact"
                    
                    elif modele in {"appel le centre",
                                    "appelle",
                                    "appeler",
                                    "telephoner",
                                    "telephone",
                                    "rejoins",
                                    "rejoindre"
                                    }:
                        print("appel")
                        return "appel"                    
                        
                    elif modele in {"quels sont mes activités?",
                                    "quels sont les activités?",
                                    "quand y a-t-il des activités",
                                    "y a-t-il des activités",
                                    "ai-je des activités",
                                    "a quel date j'ai des activités?"
                                    "a quelle heures mon activités?",
                                    "quel est mon activités",
                                    "quand est ma prochaine activités",
                                    "quand es-ce que j'ai des activités",
                                    "a quel moment j'ai une activités"
                                    }:
                        print("activité")
                        return "activité"
                    else:
                        print("cant associate model")
                        try:
                            self.motClef(text)
                        except:
                            self.speak("Commande non-associé.")
                            print("cant associate model")
                            return "no model"
                else:
                    print("score<90")
                    try:
                        return self.motClef(text)
                    except:
                        self.speak("Commande incomprise.")
                        print("score<90")
                        return "model underscore"
            except:
                print("cant extract model")    
                try:
                    return self.motClef(text)
                except:
                    self.speak("analyse incomplète")
                    print("cant extract model")    

    def motClef(self, text):
        if "heure" in text:
            print("heure")
            return "heure"
        elif "météo" in text:
            print("meteo")
            return "meteo"        
        elif "température" in text:
            print("meteo")
            return "meteo" 
        elif "médicament" in text:
            print("medicament")
            return "medicament" 
        elif "médicaments" in text:
            print("medicament")
            return "medicament" 
        elif "prescription" in text:
            print("medicament")
            return "medicament" 
        elif "prescriptions" in text:
            print("medicament")
            return "medicament" 
        elif "rendez-vous" in text:
            print("meeting")
            return "meeting" 
        elif "meeting" in text:
            print("meeting")
            return "meeting" 
        elif "médecin" in text:
            print("medecin")
            return "medecin" 
        elif "médecins" in text:
            print("medecin")
            return "medecin" 
        elif "docteur" in text:
            print("medecin")
            return "medecin" 
        elif "docteurs" in text:
            print("medecin")
            return "medecin" 
        elif "contacts" in text:
            print("contact")
            return "contact" 
        elif "contact" in text:
            print("contact")
            return "contact" 
        elif "contacter" in text:
            print("contact")
            return "contact" 
        elif "contacté" in text:
            print("contact")
            return "contact" 
        elif "appeller" in text:
            print("appel")
            return "appel" 
        elif "appellé" in text:
            print("appel")
            return "appel" 
        elif "appelle" in text:
            print("appel")
            return "appel"  
        elif "appel" in text:
            print("appel")
            return "appel"  
        elif "téléphone" in text:
            print("appel")
            return "appel" 
        elif "téléphoner" in text:
            print("appel")
            return "appel" 
        elif "téléphoné" in text:
            print("appel")
            return "appel" 
        elif "iphone" in text:
            print("appel")
            return "appel" 
        elif "activité" in text:
            print("activite")
            return "activite" 
        elif "activités" in text:
            print("activite")
            return "activite" 
        
   