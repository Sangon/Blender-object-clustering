# Blender clustering

Simple clustering addon for blender. Currently only supports DBSCAN and OPTICS
More info: https://scikit-learn.org/stable/modules/clustering.html#clustering

## Getting Started

Running this addon requires Blender 2.80 and the scikit_learn python package. If you dont know how to make packages work in blender see the example below.

### Prerequisites

Python >=3.7.x
Blender >=2.80
[scikit_learn](https://pypi.org/project/scikit-learn/) >= 0.21.1

### How to make packages work in Blender 2.80

1. Install python 3.7.x. (Python 3.7.3, v3.7.3:ef4ec6ed12 was used while developing) and make sure its added to PATH.
2. Download Blender 2.80. Preferably the zipped/standalone version since we are going to modify it which might break some existing addons/functionality.
3. Delete the python folder under **%ProgramFiles%/Blender Foundation/2.80** or in the case of the standalone version where ever you installed it. This makes Blender fall back to the system python installation which in turn enables us to easily use packages in blender. If your blender won't open after this make sure you have a compatible python version (Blender 2.80 uses 3.7.0).

## Authors

* **Henri Hakala** - [Sangon](https://github.com/Sangon)
* **Joel Pesu** - [joelpesu](https://github.com/joelpesu)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details