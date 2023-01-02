import pymongo

# Running on RaspbarryPi
# client = pymongo.MongoClient("localhost",username='admin',password='SUPERSECRETPASSWORD')
# Tested on windows
#client = pymongo.MongoClient("localhost")
URI = 'mongodb+srv://app_user:app123456@cluster0.lk6o7.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(URI)

db = client.project  # La base de donnée project
collection = db.profil  # La collection profil


class Profil:
    def __init__(self, key, first_name=None, last_name=None, phone=None, personnel_1=None, phone_1=None, personnel_2=None, phone_2=None,
                 personnel_3=None,
                 phone_3=None,
                 professional=None, phone_pro=None, urgence=None, phone_urg=None, medecin=None, phone_med=None,
                 medicament=None, dose=None,
                 rendez_vous_sujet=None, rendez_vous_date=None, rendez_vous_medecin=None, rendez_vous_loc=None):
        self.key = key
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        # 3 contacts personnels
        self.personnel_1 = personnel_1
        self.phone_1 = phone_1
        self.personnel_2 = personnel_2
        self.phone_2 = phone_2
        self.personnel_3 = personnel_3
        self.phone_3 = phone_3
        # 1 interlocuteur professionnel
        self.professional = professional
        self.phone_pro = phone_pro
        # 1 contact urgent
        self.urgence = urgence
        self.phone_urg = phone_urg
        # Le médecin principal responsable
        self.medecin = medecin
        self.phone_med = phone_med
        # registre des médicaments, peut être multiple
        self.medicament = medicament
        self.dose = dose
        # registre des rendez-vous, peut être multiple
        self.rendez_vous_sujet = rendez_vous_sujet
        self.rendez_vous_date = rendez_vous_date
        self.rendez_vous_medecin = rendez_vous_medecin
        self.rendez_vous_loc = rendez_vous_loc

    def insert(self):
        if collection.count_documents({"Key": self.key}) != 0:
            print("Error: Ce nom d'utilisateur est déjà enregistré")
        elif collection.count_documents({"Phone": self.phone}) != 0:
            print("Error: Ce numéro de téléphone est déjà enregistré")
        else:
            enregistrement = {"Key": self.key,
                              "First_Name": self.first_name,
                              "Last_Name": self.last_name,
                              "Phone": self.phone,
                              "Personnel": {"1": [self.personnel_1, self.phone_1],
                                            "2": [self.personnel_2, self.phone_2],
                                            "3": [self.personnel_3, self.phone_3]},
                              "Professional": [self.professional, self.phone_pro],
                              "Urgence": [self.urgence, self.phone_urg],
                              "Medecin": [self.medecin, self.phone_med],
                              "Medicament": [{"Nom": self.medicament, "Dose": self.dose}],
                              "Rendez_Vous": [{"Sujet": self.rendez_vous_sujet, "Date": self.rendez_vous_date,
                                               "Medecin": self.rendez_vous_medecin, "Loc": self.rendez_vous_loc}]}
            # print("insérer: ", enregistrement)
            collection.insert_one(enregistrement).inserted_id
            print("L'enregistrement du nouvel utilisateur est terminé.")

    def ajoute_medicament(self, medicament, dose):
        for item in db.list_collection_names():
            collection = db[item]
            cursor = collection.find({"Key": self.key})
            for document in cursor:
                if document['Medicament'] != [] and all(
                        v is not None for v in [document['Medicament'][0]['Nom'], document['Medicament'][0]['Dose']]):
                    collection.update_one({"Key": self.key},
                                          {"$push": {"Medicament": {"Nom": medicament, "Dose": dose}}})
                else:
                    collection.update_one({"Key": self.key},
                                          {"$set": {"Medicament": [{"Nom": medicament, "Dose": dose}]}})

    def ajoute_rendez_vous(self, rendez_vous_sujet, rendez_vous_date, rendez_vous_medecin, rendez_vous_loc):
        for item in db.list_collection_names():
            collection = db[item]
            cursor = collection.find({"Key": self.key})
            for document in cursor:
                if document['Rendez_Vous'] != [] and all(
                        v is not None for v in [document['Rendez_Vous'][0]['Sujet'], document['Rendez_Vous'][0]['Date'],
                                                document['Rendez_Vous'][0]['Medecin'],
                                                document['Rendez_Vous'][0]['Loc']]):
                    collection.update_one({"Key": self.key},
                                          {"$push": {
                                              "Rendez_Vous": {"Sujet": rendez_vous_sujet, "Date": rendez_vous_date,
                                                              "Medecin": rendez_vous_medecin, "Loc": rendez_vous_loc}}})
                else:
                    collection.update_one({"Key": self.key},
                                          {"$set": {
                                              "Rendez_Vous": [{"Sujet": rendez_vous_sujet, "Date": rendez_vous_date,
                                                               "Medecin": rendez_vous_medecin,
                                                               "Loc": rendez_vous_loc}]}})

    def supprimer_rendez_vous(self, rendez_vous_sujet, rendez_vous_date, rendez_vous_medecin, rendez_vous_loc):
        for item in db.list_collection_names():
            collection = db[item]
            cursor = collection.find({"Key": self.key})
            for document in cursor:
                # print(document['Rendez_Vous'])
                for item in document['Rendez_Vous']:
                    if item['Sujet'] == rendez_vous_sujet and item['Date'] == rendez_vous_date and item['Medecin'] == rendez_vous_medecin and item['Loc'] == rendez_vous_loc:
                        # print("rendez_vous deleted!")
                        collection.update_one({"Key": self.key},
                                              {"$pull": {
                                                  "Rendez_Vous": {"Sujet": rendez_vous_sujet, "Date": rendez_vous_date,
                                                                  "Medecin": rendez_vous_medecin,
                                                                  "Loc": rendez_vous_loc}}})

    def supprimer_medicament(self, medicament, dose):
        for item in db.list_collection_names():
            collection = db[item]
            cursor = collection.find({"Key": self.key})
            for document in cursor:
                # print(document['Medicament'])
                for item in document['Medicament']:
                    # print("medicament deleted!")
                    if item['Nom'] == medicament and item['Dose'] == dose:
                        collection.update_one({"Key": self.key},
                                              {"$pull": {"Medicament": {"Nom": medicament, "Dose": dose}}})

    def renouvele_profil(self, first_name, last_name, phone, personnel_1, phone_1, personnel_2, phone_2, personnel_3, phone_3,
                         professional, phone_pro, urgence, phone_urg, medecin, phone_med):
        for item in db.list_collection_names():
            collection = db[item]
            collection.update_one({"Key": self.key},
                                  {"$set": {"First_Name": first_name,
                                            "Last_Name": last_name,
                                            "Phone": phone,
                                            "Personnel": {"1": [personnel_1, phone_1],
                                                          "2": [personnel_2, phone_2],
                                                          "3": [personnel_3, phone_3]},
                                            "Professional": [professional, phone_pro],
                                            "Urgence": [urgence, phone_urg],
                                            "Medecin": [medecin, phone_med]}})
            print("La mise à jour du profil utilisateur est terminée")

    # pour l'administrateur de la maison de retraite
    def fetch_profil(self):
        for item in db.list_collection_names():
            collection = db[item]
            if collection.count_documents({"Key": self.key}) == 0:
                print("Le profil utilisateur n'existe pas.")
            else:
                cursor = collection.find({"Key": self.key})
                for document in cursor:
                    print(document)

    # for MQTT use
    def pop_profil(self):
        for item in db.list_collection_names():
            collection = db[item]
            cursor = collection.find({"Key": self.key})
            for document in cursor:
                print(document)

    def delete_profil(self):
        for item in db.list_collection_names():
            collection = db[item]
            if collection.count_documents({"Key": self.key}) == 0:
                print("Le profil utilisateur n'existe pas.")
            else:
                collection.delete_one({"Key": self.key})
                print("La suppression de l'utilisateur est terminée.")
