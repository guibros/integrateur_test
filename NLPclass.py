from gtts import gTTS
import os
import speech_recognition as speechRecognition
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer


class NLP:
    def __init__(self):
        self.recognizer = speechRecognition.Recognizer()
        self.sia = SentimentIntensityAnalyzer()
        
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


