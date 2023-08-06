# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abses', 'abses.algorithms', 'abses.tools']

package_data = \
{'': ['*']}

install_requires = \
['agentpy>=0.1.5,<0.2.0',
 'netcdf4>=1.6.2,<2.0.0',
 'pint>=0.20.1,<0.21.0',
 'prettytable>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'abses',
    'version': '0.1.3',
    'description': 'ABSESpy makes it easier to build artificial Social-ecological systems with real GeoSpatial datasets and fully incorporate human behaviour.',
    'long_description': '![pixel_abses2](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/pixel_abses2.svg)\n\n[![license](https://img.shields.io/github/license/songshgeo/absespy)](http://www.apache.org/licenses/) ![downloads](https://img.shields.io/github/downloads/songshgeo/absespy/total) ![codesize](https://img.shields.io/github/languages/code-size/songshgeo/absespy) ![tag](https://img.shields.io/github/v/tag/songshgeo/absespy)\n[![github](https://img.shields.io/badge/Website-SongshGeo-brightgreen.svg)](https://cv.songshgeo.com/) ![stars](https://img.shields.io/github/stars/songshgeo/absespy?style=social) [![twitter](https://img.shields.io/twitter/follow/shuangsong11?style=social)](https://twitter.com/shuangsong11)\n\n<!-- Language: [English Readme](#) | [简体中文](README_ch) -->\n\n`ABSESpy` makes it easier to build artificial **[Social-ecological systems](https://songshgeo.github.io/ABSESpy/docs/about/)** with real **GeoSpatial datasets** and fully incorporate **human behaviour**.\n\n## Why `ABSESpy`?\n\n**Several characteristics of Agent-Based model (ABM) make it an essential method for social-ecological systems (SES) research:**\n\n1. It focuses on the change of an SES over time from mutual adaptations of agents and their environments.\n2. its ability to generate emergent system-level outcomes from micro-level interactions and macro-level feedback.\n3. its ability to represent the diversity and heterogeneity of human and non-human actors and the spatial characteristics of an SES ...\n\nHowever, there is currently no modelling framework that **combines geo-spatial data and actor behaviour** (`actor` is the term for agents in the SES framework) well. `ABSESpy` is designed for spatial modelling that **couples human and nature** by:\n\n- Modelling environment for agents with **[geo data](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/nature/geodata/)**: `Shapefile`, `GeoTiff`, `NetCDF`.\n- Modelling **[human behaviour](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/human/CCR_example/)** of agents with [cognition, contagion and responses](https://songshgeo.github.io/ABSESpy/docs/background/#human-behaviour-framework).\n- Easily manage all [parameters, arguments](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/parameters/), and variables with a `yaml` settings file.\n\n## Install\n\nInstall with pip or your favourite PyPI package manager.\n```\npip install abses\n```\n\n## Basic usage & Documents\n\nYou can see how to use `ABSESpy` in these simple [tutorials](https://songshgeo.github.io/ABSESpy/tutorial/user_guide/):\n\n1. [Organize an Agent-based model](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/model/) and [easily manage parameters](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/parameters/).\n2. Using [geo-spatial data](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/nature/geodata/) as the environment.\n3. Simply applying a [human behavior framework](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/human/CCR_example/).\n\n<img src="https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/DQg0xJ.jpg" alt="Drawing" style="width: 600px;"/>\n\nAccess the [full Documentation here](https://songshgeo.github.io/ABSESpy/).\n\n## Get in touch\n\n- **For enthusiastic developers and contributors**, all contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n- **For SES researchers**, welcome to use this package in social-ecological system (SES) studies. If you have a model published, feel free to contribute it to our model library through [mailing list](https://groups.google.com/g/absespy).\n\nIf you need any help when using `ABSESpy`, don\'t hesitate to get in touch with us through:\n\n- Ask usage questions ("How to do?") on\xa0[_GitHub_\xa0Discussions](https://github.com/SongshGeo/ABSESpy/discussions).\n- Report bugs, suggest features or view the source code\xa0[on\xa0_GitHub_](https://github.com/SongshGeo/ABSESpy/issues).\n- For less well-defined questions or ideas or to announce other projects of interest to xarray users, use the\xa0[mailing list](https://groups.google.com/g/absespy).\n\n## License\n\nCopyright 2023, `ABSESpy` [Shuang Song](https://cv.songshgeo.com/)\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at\n\n[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\n\n`ABSESpy` bundles portions of `AgentPy`, `pandas`, `NumPy` and `Xarray`; the full text of these licenses is included in the licenses directory.\n',
    'author': 'Shuang Song',
    'author_email': 'songshgeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8.1',
}


setup(**setup_kwargs)
