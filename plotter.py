import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def plot(self, X, Y, data, xlabel, ylabel, zlabel, title, zmin=None, zmax=None):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # set axis limits
        ax.set_xlim(min(X), max(X))
        ax.set_ylim(min(Y), max(Y))
        if zmin is not None and zmax is not None:
            ax.set_zlim(zmin, zmax)

        # create meshgrid and plot
        X, Y = np.meshgrid(X, Y)
        ax.plot_surface(X, Y, data, cmap='viridis', linewidth=0)

        # set title and labels
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)

        # show
        fig.show()
