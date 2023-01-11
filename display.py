from datetime import datetime as dt

def userNotinDB(display):
    display.main = ''
    display.secondary = 'User not in database'
    display.spinner = 'images/black.png'
    display.date = False
    display.time = False
    
def turnOff(display):
    display.main = 'Au Revoir'
    display.secondary = ''
    display.spinner = 'images/black.png'
    display.date = False
    display.time = False


def showNothing(display):
    display.main = ''
    display.secondary = ''
    display.spinner = 'images/black.png'
    display.date = False
    display.time = False
    
def otherRequest(display):
    display.main = ''
    display.secondary = "Avez-vous besoin d'autres chose?"
    display.spinner = 'images/waiting.zip'
    display.date = False
    display.time = False
    
def identificationProcess(display):
    display.main = f''
    display.secondary = 'Identification en cours'
    display.spinner = 'images/wave.zip'
    display.date = True
    display.time = True
    
def unknownUser(display):
    display.main = 'Current Activities'
    display.secondary = ''
    display.date = True
    display.time = True
    
def identifiedUser(display, userName):
    display.main = f'Bonjour {userName}'
    display.secondary = "Comment vous sentez-vous?"
    display.spinner = 'images/speaking.zip'
    display.date = True
    display.time = True
    
def positiveMenu(display, userName):
    display.main = f'Ok {userName}, Comment puis-je vous aider?'
    display.secondary = "Dites une commande"
    display.spinner = 'images/speaking.zip'
    display.date = True
    display.time = True
    
def userRequest(display, request):
    display.main = request
    # display.secondary = request
    # display.date = True
    # display.time = True
    
def userRequest_time(display):
    display.main = "Il est présentement"
    display.secondary = dt.now().strftime('%I:%M')
    
def userRequest_medication(display, medication):
    display.main = "Vos médicaments:"
    display.secondary = medication
    
def userAideMenu(display, contacts):
    display.main = "Avec qui aimeriez vous parler?"
    display.secondary = contacts
    display.date = True
    display.time = True
    
def emergency(display, text):
    display.main = text
    display.secondary = f"Proche aidant / spécialiste de la santé?\nInfirmier ou infirmière?\nServices d'urgence?"
    display.date = True
    display.time = True