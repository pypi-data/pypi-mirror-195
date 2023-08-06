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
    'version': '0.1.2',
    'description': '',
    'long_description': '# qabot\n\nQuery local csv files or databases with natural language queries powered by\n`langchain` and `openai`.\n\nWorks on local CSV files:\n\n![](.github/local_csv_query.png)\n\nas well as on real databases:\n\n![](.github/external_db_query.png)\n\n\n## Quickstart\n\nYou need to set the `OPENAI_API_KEY` environment variable to your OpenAI API key, \nwhich you can get from [here](https://platform.openai.com/account/api-keys).\n\nInstall the `qabot` command line tool using pip/poetry:\n\n\n```bash\n$ poetry install qabot\n```\n\nThen run the `qabot` command with either files or a database connection string:\n\n### Local CSV file/s\n\n```bash\n$ qabot -q "how many passengers survived by gender?" -f data/titanic.csv\n🦆 Loading data from files...\nLoading data/titanic.csv into table titanic...\n\nQuery: how many passengers survived by gender?\nResult:\nThere were 233 female passengers and 109 male passengers who survived.\n\n\n 🚀 any further questions? [y/n] (y): y\n\n 🚀 Query: what was the largest family who did not survive? \nQuery: what was the largest family who did not survive?\nResult:\nThe largest family who did not survive was the Sage family, with 8 members.\n\n 🚀 any further questions? [y/n] (y): n\n\n```\n\n### Existing database\n\nInstall any required drivers for your database, e.g. `pip install psycopg2-binary` for postgres.\n\nFor example to connect and query directly from the trains database in the [relational dataset repository](https://relational.fit.cvut.cz/dataset/Trains):\n\n```bash\n$ pip install mysqlclient\n\n$ qabot -d mysql+mysqldb://guest:relational@relational.fit.cvut.cz:3306/trains -q "what are the unique load shapes of cars, what are the maximum number of cars per train?" \nQuery: what are the unique load shapes of cars, what are the maximum number of cars per train?\nResult:\nThe unique load shapes of cars are circle, diamond, hexagon, rectangle, and triangle, and the maximum number of cars per train is 3.\n\n```\n\nNote you can also supply the database connection string via the environment variable\n`QABOT_DATABASE_URI`.\n\n#### Limit the tables\n\nYou can limit the tables that are queried by passing the `-t` flag. For example, to only query the `cars` table:\n\n```bash\n$ export QABOT_DATABASE_URI=mysql+mysqldb://guest:relational@relational.fit.cvut.cz:3306/trains\n$ qabot -q "what are the unique load shapes of cars?" -t cars\n\nThe unique load shapes of cars are circle, hexagon, triangle, rectangle, and diamond.\n```\n\n## See the intermediate steps and database queries\n\nUse the `-v` flag to see the intermediate steps and database queries:\n\n```bash\n$ qabot -d mysql+mysqldb://guest:relational@relational.fit.cvut.cz:3306/trains -q "what are the unique load shapes of cars, what are the maximum number of cars per train?" -v\nQuery: what are the unique load shapes of cars, what are the maximum number of cars per train?\nIntermediate Steps: \n  Step 1\n\n    list_tables_sql_db(\n      \n    )\n\n    Output:\n    trains, cars\n\n  Step 2\n\n    schema_sql_db(\n      trains, cars\n    )\n\n    Output:\n    CREATE TABLE trains (\n        id INTEGER(11) NOT NULL, \n        direction VARCHAR(4), \n        PRIMARY KEY (id)\n    )ENGINE=InnoDB DEFAULT CHARSET=latin1\n\n    SELECT * FROM \'trains\' LIMIT 3;\n    id  direction\n    1   east\n    2   east\n    3   east\n\n\n    CREATE TABLE cars (\n        id INTEGER(11) NOT NULL, \n        train_id INTEGER(11), \n        `position` INTEGER(11), \n        shape VARCHAR(255), \n        len VARCHAR(255), \n        sides VARCHAR(255), \n        roof VARCHAR(255), \n        wheels INTEGER(11), \n        load_shape VARCHAR(255), \n        load_num INTEGER(11), \n        PRIMARY KEY (id), \n        CONSTRAINT cars_ibfk_1 FOREIGN KEY(train_id) REFERENCES trains (id) ON DELETE CASCADE ON UPDATE CASCADE\n    )ENGINE=InnoDB DEFAULT CHARSET=latin1\n\n    SELECT * FROM \'cars\' LIMIT 3;\n    id  train_id        position        shape   len     sides   roof    wheels  load_shape      load_num\n    1   1       1       rectangle       short   not_double      none    2       circle  1\n    2   1       2       rectangle       long    not_double      none    3       hexagon 1\n    3   1       3       rectangle       short   not_double      peaked  2       triangle        1\n\n  Step 3\n\n    query_sql_db(\n      SELECT load_shape, MAX(load_num) FROM cars GROUP BY load_shape\n    )\n\n    Output:\n    [(\'circle\', 3), (\'diamond\', 1), (\'hexagon\', 1), (\'rectangle\', 3), (\'triangle\', 3)]\n\n\nResult:\nThe unique load shapes of cars are circle, diamond, hexagon, rectangle, and triangle, and the maximum number of cars per train is 3.\n\n```\n\n### Links\n- [Python library docs](https://langchain.readthedocs.io)\n- [Agent docs to talk to arbitrary apis via OpenAPI/Swagger](https://langchain.readthedocs.io/en/latest/modules/agents/agent_toolkits/openapi.html)\n- [Agents/Tools to talk SQL](https://langchain.readthedocs.io/en/latest/modules/agents/agent_toolkits/sql_database.html)\n- [Typescript library](https://hwchase17.github.io/langchainjs/docs/overview/)\n\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@hardbyte.nz',
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
