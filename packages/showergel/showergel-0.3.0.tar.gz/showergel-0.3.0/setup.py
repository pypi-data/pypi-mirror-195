# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['showergel', 'showergel.commands', 'showergel.rest']

package_data = \
{'': ['*'], 'showergel': ['www/*', 'www/css/*', 'www/fonts/*', 'www/js/*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0',
 'Paste>=3.5.0,<4.0.0',
 'arrow>=1.1.0,<2.0.0',
 'click>=8,<9',
 'sphinx-rtd-theme>=0.5.1,<0.6.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['showergel = showergel.commands.main:showergel_cli']}

setup_kwargs = {
    'name': 'showergel',
    'version': '0.3.0',
    'description': 'Companion application for a Liquidsoap radio',
    'long_description': '=========\nShowergel\n=========\n\nShowergel is made to live aside Liquidsoap_:\nwhile a Liquidsoap script creates a radio stream,\nShowergel provides complementary features like playlist logging or occasional\nscheduling, with a (minimalist) Web interface.\nIt is made to run on a Linux box (with systemd) dedicated to your radio stream.\n\n**This is work in progress!** We\'ll welcome both contributions and comments,\nfeel free to write in the Issues or Discussions tabs.\n\nLicense: GPL3_.\n\nTake a look\n-----------\n\nIf you\'d like to see what it looks like,\ncheck out our `demo installation <https://showergel.fly.dev>`_.\nIt is only the visible part of Showergel,\nrunning on fake data.\nYou can also use it as a stub back-end\n`when developping that interface <https://showergel.readthedocs.io/en/latest/installing.html#install-for-front-end-development>`_.\n\n\nQuick install\n-------------\n\nOur automated script can install Liquidsoap and Showergel on an Ubuntu or Debian machine::\n\n    wget https://raw.githubusercontent.com/martinkirch/showergel/main/installers/showergel_quickstart.sh && chmod +x showergel_quickstart.sh && ./showergel_quickstart.sh\n\nThe script will need to run `sudo`.\nIt will start the radio, you should hear it as soon as you put sound files in the `~/Music` folder.\nIt will also register the radio as a system service, so the radio and its interface will start when the machine reboots, too.\n\nThis script installs our "quickstart" LiquidSoap script.\nAfter a first try we advise you to have a closer look to Showergel\'s documentation on https://showergel.readthedocs.io/. \n\n\n.. _Liquidsoap: https://www.liquidsoap.info/\n.. _GPL3: https://www.gnu.org/licenses/gpl-3.0.html\n',
    'author': 'Martin Kirchgessner',
    'author_email': 'martin.kirch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/martinkirch/showergel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
