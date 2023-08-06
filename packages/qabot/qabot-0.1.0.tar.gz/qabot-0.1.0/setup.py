# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qabot']

package_data = \
{'': ['*']}

install_requires = \
['duckdb-engine>=0.6.9,<0.7.0',
 'langchain>=0.0.100,<0.0.101',
 'openai>=0.27.0,<0.28.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'rich>=13.3.1,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['qabot = qabot.cli:run']}

setup_kwargs = {
    'name': 'qabot',
    'version': '0.1.0',
    'description': '',
    'long_description': '# qabot\n\nQuery local csv files or databases with natural language queries powered by\n`langchain` and `openai`.\n\n## Quickstart\n\nYou need to set the `OPENAI_API_KEY` environment variable to your OpenAI API key, \nwhich you can get from [here](https://platform.openai.com/account/api-keys).\n\nInstall the `qabot` command line tool using poetry:\n\n\n```bash\n$ poetry install\n\n$ qabot -q "how many passengers survived by gender?" -f data/titanic.csv\n🦆 Loading data from files...\nLoading data/titanic.csv into table titanic...\n\nQuery: how many passengers survived by gender?\nResult:\nThere were 233 female passengers and 109 male passengers who survived.\n\n\n 🚀 any further questions? [y/n] (y): y\n\n 🚀 Query: what was the largest family who did not survive? \nQuery: what was the largest family who did not survive?\nResult:\nThe largest family who did not survive was the Sage family, with 8 members.\n\n 🚀 any further questions? [y/n] (y): n\n\n```\n\n## Connect to a live database:\n\nInstall any required drivers for your database, e.g. `pip install psycopg2-binary` for postgres.\n\nFor example to connect and query directly from the trains database in the [relational dataset repository](https://relational.fit.cvut.cz/dataset/Trains):\n\n```bash\n$ pip install mysqlclient\n\n$ qabot -d mysql+mysqldb://guest:relational@relational.fit.cvut.cz:3306/trains -q "what are the unique load shapes of cars, what are the maximum number of cars per train?" \nQuery: what are the unique load shapes of cars, what are the maximum number of cars per train?\nResult:\nThe unique load shapes of cars are circle, diamond, hexagon, rectangle, and triangle, and the maximum number of cars per train is 3.\n\n```\n\n### Links\n- [Python library docs](https://langchain.readthedocs.io)\n- [Agent docs to talk to arbitrary apis via OpenAPI/Swagger](https://langchain.readthedocs.io/en/latest/modules/agents/agent_toolkits/openapi.html)\n- [Agents/Tools to talk SQL](https://langchain.readthedocs.io/en/latest/modules/agents/agent_toolkits/sql_database.html)\n- [Typescript library](https://hwchase17.github.io/langchainjs/docs/overview/)\n\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@thorne.link',
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
