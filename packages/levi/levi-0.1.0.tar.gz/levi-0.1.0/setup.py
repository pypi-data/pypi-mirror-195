# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['levi']

package_data = \
{'': ['*']}

install_requires = \
['deltalake==0.7.0']

setup_kwargs = {
    'name': 'levi',
    'version': '0.1.0',
    'description': 'Delta Lake helper methods',
    'long_description': '# Levi\n\nDelta Lake helper methods.  No Spark dependency.\n\n## Installation\n\nInstall the latest version with `pip install levi`.\n\n## Delta File Stats\n\nThe `delta_file_stats` function provides information on the number of bytes in files of a Delta table.  Example usage:\n\n```python\nimport levi\nfrom deltalake import DeltaTable\n\ndt = DeltaTable("some_folder/some_table")\nlevi.delta_file_sizes(dt)\n\n# return value\n{\n    \'num_files_<1mb\': 345, \n    \'num_files_1mb-500mb\': 588,\n    \'num_files_500mb-1gb\': 960,\n    \'num_files_1gb-2gb\': 0, \n    \'num_files_>2gb\': 5\n}\n```\n\nThis output shows that there are 345 small files with less than 1mb of data and 5 huge files with more than 2gb of data.  It\'d be a good idea to compact the small files and split up the large files to make queries on this Delta table run faster.\n\nYou can also specify the boundaries when you invoke the function to get a custom result:\n\n```python\nlevi.delta_file_sizes(dt, ["<1mb", "1mb-200mb", "200mb-800mb", "800mb-2gb", ">2gb"])\n```\n',
    'author': 'Matthew Powers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
