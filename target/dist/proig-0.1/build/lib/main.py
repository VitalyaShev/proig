from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.popup import Popup

import time
import os
import pygame as pg
pg.mixer.init()

musiclist = []

class MainWidget(MDScreen):
    #this first class is responsible for the screen that is, what the widgets will be placed on
    container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.play = False
        self.pause = False
        self.music = False
        self.sound = None
        self.flag = False
        self.s = 0
        self.filename = 0
        self.filename1 = 0
        self.muspos = 0
        self.removebut = False
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        #scroll settings and music display on the screen
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_text_inputs()

    def add_text_inputs(self):
        #showing music on the screen
        fileList = os.listdir(".")
        i = 50
        id = 'test'+ str(i)
        for filename in fileList:
            if filename.endswith(".mp3"):
                musiclist.append(filename)
        for filename in musiclist:
            if (len(musiclist)<13):
                lab = Label(text=filename,size_hint_y=None, height=50, width = self.ids.RightPanelDown.width)
                btn = Button(text="Add", height=lab.size[1], pos=(lab.pos[0]+1435, lab.pos[1]+300- i))
                btn1 = Button(text=filename, on_press=lambda x: self.playaudio(x.text), height=lab.size[1],pos=(lab.pos[0], lab.pos[1] + 300 - i))
            else:
                lab = Label(text=filename,size_hint_y=None, height=50, width = self.ids.RightPanelDown.width)
                btn = Button(text="Add", height=lab.size[1], pos=(lab.pos[0]+1435, lab.pos[1]+1200- i))
                btn1 = Button(text=filename, on_press=lambda x: self.playaudio(x.text), height=lab.size[1],pos=(lab.pos[0], lab.pos[1] + 1200 - i))
            i += 50
            lab.add_widget(btn)
            lab.add_widget(btn1)
            self.container.add_widget(lab)


    def playaudio(self,filename):
        #the function of starting, pausing, creating widgets for music control
        if (self.sound == None):
            pg.mixer.music.load(filename)
            self.sound = pg.mixer.Sound(filename)
            self.filename = filename
            for i in musiclist:
                if (i == self.filename):
                    n = musiclist.index(i)
                    if (i != musiclist[-1]):
                        self.filename1 = musiclist[n + 1]
                    else:
                        self.filename1 = musiclist[0]
            if (self.removebut==False):
                self.butplay(self.ids.play, 1)
        else:
            if (self.filename!=filename):
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                self.play = False
                self.music = False
                self.pause = False
                self.sound = None
                self.filename = filename
                pg.mixer.music.load(filename)
                self.sound = pg.mixer.Sound(filename)
                for i in musiclist:
                    if (i == self.filename):
                        n = musiclist.index(i)
                        if (i != musiclist[-1]):
                            self.filename1 = musiclist[n + 1]
                        else:
                            self.filename1 = musiclist[0]
                self.progressbar.max = self.sound.get_length()
                self.progressbar.value = 0
                self.progressbar.min = 0
                self.mussiz.text = time.strftime('%M:%S', time.gmtime(self.sound.get_length()+1))
                Clock.unschedule(self.progressbarEvent)
                Clock.unschedule(self.timeEvent)

        if (self.flag == False):
            self.progressbar = Slider(min=0, max=self.sound.get_length(), value=0, pos = (810, 660),size=(700, 10))
            self.buttonstpl = ToggleButton(pos = (1130, 680), size = (50,50),on_press=lambda x: self.playaudio(self.filename))
            self.butnext = Button(pos = (1200, 680), size = (50,50),on_press=lambda x: self.nextmus())
            self.butpre = Button(pos=(1060, 680), size=(50, 50),on_press=lambda x: self.premus())
            self.volumeslider = Slider(min=0,max=1,value=0.5,orientation='horizontal', pos = (560, 660), size=(200, 10))
            self.filebar = Label(text = self.filename, pos=(1100, 710))
            self.mussiz = Label(text = time.strftime('%M:%S', time.gmtime(self.sound.get_length()+1)), pos=(1420, 640))
            self.mustime = Label(text = "00:00", pos=(800, 640))
            self.progressbar.bind(value = self.setpos)
            self.volumeslider.bind(value = self.vol)
            self.ids.RightPanelUp.add_widget(self.progressbar)
            self.ids.RightPanelUp.add_widget(self.buttonstpl)
            self.ids.RightPanelUp.add_widget(self.butnext)
            self.ids.RightPanelUp.add_widget(self.butpre)
            self.ids.RightPanelUp.add_widget(self.volumeslider)
            self.ids.RightPanelUp.add_widget(self.filebar)
            self.ids.RightPanelUp.add_widget(self.mussiz)
            self.ids.RightPanelUp.add_widget(self.mustime)
            self.flag = True


        if (self.music == False):
            pg.mixer.music.set_volume(self.volumeslider.value)
            self.filebar.text = self.filename
            if (self.pause == True):
                pg.mixer.music.unpause()
            else:
                pg.mixer.music.play()
            self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar, 1)
            self.timeEvent = Clock.schedule_interval(self.settime, 1)
            self.music = True
            self.play = True
            self.pause = False
        else:
            Clock.unschedule(self.progressbarEvent)
            Clock.unschedule(self.timeEvent)
            pg.mixer.music.pause()
            self.play = False
            self.music = False
            self.pause = True

    def butplay(self, but, n):
        #the function responsible for removing the play button at the start of playback
        self.removebut = True
        self.remove_widget(but)
        if (n==0):
            for file in musiclist:
                self.playaudio(file)
                break

    def updateprogressbar(self,value):
        #music progress slider update function
        if self.progressbar.value < self.progressbar.max:
            self.progressbar.value += 1
        else:
            self.playaudio(self.filename1)

    def nextmus(self):
        #switching songs forward
        for i in musiclist:
            if (i == self.filename):
                n = musiclist.index(i)
                if (self.filename != musiclist[-1]):
                    self.playaudio(musiclist[n + 1])
                else:
                    self.playaudio(musiclist[0])
                break

    def premus(self):
        # switching songs back
        for i in musiclist:
            if (i == self.filename):
                n = musiclist.index(i)
                if (self.filename == musiclist[0]):
                    self.playaudio(musiclist[-1])
                else:
                    self.playaudio(musiclist[n - 1])
                break

    def settime(self, t):
        #updating the music playback time
        self.mustime.text = time.strftime('%M:%S', time.gmtime(self.progressbar.value))


    def setpos(self, instance, value):
        #function so that you can select any position for playing music
        if (pg.mixer.music.get_busy()):
            pg.mixer.music.set_pos(value)

    def vol(self, instance, value):
        #music volume control
        pg.mixer.music.set_volume(value)

    def addps(self):
        #playlist additions
        layout = BoxLayout(padding=10, orientation='vertical')
        self.txt1 = TextInput(text='', multiline=False)
        layout.add_widget(self.txt1)
        btn1 = Button(text="OK")
        btn1.bind(on_press=self.buttonClicked)
        layout.add_widget(btn1)
        self.popupWindow = Popup(title="Как назовем?", content=layout, size_hint=(None, None), size=(300, 200))
        self.popupWindow.open()

    def buttonClicked(self, btn):
        #turning off the pop-up window
        self.popupWindow.dismiss()

class Playls(MDScreen):
    # this second class is responsible for the screen that is, what the widgets will be placed on
    def __init__(self, **kwargs):
        super(Playls, self).__init__(**kwargs)




class MyMusicApp(MDApp):
    #this function is responsible for what will be shown on the screen
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWidget(name='mymusic'))
        sm.add_widget(Playls(name='playls'))
        return sm


if __name__ == "__main__":
    Window.fullscreen = 'auto'
    MyMusicApp().run()
