import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.clock import Clock
import threading
import time
import lib.pattern

#Looks like using another thread won't work. Got the error:
# TypeError: Cannot change graphics instruction outside the main Kivy thread
# See https://stackoverflow.com/questions/71885469/cannot-create-graphics-instruction-outside-the-main-kivy-thread
class Updater(threading.Thread):
    def __init__(self, stripApp, iterations, sleepInterval):
        threading.Thread.__init__(self)
        self.stripApp = stripApp
        self.iterations = iterations
        self.sleepInterval = sleepInterval
 
        # helper function to execute the threads
    def run(self):
        time.sleep(1)
        for i in range(self.iterations):
          print(".")
          self.stripApp.myStrip.color.rgba = (i/self.iterations, 0.3, 0.1, 1)
          time.sleep(self.sleepInterval)
 
 
class Strip(Widget):
    def __init__(self, **kwargs):
        super(Strip, self).__init__(**kwargs)
        self.x=0
        with self.canvas:
        	self.color = Color(rgba=(0.9, 0.9, 0.1, 1))
        	self.circle = Ellipse(pos=(100, 100), size=(50, 50))
        	Clock.schedule_interval(self.update, 1/30.)

    def update(self, *args):
        self.x+=3
        self.color.rgba = (self.x/1000, 0.3, 0.1, 1)

class My_app(App):
    def build(self):
        self.myStrip = Strip()
        return self.myStrip



#n: length of strip (read only)
#[]: array of values of type *color*
#fill(*color*): updates all pixels to the given color.
#show(): updates the actual pixels
class MockStrip():
	def __init__(self, size):
		self.pixels = [(0,0,0)]*size
		self.n = size
	
	def __getitem__(self, index):
		return self.pixels[index]
		
	def __setitem__(self, index, color):
		self.pixels[index] = color
		
	def fill(color):
		for i in range(self.n):
			self.pixels[i] = color
	
	def show():
		#Here's where we need to update the kivy widget
		
mockStrip = MockStrip(5)
mockStrip[0] = (3,4,5)
print(mockStrip[0])
print(mockStrip[1])
app = My_app()
#updateThread = Updater(app, 100, .1)
#updateThread.start()
#app.run()