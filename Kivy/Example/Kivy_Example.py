from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.config import Config
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color

import random

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '320')


running = True


class MyWidget(AnchorLayout):

    LOC = []
    for i in range (10):
        LOC.append((random.randint(0,400),random.randint(0,300)))


    B_G_IMG="B_image.png"


    time_number = StringProperty()

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.time_number = str(50)

    def remove_rectangle(self, widget):
        self.grid_layout.remove_widget(widget)
        self.set_level(2)
    def set_level(self,level_num):
        global B_G_ImG
        B_G_IMG = StringProperty("B_image2.png")
        print(B_G_IMG)


    def call(self):
        if running:
            #print(self.time_number)
            #self.time_number = str(int(self.time_number)+1)
            pass
    def clicked(self):
        global running
        #self.time_number = 50
        running=False

    Clock.schedule_interval(call, 1)

    pos1 =(0) #random.randint(-200,200)
    pos2 =(0) #random.randint(-200,200)

class WidgetsApp(App):
    def build(self):
        return MyWidget()


if __name__=="__main__":
    WidgetsApp().run()