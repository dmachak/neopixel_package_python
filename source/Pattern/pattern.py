
#  ColorPalette
#
#  Created by Dan Machak on 1/10/17 in C++
#  Ported to CircuitPython 11/16/19

import math
import time
import random
from array import array

# Index of RGB values in color tuples
R = 0
G = 1
B = 2

class ColorPalette:
    """Defines the set of colors used by a Pattern controller"""
    def __init__(self):
        self.size = 0
        self.colors = []


    def addColor(self, red, green, blue):
        color = array("H") # array of unsigned short ints
        self.size = self.size + 1
        color.append(red)
        color.append(green)
        color.append(blue)
        self.colors.append(color)

    def getColor(self, index):
        return self.colors[index]

    def checkIndex(self, index):
        return (index < self.size)

    def red(self, index):
        return self.getColor(index)[0]

    def green(self, index):
        return self.getColor(index)[1]

    def blue(self, index):
        return self.getColor(index)[2]

class ColorFunction:
    """Defines a function that modifies a Color over time."""
    def __init__(self, duration, colorPalette, params):
        self.duration = duration
        self.colorPalette = colorPalette
        self.params = params

    def getColor(self, position, time): return (red(0), green(0), blue(0))
    def r(self, i): return self.colorPalette.red(i)
    def g(self, i): return self.colorPalette.green(i)
    def b(self, i): return self.colorPalette.blue(i)
    def p(self, i): return self.params[i]

class SinColorFunction(ColorFunction):
    def getColor(self, position, time):
        f = math.sin(2*math.pi*(time + 3*self.duration/4)/self.duration) + 1;
        return (
            int(self.r(0) + (self.r(1)-self.r(0))*f/2),
            int(self.g(0) + (self.g(1)-self.g(0))*f/2),
            int(self.b(0) + (self.b(1)-self.b(0))*f/2)
        )

class StepColorFunction(ColorFunction):
    def getColor(self, position, time):
        return self.colorPalette.getColor(1)

#class Decay

class PulsePattern:
    FLAG1 = 1
    FLAG2 = 2
    FLAG3 = 4
    FLAG4 = 8
    FLAG5 = 16
    FLAG6 = 32
    FLAG7 = 64
    FLAG8 = 128

    FLAG1_MASK = 255^FLAG1
    FLAG2_MASK = 255^FLAG2
    FLAG3_MASK = 255^FLAG3
    FLAG4_MASK = 255^FLAG4
    FLAG5_MASK = 255^FLAG5
    FLAG6_MASK = 255^FLAG6
    FLAG7_MASK = 255^FLAG7
    FLAG8_MASK = 255^FLAG8

    # strip: of type neopixel.NeoPixel
    # colorFunction: the function to apply to each of the pulses
    # nPulses: Number of LEDs that are pulsing at any one time.
    def __init__(self, strip, colorFunction, nPulses):
        self.strip = strip;
        self.colorFunction = colorFunction
        self.nPulses = nPulses
        self.updateLength(self.strip.n)
        self.initializePulses()

    def getFlag(self, n, flag): return self.flags[n] & flag
    def setFlag(self, n, flag, value): self.flags[n] = (self.flags[n] | flag) if value else (self.flags[n] & (255^flag))
    def isComplete(self, index): return (not(self.isPixelOn(self.pulseIndex[index])) or self.pulseStep[index] >= self.colorFunction.duration)

    def turnPixelOn(self, n):  self.setFlag(n, PulsePattern.FLAG1, True)
    def turnPixelOff(self, n): self.setFlag(n, PulsePattern.FLAG1, False)
    def isPixelOn(self, n): return self.getFlag(n, PulsePattern.FLAG1)

    def setStep(self, n, s): self.step[n] = s
    def incrementStep(self, n): self.step[n] += 1
    def getStep(self, n): return self.step[n]

    def updateLength(self, n):
        self.flags = array("H")
        self.step = array("H")
        for i in range(n):
            self.flags.append(0)
            self.step.append(0)

    def initializePulses(self):
        self.pulseStep = array("H")
        self.pulseDelay = array("H")
        self.pulseIndex = array("H")
        for i in range(self.nPulses):
            self.pulseStep.append(0)
            self.pulseDelay.append(0)
            self.pulseIndex.append(0)
        for i in range(self.nPulses):
            self.startNewPulse(i, int(i*100/self.nPulses))

    def increment(self):
        for i in range(self.nPulses):
            if self.isComplete(i):
                self.resetPulse(i, 0);
            else:
                if self.pulseDelay[i] > 0:
                    self.pulseDelay[i] -= 1
                else:
                    self.strip[self.pulseIndex[i]] = self.colorFunction.getColor(0, self.pulseStep[i])
                    self.pulseStep[i] += 1
        self.strip.show();


    def resetPulse(self, pIndex, delay):
        self.turnPixelOff(self.pulseIndex[pIndex])
        self.pulseIndex[pIndex] = 0
        self.pulseDelay[pIndex] = 0
        self.pulseStep[pIndex] = 0
        self.startNewPulse(pIndex, delay)

    def startNewPulse(self, pIndex, delay):
        pix = random.randrange(self.strip.n)
        while self.isPixelOn(pix):
            pix = random.randrange(self.strip.n)
        self.startPixel(pix, pIndex, delay)

    def startPixel(self, index, pIndex, delay):
        self.turnPixelOn(index)
        self.pulseIndex[pIndex] = index
        self.pulseDelay[pIndex] = delay
        self.pulseStep[pIndex] = 0


class StripUtil:

    def __init__(self, strip, stepSize):
        self.strip = strip;
        self.stepSize = stepSize


    def resetStrip(self):
        for i in range(len(self.strip)):
            self.strip[i] = (0,0,0)
        self.strip.show()

    def setStripToColor(self, color):
        for i in range(len(self.strip)):
            self.strip[i] = color


    def fade(self, c1, c2, t):
        nSteps = int(t/self.stepSize)

        rdiff = c2[R] - c1[R]
        gdiff = c2[G] - c1[G]
        bdiff = c2[B] - c1[B]

        for i in range(nSteps):
            r = c1[R] + int(i * rdiff/nSteps)
            g = c1[G] + int(i * gdiff/nSteps)
            b = c1[B] + int(i * bdiff/nSteps)

            self.setStripToColor((r,g,b))
            self.strip.show()
            time.sleep(self.stepSize)


    def fadeIn(self, color, timeInMilliseconds):
        self.fade((0,0,0), color, timeInMilliseconds)

    def swipeUp(self, color, pixelsPerStep):
        for i in range(0, self.strip.n, pixelsPerStep):
            for j in range(0, pixelsPerStep):
                self.strip[i+j, color]
            self.strip.show()
