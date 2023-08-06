# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dstate', 'dstate.driver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dstate',
    'version': '0.1.0',
    'description': 'dstate is the library for distributed finite state machines',
    'long_description': "# dstate - distributed state machines\n\n[![Test dstate](https://github.com/aptakhin/dstate/actions/workflows/test.yml/badge.svg)](https://github.com/aptakhin/dstate/actions/workflows/test.yml)\n\ndstate is the library for distributed finite state machines. Library's mission is to add more clarity and maintainability to distributed applications, which can go finite state machine approach. It adds persistence and locks on the powerful [python-statemachine](https://github.com/fgmacedo/python-statemachine). With future releases timers support will be added.\n\n\n## Install\n\n```bash\n./shell/install-local.py\n# or\npoetry install --with dev --with python-statemachine --with driver\n```\n\n## Usage\n\nPretty unstable. No examples yet.\n\n[Tests file](./smoke_tests/test_dstate.py)\n\n## Dev\n\n```bash\n./shell/ruff.sh\n./shell/black.sh\n./shell/pytest-smoke.sh\n./shell/flake8.sh\n./shell/mypy.sh\n```\n\nAlso the same set is supported with `pre-commit`:\n\n```bash\npre-commit install\n```\n\nFast smoke pytests with watcher:\n\n```bash\n./shell/ptw.sh\n```\n\n\nFull environment tests require `docker compose`:\n\n```bash\n./full_tests/shell/beg-mongo.sh\n./shell/pytest-full.sh\n./full_tests/shell/end-mongo.sh\n```\n",
    'author': 'Alex Ptakhin',
    'author_email': 'me@aptakhin.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
