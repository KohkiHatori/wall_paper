import numpy as np
import random
import math
from PIL import Image
from itertools import product
from datetime import datetime
from functions import *


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


class ImageDataMaker:

    def __init__(self, functions, rgb_ratio, screen_size=(1080, 1980), reverse=False):
        self.functions = [self.init_function(func) for func in functions]
        self.rgb_ratio = np.array(rgb_ratio)
        self.height, self.width = screen_size
        self.domain = math.pi * 4
        self.f_range = self.domain * (self.height / self.width)
        self.max_brightness = 255
        self.max_diff_pix = 24
        self.max_ratio = self.max_brightness // (max(self.rgb_ratio))
        self.cartesian_max_diff = self.f_range / (self.height / 2) * self.max_diff_pix
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.reverse = reverse

    def convert_function(self, function):
        """
        It transforms the input function to pixel format
        :param function:
        :return: Transformed function
        """
        return lambda x: (function((x+self.width/2)*(self.domain/self.width)) + self.height/2) * (-self.height/self.f_range)

    def init_function(self, function):
        """
        This function initializes the input function
        :param function:
        :return: Initialized function
        """
        function = self.convert_function(function)
        function = np.vectorize(function)
        return function

    def _get_strength(self, difference):
        if difference == 0:
            return self.max_ratio
        default = int(self.max_ratio * ((self.cartesian_max_diff - difference) / self.cartesian_max_diff))
        if difference <= self.cartesian_max_diff / 3:
            return default
        prob = random.random()
        delta = difference / self.cartesian_max_diff
        if prob > delta:
            return default
        return 0

    def assign_rgb(self, y, x):
        # modifying x&y to be in cartesian coordinates
        x = x - self.width / 2
        y = - (y - self.height / 2)
        # modifying x&y to be in the right magnification
        x = self.domain / (self.width / 2) * x
        y = self.f_range / (self.height / 2) * y
        difference = self.get_difference(y, x)
        strength = self._get_strength(difference)
        return self.rgb_ratio * strength

    def _get_ys(self):
        """
        Get range of y for each x value
        :return:
        """
        x = np.arange(0, self.width, 1)
        vec_int = np.vectorize(int)
        y_actual = np.array([vec_int(func(x)) for func in self.functions])
        print(y_actual[0][990])
        y_upper = y_actual + self.cartesian_max_diff
        y_lower = y_actual - self.cartesian_max_diff
        y_ranges = np.transpose(np.array([y_lower, y_upper]))
        return y_ranges

    def create_data(self):
        y_ranges = self._get_ys()




def main():
    functions = [math.tan]
    rgb_ratio = (1, 4, 2)
    data = ImageDataMaker(functions, rgb_ratio, reverse=False)
    data.create_data()
    destination = "~/Desktop/py/wp"
    # tes = WallPaper(data.data, destination)
    # tes.main(output=False)


if __name__ == "__main__":
    main()
