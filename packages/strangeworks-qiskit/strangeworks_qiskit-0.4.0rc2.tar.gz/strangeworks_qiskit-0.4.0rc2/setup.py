# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks_qiskit',
 'strangeworks_qiskit.backends',
 'strangeworks_qiskit.jobs',
 'strangeworks_qiskit.platform']

package_data = \
{'': ['*']}

install_requires = \
['qiskit<=0.40.0', 'strangeworks==0.4.0rc2']

setup_kwargs = {
    'name': 'strangeworks-qiskit',
    'version': '0.4.0rc2',
    'description': 'Strangeworks Qiskit SDK Extension',
    'long_description': '| ⚠️ | This SDK is currently in pre-release alpha state and subject to change. To get\nmore info or access to test features check out the\n[Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n\n# Strangeworks Qiskit Extension\n\nStrangeworks Python SDK extension for Qiskit.\n\nFor more information on using the SDK check out the\n[Strangeworks documentation](https://docs.strangeworks.com/).\n',
    'author': 'Strange Devs',
    'author_email': 'hello@strangeworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
