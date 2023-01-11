from pymongo import MongoClient as mongo


# CREATION OF RPA CLASS

class RPA:
    def __init__(self):
        URI = "mongodb+srv://Phil:Sp9IFET6c7ceIWQa@maiya.engxn.mongodb.net/?retryWrites=true&w=majority"
        client = mongo(URI)
        db = client.RPA
        self.collection = db['RPA Clients']
    
    
    def insertNewClient(self, keyName, firstName, lastName, phone, address,
                        friend_1='n/a', fr_last_1= 'n/a', fr_phone_1='n/a', fr_type1='n/a',
                        friend_2='n/a', fr_last_2= 'n/a', fr_phone_2='n/a', fr_type2='n/a',
                        friend_3='n/a', fr_last_3= 'n/a', fr_phone_3='n/a', fr_type3='n/a',
                        family_1='n/a', fa_last_1= 'n/a', fa_phone_1='n/a', fa_type1='n/a',
                        family_2='n/a', fa_last_2= 'n/a', fa_phone_2='n/a', fa_type2='n/a',
                        family_3='n/a', fa_last_3= 'n/a', fa_phone_3='n/a', fa_type3='n/a',
                        medical_1='n/a', me_last_1= 'n/a', me_phone_1='n/a', me_type1='n/a',
                        medical_2='n/a', me_last_2= 'n/a', me_phone_2='n/a', me_type2='n/a',
                        medical_3='n/a', me_last_3= 'n/a', me_phone_3='n/a', me_type3='n/a',
                        emergency_1='n/a', em_last_1= 'n/a', em_phone_1='n/a', em_type1='n/a',
                        emergency_2='n/a', em_last_2= 'n/a', em_phone_2='n/a', em_type2='n/a',
                        emergency_3='n/a', em_last_3= 'n/a', em_phone_3='n/a', em_type3='n/a',
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
                                'Contact_1': {'Name': friend_1, 'Last': fr_last_1, 'Telephone': fr_phone_1, 'Type': fr_type1},
                                'Contact_2': {'Name': friend_2, 'Last': fr_last_2, 'Telephone': fr_phone_2, 'Type': fr_type2},
                                'Contact_3': {'Name': friend_3, 'Last': fr_last_3, 'Telephone': fr_phone_3, 'Type': fr_type3},
                                'Contact_4': {'Name': family_1, 'Last': fa_last_1, 'Telephone': fa_phone_1, 'Type': fa_type1},
                                'Contact_5': {'Name': family_2, 'Last': fa_last_2, 'Telephone': fa_phone_2, 'Type': fa_type2},
                                'Contact_6': {'Name': family_3, 'Last': fa_last_3, 'Telephone': fa_phone_3, 'Type': fa_type3},
                                'Contact_7': {'Name': medical_1, 'Last': me_last_1, 'Telephone': me_phone_1, 'Type': me_type1},
                                'Contact_8': {'Name': medical_2, 'Last': me_last_2, 'Telephone': me_phone_2, 'Type': me_type2},
                                'Contact_9': {'Name': medical_3, 'Last': me_last_3, 'Telephone': me_phone_3, 'Type': me_type3},
                                'Contact_10': {'Name': emergency_1, 'Last': em_last_1, 'Telephone': em_phone_1, 'Type': em_type1},
                                'Contact_11': {'Name': emergency_2, 'Last': em_last_2, 'Telephone': em_phone_2, 'Type': em_type2},
                                'Contact_12': {'Name': emergency_3, 'Last': em_last_3, 'Telephone': em_phone_3, 'Type': em_type3}
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
        user = self.collection.find_one({"ClientInfo.keyName": keyName})
        return user


if __name__ == '__main__':
    
    # INSTANTIATE CLASS
    RPA_db = RPA()
    
    # INSERT CLIENT WITH METHOD
    # RPA_db.insertNewClient( 'Phil', 'Phil', 'Doe', '514-564-8656', '123 RPA street, Montreal, Quebec, H1H 1H1',
    #                         friend_1='Nancy', fr_last_1='Smith', fr_phone_1='514-222-3456', fr_type1='Friend',
    #                         friend_2='Harry', fr_last_2='Klein', fr_phone_2='514-333-7547', fr_type2='Friend',
    #                         friend_3='George', fr_last_3='Ramos', fr_phone_3='514-444-8685', fr_type3='Friend',
    #                         family_1='Jim', fa_last_1='Doe', fa_phone_1='514-555-5745', fa_type1='Family',
    #                         family_2='Larry', fa_last_2='Doe', fa_phone_2='514-666-9867', fa_type2='Family',
    #                         family_3='Stephanie', fa_last_3='Doe', fa_phone_3='514-777-4354', fa_type3='Family',
    #                         medical_1='Dr. John', me_last_1='Miles', me_phone_1='514-888-9876', me_type1='Medical',
    #                         medical_2='Dr. Harry', me_last_2='Kravitz', me_phone_2='514-234-2452', me_type2='Medical',
    #                         medical_3='Dr. Liz', me_last_3='Nancy', me_phone_3='514-432-7355', me_type3='Medical',
    #                         emergency_1='Billy', em_last_1='Doe', em_phone_1='514-567-2432', em_type1='Emergency',
    #                         emergency_2='Evelyne', em_last_2='Richards', em_phone_2='765-111-7546', em_type2='Emergency',
    #                         emergency_3='Lisa', em_last_3='Kuds', em_phone_3='795-564-1234', em_type3='Emergency',
    #                         medication_1='Valium XR', dosageMed_1='3 times per day for 2 weeks',
    #                         medication_2='Motrin', dosageMed_2='1 pill every morning',
    #                         medication_3='Nalaproxen', dosageMed_3='2 pills before bed',
    #                         appointment_1='Oncologist', date_1='Monday, February 4, 2023', time_1='14:00', place_1='CLSC Montreal',
    #                         appointment_2='Neurosurgeon', date_2='Tuesday, March 6, 2023', time_2='13h00', place_2='Notre-Dame Hospital',
    #                         appointment_3='Family doctor', date_3='Thursday, April 2, 2023', time_3='8h30', place_3='Downtown Medical Clinic')
    
    # GET ALL CONTACT INFO BASED ON MQTT KEY RECEIVED AND PLACE IN VARIABLE 'john'
    phil = RPA_db.findClient('Phil')
    
    print('\n'.join(phil['Medication'].keys()))


    #ACCESS DATA (SEE EXAMPLES BELOW)
        
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
        
        
    print('\n\n**************** END ***************')
