import time
from GPIOconfig import ProximitySensor
from mqttConfig import MQTTcontroller


class ProximtyChecker:
    def __init__(self, distance=11):  # distance argument is only for testing purposes
        self.THRESHOLD_DISTANCE = 10
        self.initialBaseTime = time.time()
        self.initialProximityTime = time.time()
        self.BASE_WAIT_TIME = 5
        self.PROXIMITY_WAIT_TIME = 5
        mqtt.publish('AHUNTSIC-PROJ-INT/proxi', 'basestate')
        self.state = False
        self.newState = False
        # self.distance = distance  # Uncomment only for testing purposes
        
    def forAtLeast_x_seconds(self, seconds, initialTime):
        currenTime = time.time()
        timeDifference = round(currenTime - initialTime)
        if timeDifference >= seconds:
            return True
        return False
    
    def run(self, distance):
        if distance > self.THRESHOLD_DISTANCE:  # Every 'BASE_WAIT_TIME' seconds, publish basestate if distance greater than threshold
            self.newstate = False
            if self.newstate != self.state:
                mqtt.publish('AHUNTSIC-PROJ-INT/state', f'basestate, {distance}')
            if self.forAtLeast_x_seconds(self.BASE_WAIT_TIME, self.initialBaseTime):
                mqtt.publish('AHUNTSIC-PROJ-INT/state', f'basestate, dontCheckIdentity, {distance}')
                self.initialBaseTime = time.time()  # Update the initial proximity time
                print(distance)
            self.initialProximityTime = time.time()
        elif distance <= self.THRESHOLD_DISTANCE:
            self.newstate = True
            if self.newstate != self.state:
                mqtt.publish('AHUNTSIC-PROJ-INT/state', f'limbostate, dontCheckIdentity, {distance}')
            if self.forAtLeast_x_seconds(self.PROXIMITY_WAIT_TIME, self.initialProximityTime): 
                mqtt.publish('AHUNTSIC-PROJ-INT/state', f'proxistate, checkIdentity, {distance}')
                self.initialProximityTime = time.time()
                print(distance)
            self.initialBaseTime = time.time()
        self.state = self.newState
          
if __name__ == '__main__':
    
    try:
        from threading import Thread
        
        proximity = ProximitySensor()
        proximity.setup()
        proxiThread = Thread(target=proximity.loop)
        proxiThread.start()
        
        mqtt = MQTTcontroller()
        proximityChecker = ProximtyChecker()
        
        while True:
            proximityChecker.run(proximity.distance)
        
        
        # ****** Uncomment section below for testing only ******
        
        # def inputs():
        #     while True:
        #         proximity.distance = int(input('Write distance: '))
                
        # inputsThread = Thread(target=inputs)
        # inputsThread.start()
        # time.sleep(5)
        
        # ******************************************************

    except KeyboardInterrupt:
        proximity.activated = False