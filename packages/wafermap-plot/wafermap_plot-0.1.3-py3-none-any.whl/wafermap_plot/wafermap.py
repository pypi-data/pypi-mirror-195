# MODULES
import numpy as np
from typing import List
from pathlib import Path

# MATPLOTLIB
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors

# WAFERMAP_PLOT
from wafermap_plot.models.defect_point import DefectPoint


class WaferMapPlot:
    def __init__(self):
        self._figure, self._ax = plt.subplots()

    def plot(
        self, defect_points: List[DefectPoint], cmap: str = "viridis"
    ) -> plt.Figure:

        x = np.linspace(-100, 100, 100)
        y = np.linspace(-100, 100, 100)

        X, Y = np.meshgrid(x, y)

        F = X**2 + Y**2 - 100 * 100

        self._ax.contour(X, Y, F, [0], colors="black")
        self._ax.set_aspect(1)

        self._ax.xaxis.set_visible(False)
        self._ax.yaxis.set_visible(False)

        plt.xlim(-110, 110)
        plt.ylim(-110, 110)

        unique_bins = sorted(set([defect_point.bin for defect_point in defect_points]))

        number_colors = len(unique_bins)

        cm = plt.get_cmap(cmap)
        cNorm = colors.Normalize(vmin=0, vmax=number_colors - 1)
        scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)

        self._ax.set_prop_cycle(
            color=[scalarMap.to_rgba(i) for i in range(number_colors)]
        )

        [
            self._ax.scatter(
                *zip(*[dp.point for dp in defect_points if dp.bin == unique_bin]),
                s=1,
                marker="s"
            )
            for unique_bin in unique_bins
        ]

    def show(self):
        self._figure.show()

    def save(self, path: Path):
        self._figure.savefig(path)

    @property
    def figure(self):
        return self._figure
