import numpy as np
import random
import math
from PIL import Image
from itertools import product
from datetime import datetime


class Wp:


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

class Data:

    def __init__(self, functions, rgb_ratio, screen_size=(1080, 1980), reverse=False):
        self.functions = functions
        self.rgb_ratio = rgb_ratio
        self.height, self.width = screen_size
        self.domain = math.pi*4
        self.max_brightness = 255
        self.max_diff_pix = 24
        self.initialise_vars()
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8 )
        self.reverse = reverse

    def initialise_vars(self): 
        self.f_range = self.get_range()
        self.max_ratio = self.max_brightness//(max(self.rgb_ratio))
        self.real_max_diff = self.f_range/(self.height/2) * self.max_diff_pix
     
        
    def get_range(self):
        return self.domain * (self.height/self.width)

    def assign_rgb(self, y, x):
        # modifying x&y to be in cartesian coordinates
        x = x - self.width/2
        y = self.height - y - self.height/2
        # modifying x&y to be in the right magnification
        x = self.domain/(self.width/2) * x 
        y = self.f_range/(self.height/2) * y 
        if self.any_in_range(y, x):
            difference = self.get_difference(y, x)
            if difference == 0:
                strength = self.max_ratio
            else:
                default = int(self.max_ratio * ((self.real_max_diff - difference)/self.real_max_diff))
                if difference <= self.real_max_diff/3:
                    strength = default
                else:
                    prob = random.random()
                    delta = difference/self.real_max_diff
                    if prob > delta:
                        strength = default
                    else:
                        strength = 0
            r, g, b = (i * strength for i in self.rgb_ratio)
        else:
            r, g, b = (0, 0, 0)
        return r, g, b
    
    def get_difference(self, y ,x):
        differences = []
        for function in self.functions:
            try:
                fx = function(x)
            except ValueError:
                continue
            if fx - self.real_max_diff <= y <= fx + self.real_max_diff:
                differences.append(abs(fx-y))
        if self.reverse:
            for function in self.functions:
                try:
                    fx = -function(x)
                except ValueError:
                    continue
                if fx - self.real_max_diff <= y <= fx + self.real_max_diff:
                    differences.append(abs(fx-y))
        return min(differences)

    def any_in_range(self, y, x):
        bools = []
        for function in self.functions:
            fx = function(x)
            if fx - self.real_max_diff <= y <= fx + self.real_max_diff:
                bools.append(True)
            else:
                bools.append(False)
        if self.reverse:
            for function in self.functions:
                fx = -function(x)
                if fx - self.real_max_diff <= y <= fx + self.real_max_diff:
                    bools.append(True)
                else:
                    bools.append(False)
        return any(bools)


        
    def create_data(self):
        for y, x in product([y for y in range(self.height)], [x for x in range(self.width)]):
            r, g, b = self.assign_rgb(y, x)
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
    data = Data(functions, rgb_ratio, reverse=False)
    data.create_data()
    destination = "~/Desktop/py/wp"
    tes = Wp(data.data, destination)
    tes.main(output=False)


if __name__ == "__main__":
    main()

