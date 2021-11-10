from .v3d import Point

from shapely import geometry as s_geometry
from shapely import affinity as s_affinity

from matplotlib import patches


class Ellipse:
    def __init__(self, pos: Point, a: float, b: float, theta: float = 0, brightness: float = 1) -> None:
        """
        An ellipse object

        :param pos: position of the center fo the ellipse
        :param a: semi-major axis of the ellipse
        :param b: semi-minor axis of the ellipse
        :param theta: Angle of rotation. (Degree)
        :param brightness: a value (corresponding to flux) between 0 and 1.
        """
        self.pos = pos
        self.a = a
        self.b = b
        self.theta = theta
        self.brightness = brightness

    def __str__(self) -> str:
        return f"Ellipse(pos={self.pos}, a={self.a}, b={self.b}, theta={self.theta}, brightness={self.brightness})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def geometry(self) -> s_geometry.Polygon:
        """
        Generates a shapely ellipse

        :return: A shapely Polygon
        """
        return s_affinity.rotate(
            s_affinity.scale(
                s_geometry.Point(self.pos.x - 0.5, self.pos.y - 0.5).buffer(1),
                self.a,
                self.b
            ),
            self.theta
        )

    def move(self, point: Point, relative=True) -> None:
        """
        Moves (changes the position of) the ellipse

        :param point: Step to take or point to move. Depends on `relative`
        :param relative: Is the give point a step to take? Otherwise moves the ellipse to given point.
        """
        if relative:
            self.pos += point
        else:
            self.pos = point

    def reshape(self, a: float, b: float) -> None:
        """
        Reshapes the ellipse

        :param a: new semi-major axis
        :param b: new semi-minor axis
        """
        self.a, self.b = a, b

    def rotate(self, theta: float, relative=True) -> None:
        """
        Rotates the ellipse about it's center by given angle or sets the angle of the ellipse.

        :param theta: Angle in degrees
        :param relative: Is the give angle a step to rotate? Otherwise rotates the ellipse to given angle.
        """
        if relative:
            self.theta += theta
        else:
            self.theta = theta

    def matplotlib_artist(self) -> patches.Ellipse:
        """
        Creates a matplotlib artist to be used on animation

        :return: An ellipse object that matplotlib understands
        """
        e = patches.Ellipse(xy=(self.pos.x, self.pos.y),
                            width=2 * self.a, height=2 * self.b,
                            angle=90 - self.theta)

        e.set_facecolor((self.brightness, self.brightness, self.brightness))
        e.set_edgecolor((1 - self.brightness, 1 - self.brightness, 1 - self.brightness))
        return e


class EllipticRing:
    def __init__(self, pos: Point, a_range: list, b_range: list, theta: float = 0, brightness: float = 1) -> None:
        """
        An ellipse object

        :param pos: The position of the center fo the ellipse
        :param a_range: a list of upper and lower value of the sami-major axis
        :param b_range: a list of upper and lower value of the sami-minor axis
        :param theta: Angle of rotation. (Degree)
        :param brightness: a value (corresponding to flux) between 0 and 1.
        """
        self.pos = pos
        self.a_range = a_range
        self.b_range = b_range
        self.theta = theta
        self.brightness = brightness

    def __str__(self) -> str:
        return f"EllipticRing(pos={self.pos}, arange={self.a_range}" \
               f", b_range={self.b_range}, theta={self.theta}, brightness={self.brightness})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def geometry(self) -> s_geometry.Polygon:
        """
        Generates a shapely ellipse ring

        :return: A shapely Polygon
        """
        outer = s_affinity.rotate(
            s_affinity.scale(
                s_geometry.Point(self.pos.x, self.pos.y).buffer(1),
                max(self.a_range),
                max(self.b_range)
            ),
            self.theta
        )

        inner = s_affinity.rotate(
            s_affinity.scale(
                s_geometry.Point(self.pos.x, self.pos.y).buffer(1),
                min(self.a_range),
                min(self.b_range)
            ),
            self.theta
        )
        return outer.difference(inner)

    def move(self, point: Point, relative=True) -> None:
        """
        Moves (changes the position of) the ellipse

        :param point: Step to take or point to move. Depends on `relative`
        :param relative: Is the give point a step to take? Otherwise moves the ellipse to given point.
        """
        if relative:
            self.pos += point
        else:
            self.pos = point

    def reshape(self, a_range: list, b_range: list) -> None:
        """
        Reshapes the ellipse

        :param a_range: a list of upper and lower value of the sami-major axis
        :param b_range: a list of upper and lower value of the sami-minor axis
        """
        self.a_range, self.b_range = a_range, b_range

    def rotate(self, theta: float, relative=True) -> None:
        """
        Rotates the ellipse about it's center by given angle or sets the angle of the ellipse.

        :param theta: Angle in degrees
        :param relative: Is the give angle a step to rotate? Otherwise rotates the ellipse to given angle.
        """
        if relative:
            self.theta += theta
        else:
            self.theta = theta

    def matplotlib_artist(self) -> patches.Ellipse:
        """
        Creates a matplotlib artist to be used on animation

        :return: An ellipse object that matplotlib understands
        """
        e = patches.Ellipse(xy=(self.pos.x, self.pos.y),
                            width=2 * max(self.a_range), height=2 * max(self.b_range),
                            angle=90 - self.theta)

        e.set_facecolor((self.brightness, self.brightness, self.brightness))
        e.set_edgecolor("none")
        return e
