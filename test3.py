from NLPclass import NLP


nlp = NLP()

nlp.speak("parler")
data = nlp.listen()

nlp.speak(data)