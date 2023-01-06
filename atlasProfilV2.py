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


# if __name__ == '__main__':
    
#     # INSTANTIATE CLASS
#     RPA_db = RPA()
    
#     # INSERT CLIENT WITH METHOD
#     RPA_db.insertNewClient( 'John01', 'John', 'Doe', '514-564-8656', '123 RPA street, Montreal, Quebec, H1H 1H1',
#                             friend_1='Nancy Smith', fr_phone_1='514-222-3456',
#                             friend_2='Harry Klein', fr_phone_2='514-333-7547',
#                             friend_3='George Ramos', fr_phone_3='514-444-8685',
#                             family_1='Jim Doe', fa_phone_1='514-555-5745',
#                             family_2='Larry Doe', fa_phone_2='514-666-9867',
#                             family_3='Stephanie Doe', fa_phone_3='514-777-4354',
#                             medical_1='Dr. Miles', me_phone_1='514-888-9876',
#                             medical_2='Dr. Kravitz', me_phone_2='514-234-2452',
#                             medical_3='Dr. Nancy', me_phone_3='514-432-7355',
#                             emergency_1='Billy Doe', em_phone_1='514-567-2432',
#                             emergency_2='Evelyne Richards', em_phone_2='765-111-7546',
#                             emergency_3='Lisa Kuds', em_phone_3='795-564-1234',
#                             medication_1='Valium XR', dosageMed_1='3 times per day for 2 weeks',
#                             medication_2='Motrin', dosageMed_2='1 pill every morning',
#                             medication_3='Nalaproxen', dosageMed_3='2 pills before bed',
#                             appointment_1='Oncologist', date_1='Monday, February 4, 2023', time_1='14:00', place_1='CLSC Montreal',
#                             appointment_2='Neurosurgeon', date_2='Tuesday, March 6, 2023', time_2='13h00', place_2='Notre-Dame Hospital',
#                             appointment_3='Family doctor', date_3='Thursday, April 2, 2023', time_3='8h30', place_3='Downtown Medical Clinic')
    
# # GET ALL CONTACT INFO BASED ON MQTT KEY RECEIVED AND PLACE IN VARIABLE 'john'
# john = RPA_db.findClient('John01')


# #ACCESS DATA (SEE EXAMPLES BELOW)
    
# # ALL DATA
# print('\n\n**************** ALL DATA ***************')
# print(f"Client data:\n\n{john}")

# # CONTACT CATEGORIES
# print('\n\n**************** CONTACT CATEGORIES ***************')
# print(list(john['Contacts'].keys()))

# # FAMILLY CONTACTS 
# print('\n\n**************** COMPLETE FAMILLY CONTACTS ***************')
# print(list(john['Contacts']['Family'].items()))

# # NAMES OF DOCTORS 
# print('\n\n**************** ONLY NAMES OF DOCTORS ***************')
# print(list(john['Contacts']['Medical'].keys()))

# # ONE EMERGENCY CONTACT 
# print('\n\n**************** ONE EMERGENCY CONTACT ("Billy Doe") ***************')
# print(john['Contacts']['Emergency']['Billy Doe'])

# # MEDICATION LIST
# print('\n\n**************** MEDICATION LIST ***************')
# print(list(john['Medication'].keys()))

# # MEDICATION LIST and DOSAGE
# print('\n\n**************** MEDICATION LIST and DOSAGE ***************')
# print(list(john['Medication'].items()))

# # APPOINTMENTS
# print('\n\n**************** APPOINTMENT DATES ***************')
# for appointment, info in john['Appointments'].items():
#     print(appointment, info['Date'], info['Time'], info['Location'])
    
# # APPOINTMENT LOCATIONS
# print('\n\n**************** ONLY APPOINTMENT LOCATIONS ***************')
# for appointment, info in john['Appointments'].items():
#     print(info['Location'])
    
    
# print('\n\n**************** END ***************')
