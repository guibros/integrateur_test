import paho.mqtt.client as paho


class MQTTcontroller:
    def __init__(self, default):
        self.client = paho.Client()
        self.runMQTT()
        self.message = default
        
    def connect(self, client, userdata, flags, rc):
        print(f'MQTT connected with code {rc}')

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed to: "+str(mid)+" "+str(granted_qos))

    def message(self, client, userdata, msg):
        message = str(msg.payload).strip('b').strip("'")
        self.message = message

    def runMQTT(self):
        self.client.on_connect = self.connect
        self.client.on_subscribe = self.subscribe
        self.client.on_message = self.message
        self.client.connect('broker.mqttdashboard.com', 1883)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, payload=message,  qos=1)
    
    def subscription(self, topic):
        self.client.subscribe(topic, qos=1)
        
    def stopMQTT(self):
        self.client.loop_stop()