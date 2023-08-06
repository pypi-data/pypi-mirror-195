# UNITEST
import unittest

# MODULES
import numpy as np
from pathlib import Path
from PIL import Image

# KLARF_READER
from klarf_reader.klarf import Klarf

# WAFERMAP_PLOT
from wafermap_plot.models.defect_point import DefectPoint
from wafermap_plot.wafermap import WaferMapPlot

ASSETS_PATH: Path = Path(__file__).parent / "assets"


class TestKlarf(unittest.TestCase):
    def setUp(self) -> None:
        self.path_klarf_single_wafer = ASSETS_PATH / "J052SBN_8196_J052SBN-01.000"
        self.path_klarf_multi_wafers = ASSETS_PATH / "J237DTA_3236.000"

        self.path_image_klarf_multi_wafers = ASSETS_PATH / "img" / "J237DTA_3236.png"

    def test_wafermaps(self) -> None:
        # Given
        expected_img = Image.open(self.path_image_klarf_multi_wafers)
        expected_array = np.array(expected_img)

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)

        defect_points = [
            DefectPoint(
                defect_id=defect.id,
                point=(defect.point[0] / 1000, defect.point[1] / 1000),
                bin=index,
            )
            for index, defect in enumerate(content.wafers[0].defects)
        ]

        wafermap_plot = WaferMapPlot()
        wafermap_plot.plot(defect_points=defect_points)
        wafermap_plot.show()

        figure = wafermap_plot._figure
        figure.canvas.draw()
        array = np.array(figure.canvas.renderer.buffer_rgba())

        np.testing.assert_array_equal(expected_array, array)
