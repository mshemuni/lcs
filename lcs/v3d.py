from __future__ import annotations
import math
from typing import Union


class Point:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        A point object
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __neg__(self) -> Point:
        return self.mult(-1)

    def __pos__(self) -> Point:
        return self

    def __abs__(self) -> Point:
        return Point(abs(self.x), abs(self.y))

    def __add__(self, other: Point) -> Point:
        return self.add(other)

    def __sub__(self, other: Point) -> Point:
        return self.sub(other)

    def __mul__(self, other: Union[float, int]) -> Point:
        return self.mult(other)

    def __rmul__(self, other: Union[float, int]) -> Point:
        return self.mult(other)

    def __truediv__(self, other: Union[float, int]) -> Point:
        return self.div(other)

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def add(self, other: Point) -> Point:
        """
        Adds two point

        :param other: point to be added to self
        :return: sum of points (self + other)
        """
        if not isinstance(other, Point):
            raise ValueError("other must be a point")
        return Point(self.x + other.x, self.y + other.y)

    def sub(self, other: Point) -> Point:
        """
        Subtracts two point

        :param other:  point to be subtracted from self
        :return: difference of points (self - other)
        """
        if not isinstance(other, Point):
            raise ValueError("other must be a point")
        return self.add(-other)

    def mult(self, scalar: Union[float, int]) -> Point:
        """
        Multiplies a numeric with a point

        :param scalar: scalar to be multiplied by self
        :return: new multiplied point (scalar * self)
        """
        if not isinstance(scalar, (float, int)):
            raise ValueError("scalar must be a numeric")
        return Point(scalar * self.x, scalar * self.y)

    def div(self, scalar: Union[float, int]) -> Point:
        """
        Divids point with a numeric

        :param scalar: scalar for self to be divided by
        :return: new divided point (self / scalar)
        """
        if not isinstance(scalar, (float, int)):
            raise ValueError("scalar must be a numeric")
        return self.mult(1/ scalar)

    def dist(self, other: Point = None) -> Union[float, int]:
        """
        Calculates distace between two points

        :param other: Other point for distance to be calculated from it and self
        :return: distance (|self - other|)
        """
        other = other if other is not None else Point()
        if not isinstance(other, Point):
            raise ValueError("other must be a point or None")
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def to_polar(self) -> tuple[Union[float, int], Union[float, int]]:
        """
        Calculates polar coordinates of point

        :return: radius and angle
        """
        return self.dist(), math.degrees(math.atan2(self.y, self.x))

    def from_polar(self, r: Union[float, int], theta: Union[float, int]) -> Point:
        """
        Calculates cartesian coordinates of given polar coordinates

        :param r: radius
        :param theta: the angle
        :return: a point on the given coordinates
        """
        if not isinstance(r, (float, int)):
            raise ValueError("r must be a numeric")

        if not isinstance(theta, (float, int)):
            raise ValueError("theta must be a numeric")

        return Point(r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)))


class Vector:
    def __init__(self, point: Point) -> None:
        """
        A vector object

        :param point: point that vector is described by
        """
        self.point = point

    def __str__(self) -> str:
        return f"Vector({self.point})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: Vector) -> Vector:
        return self.add(other)

    def __sub__(self, other: Vector) -> Vector:
        return self.sub(other)

    def __neg__(self) -> Vector:
        return self.mult(-1)

    def __pos__(self) -> Vector:
        return self

    def __abs__(self) -> Vector:
        return Vector(abs(self.point))

    def __mul__(self, other: Union[float, int]) -> Vector:
        return self.mult(other)

    def __rmul__(self, other: Union[float, int]) -> Vector:
        return self.mult(other)

    def __truediv__(self, other: Union[float, int]) -> Vector:
        return self.div(other)

    def __eq__(self, other: Union[float, int]) -> Vector:
        return self.point == other.point

    def mag(self) -> Union[float, int]:
        """
        Calculates magnitude of the vector

        :return: Magnitude of the vector
        """
        r, _ = self.point.to_polar()
        return r

    def dot(self, other: Vector) -> Union[float, int]:
        """
        Calculates dot product of two vector

        :param other: The other vector to calculate dot product
        :return: dot product of other and this vector (other . self)
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        return self.point.x * other.point.x + self.point.y * other.point.y

    def mult(self, scalar: Union[float, int]) -> Vector:
        """
        Multiplies a numeric with a vector

        :param scalar: scalar to be multiplied by self
        :return: new multiplied vector (scalar * self)
        """
        if not isinstance(scalar, (float, int)):
            raise ValueError("scalar must be a numeric")
        return Vector(scalar * self.point)

    def div(self, scalar: Union[float, int]) -> Vector:
        """
        Divids vector with a numeric

        :param scalar: scalar for self to be divided by
        :return: new divided vector (self / scalar)
        """
        if not isinstance(scalar, (float, int)):
            raise ValueError("scalar must be a numeric")
        return Vector(self.point / scalar)

    def add(self, other: Vector) -> Vector:
        """
         Adds two vectors

        :param other: vector to be added to self
        :return: sum of vectors (self + other)
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        return Vector(self.point + other.point)

    def sub(self, other: Vector) -> Vector:
        """
        Subtracts two vectors

        :param other:  vector to be subtracted from self
        :return: difference of vectors (self - other)
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        return Vector(self.point - other.point)

    def heading(self) -> Union[float, int]:
        """
        Calculates the direction of a vector

        :return: angle of direction of vector (self)
        """
        _, theta = self.point.to_polar()
        return theta

    def angle_between(self, other: Vector) -> Union[float, int]:
        """
        Calculates the angle between two vectors

        :param other: vector to calculate angle between
        :return: angle between other and self  (other v self)
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        theta = math.atan2(other.point.y * self.point.x - other.point.x * self.point.y,
                           other.point.x * self.point.x + other.point.y * self.point.y)

        return math.degrees(theta)

    def unit(self) -> Vector:
        """
        Calculates the unit vector

        :return: a unit vector (|self|)
        """
        return self / self.mag()

    def rotate(self, angle: Union[float, int]) -> Vector:
        """
        Rotates a vector about another one by given angle

        :param angle: Angle of rotration
        :return: new rotated vector
        """
        if not isinstance(angle, (float, int)):
            raise ValueError("Angle must be numeric")
        r, theta = self.point.to_polar()
        new_theta = theta + angle
        return Vector(Point().from_polar(r, new_theta))

    def is_perpendicular(self, other: Vector) -> bool:
        """
        Checks if two vectors are perpendicular

        :param other: Other vector to be checked with
        :return: True of Falsity of the perpendicularity
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        return self.dot(other) < 0.000001

    def is_parallel(self, other: Vector) -> bool:
        """
        Checks if two vectors are parallel

        :param other: Other vector to be checked with
        :return: True of Falsity of the parallelism
        """
        if not isinstance(other, Vector):
            raise ValueError("other must be a vector")
        return self.heading() % 180 == other.heading() % 180
