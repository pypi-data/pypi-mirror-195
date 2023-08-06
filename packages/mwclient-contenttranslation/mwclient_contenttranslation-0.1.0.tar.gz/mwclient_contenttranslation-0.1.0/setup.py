# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mwclient_contenttranslation']

package_data = \
{'': ['*']}

install_requires = \
['mwclient>=0.10.1,<0.11.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'mwclient-contenttranslation',
    'version': '0.1.0',
    'description': 'Wikipedia ContentTranslation (CXServer) API wrapper to be used with mwclient',
    'long_description': '# mwclient-contenttranslation\nThe wrapper of ContentTranslation (CXServer) API of Wikipedia to be used with mwclient.\n\n## Usage\nInstall via PyPI: `pip install mwclient-contenttranslation`\n```\nfrom mwclient import Site\nfrom mwclient_contenttranslation import CxTranslator\nsite = Site("en.wikipedia.org")\nsite.login(USERNAME, PASSWORD)\ntranslator = CxTranslator(site)\ntranslator.translate_text(["小熊維尼", "蜂蜜罐", "小熊維尼掉進蜂蜜罐"])\n# [\'Winnie the Pooh\', \'honey pot\', \'Winnie the Pooh fell into a jar of honey\']\n```\n\n## Disclaimer\nIntended for good use only. Never abuse it.\n',
    'author': 'Hung-I Wang',
    'author_email': 'whygowe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
