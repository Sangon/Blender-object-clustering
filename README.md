# Blender clustering

Simple clustering addon for blender.

## Getting Started

Running this addon requires Blender 2.80 and the scikit_learn package. If you dont know how to make packages work in blender theres an example below. 

## How to make this addon run

1. Install python 3.7.x. (Python 3.7.3, v3.7.3:ef4ec6ed12 was used while developing) and make sure its added to PATH.
2. Download Blender 2.80. Preferably the zipped/standalone version since we are going to modify it which might break some existing addons/functionality.
3. Delete the python folder under **%ProgramFiles%/Blender Foundation/2.80** or in the case of the standalone version where ever you installed it. This makes Blender fall back to the system python installation which in turn enables us to easily use packages in blender. If your blender won't open after this make sure you have a compatible python version (Blender 2.80 uses 3.7.0).
4. Install the **scikit_learn** package. Easiest way to do this is by running  ``` pip install scikit_learn ```.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Henri Hakala** - [Sangon](https://github.com/Sangon)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details