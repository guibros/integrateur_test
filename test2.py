from profilAtlas import Profil
from atlasProfilV2 import RPA
from NLPclass import NLP
from pymongo import MongoClient as mongo


# CREATION OF RPA CLASS





# profil = Profil("Bill")

# profilFetch = profil.fetch_profil()

# profilPop = profil.pop_profil()

# print(profilFetch)

# print(profilPop)

# print(profilFetch['Last_Name'])
# print(profilFetch['First_Name'])
# print(profilFetch['Personnel']['2'][-1])
# print(profilFetch['Medicament'][-1])

nlp = NLP()
rpa = RPA()
userid = "Phil"
userdata = rpa.findClient(userid)
#print(userdata)
print(userdata['Contacts']['Contact_1'])
namelist = []
lastlist = []


for contact in userdata['Contacts'].values():
    print(contact)
    namelist.append(contact['Name'])
    lastlist.append(contact['Last'])

    
print(namelist)
print(lastlist)
    
fullnamelist = list(zip(namelist,lastlist))
print(fullnamelist)




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
        