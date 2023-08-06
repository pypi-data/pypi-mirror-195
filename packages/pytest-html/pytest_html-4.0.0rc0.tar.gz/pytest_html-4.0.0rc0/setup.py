# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_html']

package_data = \
{'': ['*'], 'pytest_html': ['resources/*', 'scripts/*']}

install_requires = \
['Jinja2>=3.0.0', 'pytest-metadata>=2.0.2', 'pytest>=7.0.0']

entry_points = \
{'pytest11': ['html = pytest_html.plugin']}

setup_kwargs = {
    'name': 'pytest-html',
    'version': '4.0.0rc0',
    'description': 'pytest plugin for generating HTML reports',
    'long_description': 'pytest-html\n===========\n\npytest-html is a plugin for `pytest <http://pytest.org>`_ that generates a HTML report for test results.\n\n.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg\n   :target: https://github.com/pytest-dev/pytest-html/blob/master/LICENSE\n   :alt: License\n.. image:: https://img.shields.io/pypi/v/pytest-html.svg\n   :target: https://pypi.python.org/pypi/pytest-html/\n   :alt: PyPI\n.. image:: https://img.shields.io/conda/vn/conda-forge/pytest-html.svg\n   :target: https://anaconda.org/conda-forge/pytest-html\n   :alt: Conda Forge\n.. image:: https://github.com/pytest-dev/pytest-html/workflows/gh/badge.svg\n   :target: https://github.com/pytest-dev/pytest-html/actions\n   :alt: CI\n.. image:: https://img.shields.io/requires/github/pytest-dev/pytest-html.svg\n   :target: https://requires.io/github/pytest-dev/pytest-html/requirements/?branch=master\n   :alt: Requirements\n.. image:: https://codecov.io/gh/pytest-dev/pytest-html/branch/master/graph/badge.svg?token=Y0myNKkdbi\n   :target: https://codecov.io/gh/pytest-dev/pytest-html\n   :alt: Codecov\n\nResources\n---------\n\n- `Documentation <https://pytest-html.readthedocs.io/en/latest/>`_\n- `Release Notes <https://pytest-html.readthedocs.io/en/latest/changelog.html>`_\n- `Issue Tracker <http://github.com/pytest-dev/pytest-html/issues>`_\n- `Code <http://github.com/pytest-dev/pytest-html/>`_\n\nContributing\n------------\n\nWe welcome contributions.\n\nTo learn more, see `Development <https://pytest-html.readthedocs.io/en/latest/development.html>`_\n\nScreenshots\n-----------\n\n.. image:: https://cloud.githubusercontent.com/assets/122800/11952194/62daa964-a88e-11e5-9745-2aa5b714c8bb.png\n   :target: https://cloud.githubusercontent.com/assets/122800/11951695/f371b926-a88a-11e5-91c2-499166776bd3.png\n   :alt: Enhanced HTML report\n',
    'author': 'Dave Hunt',
    'author_email': 'dhunt@mozilla.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pytest-dev/pytest-html',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
