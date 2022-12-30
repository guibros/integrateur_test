# from gtts import gTTS
# import os
# import playsound
# import speech_recognition as sr
# from PicoTTS import TTS_engine
# from threading import Thread
# from enum import Enum
from NLPclass import NLP

from enum import Enum
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
SIA = SentimentIntensityAnalyzer()

nlp = NLP()

# def speak(text):
#     tts1 = gTTS(text=text, lang='fr', tld='ca')
#     audio = "audio.mp3"
#     tts1.save(audio)
#     os.system('mpg321 audio.mp3')

# def username(gender, firstname, lastname):
#     user = ""
#     if gender == "M":
#         user += f"Monsieur {lastname}"
#     elif gender == "F":
#         user += f"Madame {lastname}"
#     else:
#         user += firstname
#     return user
# print(username(" ", "Ginette", "Rancours"))
# nameGreeting = username("F", "Ginette", "Rancours")
# question1 = f"Comment aller vous aujourd'hui,{ nameGreeting }"
# speak(f"Comment aller vous aujourd'hui,{ nameGreeting }")

phrase = "Une phrase très cool à analyser"

phrase1 = "Une phrase à analyser"

phrase2 = "Une phrase pas cool à analyser"

score = SIA.polarity_scores(phrase)
print(score)
score = SIA.polarity_scores(phrase1)
print(score)
score = SIA.polarity_scores(phrase2)
print(score)

print(nlp.sentimentAnalisys(phrase))
print(nlp.sentimentAnalisys(phrase1))
print(nlp.sentimentAnalisys(phrase2))