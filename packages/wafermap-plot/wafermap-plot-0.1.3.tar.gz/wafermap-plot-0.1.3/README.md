The klarf-reader library is a python 3 lib that allow to parse and get klarf content as dataclass.

## Installing WaferMapPlot

To install wafermap-plot, if you already have Python, you can install with:

```
pip install wafermap-plot
```

## How to import WaferMapPlot

To access wafermap-plot ansd its functions import it in your Python code like this:

```
from wafermap_plot.wafermap import WaferMapPlot
```

## Reading the example code

To plot a wafermap you just have to supply a list of defect points.

```
path_save = 'demo/demo.png'

wafermap_plot = WaferMapPlot()
wafermap_plot.plot(defect_points=defect_points)
wafermap_plot.show()

wafermap_plot.save(path=path_save)
```
