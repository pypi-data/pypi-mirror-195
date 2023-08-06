# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['restricted_partition']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'restricted-partition',
    'version': '0.1.1',
    'description': 'Integer partitions with an optional max length',
    'long_description': '# Restricted Partition\n\nA restricted partition is the subset of an integer partition with only partitions at\nor below a certain length.\n\n~~~python\nfrom restricted_partition import iter_partition\n\niter_partition(5)\n\n# [1, 1, 1, 1, 1]\n# [1, 1, 1, 2]\n# [1, 1, 3]\n# [1, 2, 2]\n# [1, 4]\n# [2, 3]\n# [5]\n\niter_partition(5, 3)\n\n# [1, 1, 3]\n# [1, 2, 2]\n# [1, 4]\n# [2, 3]\n# [5]\n~~~\n\nUses the accel_asc algorithm (thank you, Jerome Kelleher), so it is pretty speedy in pure Python.\n\nI found the algorithm at https://jeromekelleher.net/generating-integer-partitions.html.\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
