from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.label import Label
import time
from threading import Thread

# This is a test to render some graphics and update the view from a separate thread.

class NeoPixelStrip(Widget):
    def __init__(self):
    	Color(1, 1, 0)
    	d = 30.
    	Ellipse(pos=(100, 100), size=(50, 50))


class NeoPixelApp(App):
    def build(self):
      return NeoPixelStrip()

class YourApp(App):
    def build(self):
      root_widget = Label(text='Hello world!')
      return root_widget
      

stripApp = NeoPixelApp()
stripApp.run()
time.sleep(3)