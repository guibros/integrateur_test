import datetime
import pymongo

class MongoConsole:

    def __init__(self, host, database, collection):
        self.host = host
        self.database = database
        self.collection = collection

    def push(self, device, event):
        h=self.host
        client = pymongo.MongoClient(str(h))
        db = client[self.database] # La base de donnée
        evenement = {"nom": str(device),
                     "event" : str(event),
                      "date": datetime.datetime.now()}
        coll = db[self.collection]
        print("mongo event")
        print(evenement)
        print(coll.insert_one(evenement).inserted_id)

    def retrieve(self, number):
        h=self.host
        client = pymongo.MongoClient(str(h))
        db = client[self.database]
        coll = db[self.collection]
        entry = "DEVICE\t\tEVENT\t\tDATE/TIME\n==============================================\n\n"
        try:
            lastEntry = coll.find({},{'_id': 0}).sort([('_id',-1)]).limit(number)
            print(lastEntry)
        except:
            print("query not available")
        try:
            for item in lastEntry:
                valeurs = list(item.values())
                print(valeurs)
                device, event, time = valeurs[0], valeurs[1], valeurs[2]
                entry = entry + str(device) +"\t\t"+ str(event) +"\t"+ time.strftime("%m/%d/%Y, %H:%M:%S")+"\n"
                print(device +"\t"+ event +"\t"+ time.strftime("%m/%d/%Y, %H:%M:%S"))
        except:
            print("cant boarded data")
        return entry

mon = MongoConsole("localhost", "evenement", "historique")
mon.push("initialisation", "ON\OFF")
print(mon.retrieve(10))