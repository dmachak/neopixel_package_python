
#  ColorPalette
#
#  Created by Dan Machak on 1/10/17 in C++
#  Ported to CircuitPython 11/16/19


from array import array

class ColorPalette:
    """Defines the set of colors used by a Pattern controller"""
    def __init__(self):
        self.size=0
        self.colors = []


    def addColor(self, red, green, blue):
        self.size++
        color = array("H") # array of unsigned short ints
        color.append(red)
        color.append(green)
        color.append(blue)
        self.colors.append(color)

    def setColor(self, index, red, green, blue):
        color = array("H") # array of unsigned short ints
        color[0] = red
        color[1] = green
        color[2] = blue
        self.colors[index] = color

    def getColor(self, index):
        return self.colors[index]

    def red(self, index):
        return self.getColor(index)[0]

    def green(self, index):
        return self.getColor(index)[1]

    def blue(self, index):
        return self.getColor(index)[2]