import numpy as np

from lcs import EllipticalBody, Point
from lcs import Binary


def sim():
    b = 0.15  # The b value of limb darkening
    brightness = (1 - b) + b * np.cos(
        np.linspace(np.pi / 2, 0, 100))  # 100 elements of brighness accoring to R.Hanbury et. al.
    star = EllipticalBody(Point(0, 0), 3, 3, 0, brightness)  # Primary component
    tno = EllipticalBody(Point(15, 0), 5, 5, 0, 0.1)  # secondary component

    bs = Binary(star, tno)  # the system
    lc = bs.simulate(Point(-15, 0), 0, 100) # Simulation and light curve

    print(lc)


if __name__ == '__main__':
    sim()
