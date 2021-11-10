from .geometry import Ellipse, EllipticRing

import numpy as np


class EllipticalBody:
    def __init__(self, pos, a, b, theta=0, brightness=1):
        """
        An ellipse body object

        :param pos: Position of the center of the body
        :param a: semi-major axis of the ellipse
        :param b: semi-minor axis of the ellipse
        :param theta: Angle of rotation. (Degree)
        :param brightness: a value (corresponding to flux) between 0 and 1.
                           Or an array with n elements between 0 and 1. (Limb Darkening)
        """
        self.pos = pos
        self.a = a
        self.b = b
        self.theta = theta
        self.brightness = brightness

    def __str__(self) -> str:
        if isinstance(self.brightness, (list, np.ndarray)):
            br = [min(self.brightness), max(self.brightness)]
        else:
            br = self.brightness
        return f"EllipticalBody(pos={self.pos}, a={self.a}, b={self.b}, theta={self.theta}, brightness={br})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def bodies(self) -> list:
        """
        A list of body.

        The list would have one element (Ellipse) if there is not limb darkening.
        Otherwise n-1 element (EllipticRing) would be return. Where n is number of elements given in brightness

        :return: body as a list
        """
        if isinstance(self.brightness, (float, int)):
            return [Ellipse(self.pos, self.a, self.b, self.theta, self.brightness)]
        if isinstance(self.brightness, (list, np.ndarray)):
            a_s = np.linspace(self.a, 0, len(self.brightness))
            b_s = np.linspace(self.b, 0, len(self.brightness))
            a_s2use = np.column_stack((a_s[:-1], a_s[1:]))
            b_s2use = np.column_stack((b_s[:-1], b_s[1:]))

            return [
                EllipticRing(self.pos, a, b, self.theta, brightness)
                for a, b, brightness in zip(a_s2use, b_s2use, self.brightness)
            ]

        raise ValueError("Brightness problem")

    def move(self, point, relative=True) -> None:
        """
        Moves (changes the position of) the body

        :param point: Step to take or point to move. Depends on `relative`
        :param relative: Is the give point a step to take? Otherwise moves the ellipse to given point.
        """
        if relative:
            self.pos += point
        else:
            self.pos = point

    def reshape(self, a, b):
        """
        Reshapes the body

        :param a: new semi-major axis
        :param b: new semi-minor axis
        """
        self.a, self.b = a, b

    def rotate(self, theta, relative=True):
        """
        Rotates the ellipse about it's center by given angle or sets the angle of the body.

        :param theta: Angle in degrees
        :param relative: Is the give angle a step to rotate? Otherwise rotates the ellipse to given angle.
        """
        if relative:
            self.theta += theta
        else:
            self.theta = theta
