import unittest
import pattern

class TestColorPalette(unittest.TestCase):

    def test_setColor(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        actual = cp.getColor(0)
        self.assertEqual(10, actual[0])
        self.assertEqual(20, actual[1])
        self.assertEqual(30, actual[2])

    def test_colorAccessors(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        self.assertEqual(10, cp.red(0))
        self.assertEqual(20, cp.green(0))
        self.assertEqual(30, cp.blue(0))

    def test_multipleColors(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        cp.addColor(40, 50, 60)
        cp.addColor(70, 80, 90)
        self.assertEqual(3, cp.size)
        self.assertColor(cp.getColor(0), 10, 20, 30)
        self.assertColor(cp.getColor(1), 40, 50, 60)
        self.assertColor(cp.getColor(2), 70, 80, 90)

    @unittest.expectedFailure
    def test_indexOutOfBounds(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        cp.addColor(40, 50, 60)
        cp.addColor(70, 80, 90)
        cp.getColor(3)

    def assertColor(self, actual, expected_red, expected_green, expected_blue):
        self.assertEqual(expected_red, actual[0])
        self.assertEqual(expected_green, actual[1])
        self.assertEqual(expected_blue, actual[2])


class TestColorFunction(unittest.TestCase):
    def test_init(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        params = [1, 2, 3]
        cf = pattern.ColorFunction(100, cp, params)
        self.assertEqual(params, cf.params)
        self.assertEqual(100, cf.duration)
        self.assertEqual(cp, cf.colorPalette)

    def test_params(self):
        params = [2, 4, 6]
        cf = pattern.ColorFunction(100, None, params)
        self.assertEqual(cf.p(0), 2)
        self.assertEqual(cf.p(1), 4)
        self.assertEqual(cf.p(2), 6)

    def test_rgb(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 20, 30)
        cp.addColor(40, 50, 60)
        cf = pattern.ColorFunction(100, cp, None)

        self.assertEqual(10, cf.r(0))
        self.assertEqual(20, cf.g(0))
        self.assertEqual(30, cf.b(0))
        self.assertEqual(40, cf.r(1))
        self.assertEqual(50, cf.g(1))
        self.assertEqual(60, cf.b(1))

class TestSinColorFunction(unittest.TestCase):
    def test_getColor(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 10, 10)
        cp.addColor(20, 20, 20)
        cf = pattern.SinColorFunction(100, cp, None)
        c = cf.getColor(0, 0)
        self.assertEqual(10, c[0])
        self.assertEqual(10, c[1])
        self.assertEqual(10, c[2])

class TestPulsePattern(unittest.TestCase):
    def test_setFlag(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 5)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG1)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG2)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG3)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG4)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG5)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG6)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG7)
        self.checkFlag(pp, 3, pattern.PulsePattern.FLAG8)

    def test_setMultipleFlags(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 5)
        pp.setFlag(5, pattern.PulsePattern.FLAG1, False)
        pp.setFlag(5, pattern.PulsePattern.FLAG3, True)
        pp.setFlag(5, pattern.PulsePattern.FLAG5, True)

        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG1))
        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG2))
        self.assertTrue(pp.getFlag(5, pattern.PulsePattern.FLAG3))
        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG4))
        self.assertTrue(pp.getFlag(5, pattern.PulsePattern.FLAG5))
        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG6))
        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG7))
        self.assertFalse(pp.getFlag(5, pattern.PulsePattern.FLAG8))

    def test_pixelStateAtInit(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 4)
        nOn = 0
        for i in range(10):
            nOn += 1 if pp.isPixelOn(i) else 0
        #10 pixels, with 4 pulses, so should have 4 pixels on.
        self.assertEqual(4, nOn)

    def test_pixelSwitches(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 4)
        for i in range(10):
            self.checkPixelSwitch(pp, i)

    def test_steps(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 4)
        pp.setStep(3, 20);
        self.assertEqual(20, pp.getStep(3))
        pp.incrementStep(3)
        self.assertEqual(21, pp.getStep(3))

    def test_increment(self):
        strip = MockStrip(10)
        pp = pattern.PulsePattern(strip, self.getColorFunction(), 1)
        for i in range(10):
            if pp.isPixelOn(i): break
        self.assertTrue(pp.isPixelOn(i))
        self.assertEqual(i, pp.pulseIndex[0])
        self.assertEqual(0, pp.pulseStep[0])
        self.assertEqual(0, pp.pulseDelay[0])

        pp.increment()
        self.assertEqual(1, pp.pulseStep[0])
        self.assertEqual(0, pp.pulseDelay[0])
        self.assertEqual((10,10,10), strip[i])

        for j in range(50):
            pp.increment()
        self.assertEqual(51, pp.pulseStep[0])
        self.assertEqual((20,20,20), strip[i]) # peak of sine wave


    def checkFlag(self, pp, index, flag):
        pp.setFlag(index, flag, True)
        self.assertTrue(pp.getFlag(index, flag))
        pp.setFlag(index, flag, False)
        self.assertFalse(pp.getFlag(index, flag))

    def checkPixelSwitch(self, pp, index):
        pp.turnPixelOn(index)
        self.assertTrue(pp.isPixelOn(index))
        pp.turnPixelOff(index)
        self.assertFalse(pp.isPixelOn(index))

    def getColorFunction(self):
        cp = pattern.ColorPalette()
        cp.addColor(10, 10, 10)
        cp.addColor(20, 20, 20)
        cf = pattern.SinColorFunction(100, cp, None)
        return cf

    def printState(self, pp):
        print()
        print("flags:", pp.flags)
        print("step: ", pp.step)
        print("pulseDelay: ", pp.pulseDelay)
        print("pulseIndex: ", pp.pulseIndex)
        print("pulseStep: ", pp.pulseStep)

class MockStrip:
    def __init__(self, size):
        self.n = size
        self.my_custom_list = [(0,0,0)] * size

    def __setitem__(self, index, value):
        self.my_custom_list[index] = value

    def __getitem__(self, index):
        return self.my_custom_list[index]
        #return "Hey you are accessing {} element whose value is: {}".format(index, self.my_custom_list[index])

    def __str__(self):
        return str(self.my_custom_list)

    def show(self):
        return

if __name__ == '__main__':
    unittest.main()