# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talksheet']

package_data = \
{'': ['*']}

install_requires = \
['duckdb-engine>=0.6.9,<0.7.0',
 'duckdb>=0.7.1,<0.8.0',
 'langchain>=0.0.100,<0.0.101',
 'openai>=0.27.0,<0.28.0',
 'pandas>=1.5.3,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'textual>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['talksheet = talksheet.talksheet:app.run']}

setup_kwargs = {
    'name': 'talksheet',
    'version': '0.6.0',
    'description': 'Interact with flat files using natural languages',
    'long_description': '# Talksheet\n\nTalksheet is an AI-powered CLI tool for exploring data.\n\nIt can read data from local CSV files\n\n![local_csv_example](assets/pic_loca_csv.png)\n\nAnd from remote CSV files\n\n![remote_csv_example](assets/pic_remote_csv.png)\n\n\n## Installation\n\nTalksheet is available on PyPI. You can install it with pip:\n\n```bash\npip install talksheet\n```\n\n## Usage\n\nTalksheet is a CLI tool. You can run it with the `talksheet` command.\n\n```bash\nexport OPENAI_API_KEY=<your_openai_api_key>\n\ntalksheet\n```\n\n## Roadmap\n\n- Better UI/UX\n- Handle more data formats\n- Export results',
    'author': 'Daniel Palma',
    'author_email': 'danivgy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
