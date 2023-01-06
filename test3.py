from NLPclass import NLP


nlp = NLP()

nlp.speak("parler")
data = nlp.listen()

nlp.speak(data)
result = nlp.analyze(data)
nlp.speak(result)

# if nlp.analyzeVariable(text, friend1):
#     retuen phone number 
#     call number associated to friend1