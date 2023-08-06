# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeroeventhub']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'zeroeventhub',
    'version': '0.0.9.1',
    'description': 'Broker-less event streaming over HTTP',
    'long_description': '# ZeroEventHub\n\nThis README file contains information specific to the Python port of the ZeroEventHub.\nPlease see the [main readme file](../../README.md) for an overview of what this project is about.\n\n## Client\n\nWe recommend that you store the latest checkpoint/cursor for each partition in the client\'s\ndatabase. Example of simple single-partition consumption. *Note about the example*:\n\n* Things starting with "my" is supplied by you\n* Things starting with "their" is supplied by the service you connect to\n\n```python\n# Step 1: Setup\ntheir_partition_count = 1 # documented contract with server\nzeh_session = requests.Session() # you can setup the authentication on the session\nclient = zeroeventhub.Client(their_service_url, their_partition_count, zeh_session)\n\n# Step 2: Load the cursors from last time we ran\ncursors = my_get_cursors_from_db()\nif not cursors:\n    # we have never run before, so we can get all events with FIRST_CURSOR\n    # (if we just want to receive new events from now, we would use LAST_CURSOR)\n    cursors = [\n        zeroeventhub.Cursor(partition_id, zeroeventhub.FIRST_CURSOR)\n        for partition_id in range(their_partition_count)\n    ]\n\n# Step 3: Enter listening loop...\npage_of_events = PageEventReceiver()\nwhile myStillWantToReadEvents:\n    # Step 4: Use ZeroEventHub client to fetch the next page of events.\n    client.fetch_events(\n        cursors,\n        my_page_size_hint,\n        page_of_events\n    )\n\n    # Step 5: Write the effect of changes to our own database and the updated\n    #         cursor value in the same transaction.\n    with db.begin_transaction() as tx:\n        my_write_effect_of_events_to_db(tx, page_of_events.events)\n\n        my_write_cursors_to_db(tx, page_of_events.latest_checkpoints)\n\n        tx.commit()\n\n    cursors = page_of_events.latest_checkpoints\n\n    page_of_events.clear()\n```\n\n## Development\n\nTo run the test suite, assuming you already have Python 3.10 or later installed and on your `PATH`:\n```sh\npip install poetry==1.3.1\npoetry config virtualenvs.in-project true\npoetry install --sync\npoetry run coverage run --branch -m pytest\npoetry run coverage html\n```\n\nThen, you can open the `htmlcov/index.html` file in your browser to look at the code coverage report.\n\nAlso, to pass the CI checks, you may want to run the following before pushing your changes:\n\n```sh\npoetry run pylint ./zeroeventhub/\npoetry run flake8\npoetry run mypy --check-untyped-defs ./tests/\npoetry run mypy --disallow-untyped-defs ./zeroeventhub/\n```\n',
    'author': 'Vipps MobilePay',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vippsas/zeroeventhub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
