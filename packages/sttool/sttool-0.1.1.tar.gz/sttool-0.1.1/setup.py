# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sttool']

package_data = \
{'': ['*'], 'sttool': ['templates/config/*', 'templates/simulation/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'parse>=1.19.0,<2.0.0',
 'pypsexec>=0.3.0,<0.4.0',
 'requests>=2.28.0,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'system-info>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['sttool = sttool.cli:cli']}

setup_kwargs = {
    'name': 'sttool',
    'version': '0.1.1',
    'description': 'Simple command line tools for testing tasks',
    'long_description': '# sttool\n\n\n\nSimple command line tools for testing tasks\n\n\n## Developing\n\nRun `make` for help\n\n    make install             # Run `poetry install`\n    make showdeps            # run poetry to show deps\n    make lint                # Runs bandit and black in check mode\n    make format              # Formats you code with Black\n    make test                # run pytest with coverage\n    make build               # run `poetry build` to build source distribution and wheel\n    make pyinstaller         # Create a binary executable using pyinstaller\n',
    'author': 'Darrin Fraser',
    'author_email': 'darrin.fraser@agcocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MrSuperbear/sttool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
