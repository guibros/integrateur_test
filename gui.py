import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from datetime import datetime as dt
from mqttConfig import MQTTcontroller
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
# from kivy.uix.progressbar import ProgressBar


Window.fullscreen = True
# pb = ProgressBar(max=5)
Builder.load_file("gui.kv")

main = MQTTcontroller()
secondary = MQTTcontroller()
main.subscription('AHUNTSIC-PROJ-INT/gui')
secondary.subscription('AHUNTSIC-PROJ-INT/gui2')

class MyGridLayout(Widget):
    pass

class GUICONSTRUCTION(App):
    def on_start(self):
        Clock.schedule_interval(self.update_labels, 1)
        # pb.value = 20
         
    def update_labels(self, *args):
        self.root.ids.date.text = dt.now().strftime("%I:%M:%S %p")
        self.root.ids.time.text = dt.now().strftime("%Y-%m-%d")
        self.root.ids.greeting.text = main.message
        self.root.ids.questions.text = secondary.message
        
        
    def build(self):
        return MyGridLayout()
    
if __name__ == "__main__":
        GUICONSTRUCTION().run()
