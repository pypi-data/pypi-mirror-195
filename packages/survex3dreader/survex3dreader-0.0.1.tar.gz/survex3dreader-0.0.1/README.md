# survex-3d-reader

Import survex .3d files into Python objects.

Dumbed down version of https://github.com/patrickbwarren/qgis3-survex-import
without PyQt dependency.

Has only one funciton. Example use:

```Python
import survex3dreader

filename = "1623.3d"

data = survex3dreader.read_svx_file(filename)

```
