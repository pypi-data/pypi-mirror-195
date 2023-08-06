# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chattr_event_bus',
 'chattr_event_bus.constants',
 'chattr_event_bus.consumers',
 'chattr_event_bus.scripts',
 'chattr_event_bus.serializers',
 'chattr_event_bus.services',
 'chattr_event_bus.validators']

package_data = \
{'': ['*'],
 'chattr_event_bus': ['schemas/analytics/*',
                      'schemas/campaign_engine/*',
                      'schemas/conversation_engine/*',
                      'schemas/ecommerce/*',
                      'schemas/ecommerce_subscription_engine/*',
                      'schemas/general/*',
                      'schemas/lists/*',
                      'schemas/messaging/*',
                      'schemas/sample_product/*',
                      'schemas/segment/*',
                      'schemas/sensus/*',
                      'schemas/subscriber_engine/*',
                      'schemas/subscriptions/*',
                      'schemas/test/*',
                      'schemas/vaportal/*']}

install_requires = \
['chattr-config==0.1.1',
 'faust-streaming>=0.10.4,<0.11.0',
 'jsonschema==4.17.3',
 'pytz>=2022.7.1,<2023.0.0']

setup_kwargs = {
    'name': 'chattr-event-bus',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chattr',
    'author_email': 'chattr23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
