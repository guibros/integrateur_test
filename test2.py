from profilAtlas import Profil
#from atlasProfilV2 import RPA

from pymongo import MongoClient as mongo


# CREATION OF RPA CLASS

class RPA:
    def __init__(self):
        URI = "mongodb+srv://Phil:Sp9IFET6c7ceIWQa@maiya.engxn.mongodb.net/?retryWrites=true&w=majority"
        client = mongo(URI)
        db = client.RPA
        self.collection = db['RPA Clients']
    
    
    def insertNewClient(self, keyName, firstName, lastName, phone, address,
                        friend_1='n/a', fr_phone_1='n/a',
                        friend_2='n/a', fr_phone_2='n/a',
                        friend_3='n/a', fr_phone_3='n/a',
                        family_1='n/a', fa_phone_1='n/a',
                        family_2='n/a', fa_phone_2='n/a',
                        family_3='n/a', fa_phone_3='n/a',
                        medical_1='n/a', me_phone_1='n/a',
                        medical_2='n/a', me_phone_2='n/a',
                        medical_3='n/a', me_phone_3='n/a',
                        emergency_1='n/a', em_phone_1='n/a',
                        emergency_2='n/a', em_phone_2='n/a',
                        emergency_3='n/a', em_phone_3='n/a',
                        medication_1='n/a', dosageMed_1='n/a',
                        medication_2='n/a', dosageMed_2='n/a',
                        medication_3='n/a', dosageMed_3='n/a',
                        appointment_1='n/a', date_1='n/a', time_1= 'n/a', place_1='n/a',
                        appointment_2='n/a', date_2='n/a', time_2= 'n/a', place_2='n/a',
                        appointment_3='n/a', date_3='n/a', time_3= 'n/a', place_3='n/a'):
        new_client = {  'ClientInfo': {
                            'keyName': keyName, 'firstName': firstName,
                            'lastName':lastName,'Telephone': phone, 'address': address
                        },
                        'Contacts': {
                            'Friends': {
                                friend_1: {'Telephone': fr_phone_1},
                                friend_2: {'Telephone': fr_phone_2},
                                friend_3: {'Telephone': fr_phone_3}
                            },
                            'Family': {
                                family_1: {'Telephone': fa_phone_1},
                                family_2: {'Telephone': fa_phone_2},
                                family_3: {'Telephone': fa_phone_3}
                            },
                            'Medical': {
                                medical_1: {'Telephone': me_phone_1},
                                medical_2: {'Telephone': me_phone_2},
                                medical_3: {'Telephone': me_phone_3}
                            },
                            'Emergency': {
                                emergency_1: {'Telephone': em_phone_1},
                                emergency_2: {'Telephone': em_phone_2},
                                emergency_3: {'Telephone': em_phone_3}
                            }
                        },
                        'Medication': {
                            medication_1: {'Dosage': dosageMed_1},
                            medication_2: {'Dosage': dosageMed_2},
                            medication_3: {'Dosage': dosageMed_3}
                        },
                        'Appointments': {
                            appointment_1: {'Date': date_1, 'Time': time_1, 'Location': place_1},
                            appointment_2: {'Date': date_2, 'Time': time_2,'Location': place_2},
                            appointment_3: {'Date': date_3, 'Time': time_3,'Location': place_3}
                        }
                    }
        self.collection.insert_one(new_client)
        print(f'\n\nClient "{firstName} {lastName}" has been entered.')
        
        
    def findClient(self, keyName):
        return self.collection.find_one({"ClientInfo.keyName": keyName})




# profil = Profil("Bill")

# profilFetch = profil.fetch_profil()

# profilPop = profil.pop_profil()

# print(profilFetch)

# print(profilPop)

# print(profilFetch['Last_Name'])
# print(profilFetch['First_Name'])
# print(profilFetch['Personnel']['2'][-1])
# print(profilFetch['Medicament'][-1])

rpa = RPA()
userid = "John01"
userdata = rpa.findClient(userid)
print(userdata)