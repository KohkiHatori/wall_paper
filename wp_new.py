import numpy as np
import random
import math
from PIL import Image
from itertools import product
from datetime import datetime


class WallPaper:


    def __init__(self, data, destination, name=str(datetime.now())):
        self.data = data
        self.dest = destination
        self.name = name
        self.create_image()

    def create_image(self):
        self.image = Image.fromarray(self.data)

    def output(self):
        self.image.save(self.dest + f"{self.name}.png")

    def show(self):
        self.image.show()

    def main(self, output=False):
        self.show()
        if output:
            self.output()

class ImageData:

    def __init__(self, functions, rgb_ratio, screen_size=(1080, 1980), reverse=False):
        self.functions = [np.vectorize(func) for func in functions]
        self.rgb_ratio = np.array(rgb_ratio)
        self.height, self.width = screen_size
        self.domain = math.pi*4
        self.f_range = self.domain * (self.height/self.width)
        self.max_brightness = 255
        self.max_diff_pix = 24
        self.max_ratio = self.max_brightness//(max(self.rgb_ratio))
        self.cartesian_max_diff = self.f_range/(self.height/2) * self.max_diff_pix
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8 )
        self.reverse = reverse

    def _get_strength(self, difference):
        if difference == 0:
            return self.max_ratio
        default = int(self.max_ratio * ((self.cartesian_max_diff - difference)/self.cartesian_max_diff))
        if difference <= self.cartesian_max_diff/3:
            return default
        prob = random.random()
        delta = difference/self.cartesian_max_diff
        if prob > delta:
            return default
        return 0

    def assign_rgb(self, y, x):
        # modifying x&y to be in cartesian coordinates
        x = x - self.width/2
        y = self.height - y - self.height/2
        # modifying x&y to be in the right magnification
        x = self.domain/(self.width/2) * x 
        y = self.f_range/(self.height/2) * y 
        difference = self.get_difference(y, x)
        strength = self._get_strength(difference)
        return self.rgb_ratio * strength

    def _get_ys(self):
        x = np.linspace(-self.domain, self.domain, self.width)
        y_actual = [func(x) for func in self.functions]
        y_upper = y_actual + self.cartesian_max_diff
        y_lower = y_actual - self.cartesian_max_diff

        
    def create_data(self):
        self.data[y, x] = [r, g, b]  

"""
Fucntions to draw:
-------------------------------------------------------------------------------------------------------
"""

def exp(x):
    return math.e ** (x**2)

def mugen(x):
    return math.sqrt(x**2 - x**4)

def exp2(x):
    return x ** x

def sinsq(x):
    return math.sin(x)**2

def sin_rec(x):
    if x != 0:
        return math.sin(1/x)
    else:
        return 0

def ntan(x):
    return -math.tan(x)

def mytan(n):
    return lambda x: math.tan(x) + n

def myntan(n):
    return lambda x: -math.tan(x) + n

def create_tans():
    tans = []
    for i in range(-10, 11, 2):
        tans.append(mytan(i))
        tans.append(myntan(i))
    return tans

def cot(x):
    try:
        return 1/math.tan(x)
    except:
        return 0 

def kaidan(x):
    return math.e**math.sin(x) + x

"""
-------------------------------------------------------------------------------------------------------
"""

def main():
    functions = [math.sinh]
    rgb_ratio = (1, 4, 2)
    data = ImageData(functions, rgb_ratio, reverse=False)
    data.create_data()
    destination = "~/Desktop/py/wp"
    tes = WallPaper(data.data, destination)
    tes.main(output=False)


if __name__ == "__main__":
    main()

