# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlexperimentscheduler', 'qctrlexperimentscheduler.predefined']

package_data = \
{'': ['*']}

install_requires = \
['qctrl-commons>=17.9.1,<18.0.0',
 'qctrl-visualizer>=4.5.0,<5.0.0',
 'qctrl>=21.0.0,<22.0.0']

extras_require = \
{':python_full_version >= "3.7.2" and python_version < "3.8"': ['numpy>=1.21.6,<2.0.0',
                                                                'networkx>=2.6,<2.7'],
 ':python_version >= "3.8"': ['networkx>=3.0,<4.0'],
 ':python_version >= "3.8" and python_version < "3.12"': ['numpy>=1.23.5,<2.0.0']}

setup_kwargs = {
    'name': 'qctrl-experiment-scheduler',
    'version': '0.1.0',
    'description': 'Q-CTRL Experiment Scheduler',
    'long_description': '# Q-CTRL Experiment Scheduler\n\nThe Q-CTRL Experiment Scheduler provides convenience functionality to use\nQ-CTRL software in a series of interdependent calibration experiments.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
