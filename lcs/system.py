from .v3d import Point

import numpy as np

from matplotlib import pyplot as plt


class Binary:
    def __init__(self, bodyA, bodyB) -> None:
        """
        A system of two bodies

        :param bodyA: The A component of the system
        :param bodyB: The B component of the system
        """
        self.bodyA = bodyA
        self.bodyB = bodyB

    def __str__(self) -> str:
        return f"A={self.bodyA}, B={self.bodyB}"

    def __repr__(self) -> str:
        return self.__str__()

    def get_mag_A(self) -> float:
        """
        Flux of component A
        area of each element in list body * its brightness

        :return: total flux of the component A
        """
        if isinstance(self.bodyA.brightness, (float, int)):
            brtns = [self.bodyA.brightness]
        else:
            brtns = self.bodyA.brightness

        return sum(
            [
                b.geometry.area * br
                for b, br in zip(self.bodyA.bodies, brtns)
            ]
        )

    def get_mag_B(self) -> float:
        """
        Flux of component B
        area of each element in list body * its brightness

        :return: total flux of the component B
        """
        if isinstance(self.bodyB.brightness, (float, int)):
            brtns = [self.bodyB.brightness]
        else:
            brtns = self.bodyB.brightness

        return sum(
            [
                b.geometry.area * br
                for b, br in zip(self.bodyB.bodies, brtns)
            ]
        )

    def get_total_mag(self) -> float:
        """
        Flux of the system
        area of each element in list body * its brightness
        eclipses are taken into account.

        :return: total flux of the system
        """
        b_mag = self.get_mag_B()

        if isinstance(self.bodyA.brightness, (float, int)):
            brtns = [self.bodyA.brightness]
        else:
            brtns = self.bodyA.brightness

        a_mag = sum(
            [
                b.geometry.difference(self.bodyB.bodies[-1].geometry).area * br
                for b, br in zip(self.bodyA.bodies, brtns)
            ]
        )

        return b_mag + a_mag

    def show(self, save_to: bool = None) -> None:
        """
        Shows the current status of the system
        """
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        for st in self.bodyA.bodies:
            ax.add_artist(st.matplotlib_artist())

        for t in self.bodyB.bodies:
            ax.add_artist(t.matplotlib_artist())

        plt.xlim([-20, 20])
        plt.ylim([-20, 20])
        if save_to is not None:
            plt.savefig(f"{save_to}/sim.png")
        else:
            plt.show()

    def simulate(self, to: Point, angle: float, step: int, save_to: bool =None) -> np.ndarray:
        """
        A simulation

        :param to: Where the component B must move to
        :param angle: How much the component B must rotate
        :param step: Time resolution.
        :param save_to: save frames of matplotlib to this location
        :return: The light curve
        """
        xs = np.linspace(self.bodyB.pos.x, to.x, step)
        ys = np.linspace(self.bodyB.pos.y, to.y, step)
        angs = np.linspace(self.bodyB.theta, angle, step)

        upper_x_lims = [
            -max(abs(xs)) - 10, max(abs(xs) + 10)
        ]

        ret = []

        for it, (x, y, ang) in enumerate(zip(xs, ys, angs)):
            print(f"{100 * (it + 1) / step}% Done")
            self.bodyB.move(Point(x, y), relative=False)
            self.bodyB.rotate(ang, relative=False)

            ret.append([it, self.get_total_mag()])

            if save_to is not None:
                plt.cla()
                fig, (ax1, ax2) = plt.subplots(2)

                for st in self.bodyA.bodies:
                    ax1.add_artist(st.matplotlib_artist())

                for tno in self.bodyB.bodies:
                    ax1.add_artist(tno.matplotlib_artist())

                ax1.set_xlim(upper_x_lims)
                ax1.set_ylim([upper_x_lims[0] / 2, upper_x_lims[1] / 2])

                to_plot = np.array(ret)
                ax2.plot(to_plot[:, 0], to_plot[:, 1])

                plt.savefig(f"{save_to}/{str(it).zfill(8)}.png")

        return np.array(ret)
