# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mandybrot']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pillow>=9.4.0,<10.0.0', 'tdqm>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'mandybrot',
    'version': '0.0.0',
    'description': 'Plot the magical Mandelbrot set.',
    'long_description': "# Publish\n\nFinally, let's be brave and publish our package to PyPI.\nThere's no good reason for you not to do this, as it's free and easy to do, and it's an awesome thing to be able to say you've done!\n\n## 0 - Create or log in to PyPI\n\nNext, we need to create an account on PyPI, or log in if we already have one.\nYou can do this at [https://pypi.org/account/register/](https://pypi.org/account/register/).\n\n## 1 - Create an API token\n\nGo to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/) and create a new API token.\nMake sure to copy the token somewhere safe, as you won't be able to see it again.\n\n## 2 - Add the token to Poetry\n\n```bash\npoetry config pypi-token.pypi your-token-you-just-created\n```\n\n## 3 - Build\n\nNow we need to build the package.\n\n```bash\npoetry build\n```\n\n## 4 - Publish\n\nRun the following command to publish the package to PyPI:\n\n```bash\npoetry publish\n```\n\n---\n\n**Note**\n\nThe name you give your package must be unique on PyPI.\nIf you try to publish a package with a name that already exists, you'll get an error.\n\n---\n",
    'author': 'FreddyWordingham',
    'author_email': 'freddy@digilab.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
