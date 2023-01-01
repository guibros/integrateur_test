from NLPclass import NLP
       
nlp = NLP()
text = "Vous semblez en difficulté, comment puis-je vous aider?"      
nlp.speak(text)
#GUI negatif
data = ""
counter = 0
while data == "" and counter != 3:
    if counter != 0:
        nlp.speak("Pouvez-vous répéter?")
    data = nlp.listen()
    print(f"while: {data}")
    print(type(data))
    counter += 1
if data == "":
    nlp.speak("Passons a autre chose")
print(f"done: {data}")


def grabSpeechData(tryCount):
    data = ""
    counter = 0
    while data == "" and counter != tryCount:
        if counter != 0:
            nlp.speak("Pouvez-vous répéter?")
        data = nlp.listen()
        print(f"while: {data}")
        print(type(data))
        counter += 1
    if data == "":
        nlp.speak("Passons a autre chose")
    print(f"done: {data}")
    return data

grabSpeechData(3)


