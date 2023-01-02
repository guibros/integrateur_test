
import RPi.GPIO as GPIO
import time


class ProximitySensor:
    def __init__(self):
        self.TRIG = 11
        self.ECHO = 13
        self.distance = 0
        self.activated = True

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def distanceCalc(self):
        GPIO.output(self.TRIG, 0)
        time.sleep(0.000002)

        GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, 0)

        while GPIO.input(self.ECHO) == 0:
            a = 0
        time1 = time.time()
        while GPIO.input(self.ECHO) == 1:
            a = 1
        time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

    def loop(self):
        while self.activated:
            self.distance = round(self.distanceCalc())
            # print(f"Distance: {self.distance}\n")
            time.sleep(0.3)
        print('\nProximity loop ended')
        return

    def destroy(self):
        GPIO.cleanup()



if __name__ == "__main__":
    proxi = ProximitySensor()
    proxi.setup()
    try:
        proxi.loop()
    except KeyboardInterrupt:
        proxi.destroy()