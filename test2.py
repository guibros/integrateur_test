from profilAtlas import Profil
from atlasProfilV2 import RPA
from NLPclass import NLP






nlp = NLP()
rpa = RPA()
userid = "Phil"
userdata = rpa.findClient(userid)
#print(userdata)
print(userdata['Contacts']['Contact_1'])
namelist = []
lastlist = []
fullcontactlist = []


for contact in userdata['Contacts'].values():
    print(contact)
    fullcontactlist.append(contact)
    namelist.append(contact['Name'])
    lastlist.append(contact['Last'])

    
print(namelist)
print(lastlist)
print(fullcontactlist)
    
fullnamelist = list(zip(namelist,lastlist))
print(fullnamelist)


nlp = NLP()

nlp.speak("parler")
data = nlp.listen()

nlp.speak(data)
result = nlp.analyze(data)
nlp.speak(result)

if result == "appel":
    for contact in fullcontactlist:
        if nlp.analyzeVariable(data, contact['Name']):
            #return tel from name
            print(contact['Telephone'])
        else:
            nlp.speak("Aucun contact a ce nom")
            break

            


















#print(userdata['Contacts'])
#text= nlp.listen()
#
# listeContact = []
# for contactlist, variable in userdata['Contacts'].items():
    #print(contactlist)
    #print(variable)
    #for name, phoneNumber in variable.items():
        #print((name, phoneNumber['Telephone']))
        #isteContact.append((name, phoneNumber['Telephone']))
        #print(phoneNumber)
#print(listeContact)
# for name, phoneNumber in listeContact:
#     if nlp.analyzeVariable(text, name[0]):
#         print(name, phoneNumber)
    # print(name)
    # print(phoneNumber)
        