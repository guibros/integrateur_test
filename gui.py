import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from datetime import datetime as dt
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
import CommandCenter_v2 as CC
from threading import Thread
# from kivy.uix.progressbar import ProgressBar

#SET SCREEN RESOLUTION
RESOLUTION = 1200

# DEFAULT PARAMETERS
Window.size = (RESOLUTION, RESOLUTION)
# Window.clearcolor = (1, 1, 0, 0)
# pb = ProgressBar(max=5)
Builder.load_file("gui.kv")


class MyGridLayout(Widget):
    pass

class GUICONSTRUCTION(App):

    def on_start(self):
        self.TEST = 'x'
        Clock.schedule_interval(self.update_labels, 1)
        # pb.value = 20

    def update_labels(self, *args):
        # if cc.date == False:
        #     self.root.ids.date.text = ''
        #     self.root.ids.time.text = ''
        # else:
        #     self.root.ids.date.text = dt.now().strftime("%Y-%m-%d")
        #     self.root.ids.time.text = dt.now().strftime("%I:%M:%S %p")
        self.root.ids.main.text = cc.main
        self.root.ids.spinner.source = cc.spinner
        self.root.ids.secondary.text = cc.secondary
  
    def start(self):
        GUICONSTRUCTION().run()
        
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        self.title = 'ARPA (Assistant RPA)'
        return MyGridLayout()

    def on_request_close(self, *args):
        cc.running = False



if __name__ == "__main__":
    try:
        cc = CC.CommandCenter()
        commandCenterThread = Thread(target=cc.runCommandCenter)
        commandCenterThread.start()
        GUICONSTRUCTION().run()
        
    except KeyboardInterrupt:
        cc.running = False