# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vrobbler',
 'vrobbler.apps.books',
 'vrobbler.apps.books.api',
 'vrobbler.apps.books.migrations',
 'vrobbler.apps.music',
 'vrobbler.apps.music.api',
 'vrobbler.apps.music.migrations',
 'vrobbler.apps.podcasts',
 'vrobbler.apps.podcasts.migrations',
 'vrobbler.apps.profiles',
 'vrobbler.apps.profiles.api',
 'vrobbler.apps.profiles.migrations',
 'vrobbler.apps.scrobbles',
 'vrobbler.apps.scrobbles.api',
 'vrobbler.apps.scrobbles.migrations',
 'vrobbler.apps.scrobbles.templatetags',
 'vrobbler.apps.sports',
 'vrobbler.apps.sports.api',
 'vrobbler.apps.sports.migrations',
 'vrobbler.apps.videogames',
 'vrobbler.apps.videos',
 'vrobbler.apps.videos.api',
 'vrobbler.apps.videos.migrations']

package_data = \
{'': ['*'],
 'vrobbler': ['templates/*',
              'templates/music/*',
              'templates/scrobbles/*',
              'templates/sports/*',
              'templates/videos/*'],
 'vrobbler.apps.scrobbles': ['static/css/*', 'static/images/*']}

install_requires = \
['Django>=4.0.3,<5.0.0',
 'Markdown>=3.3.6,<4.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'celery>=5.2.7,<6.0.0',
 'cinemagoer>=2022.12.27,<2023.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'dj-database-url>=0.5.0,<0.6.0',
 'django-allauth>=0.50.0,<0.51.0',
 'django-celery-results>=2.3.0,<3.0.0',
 'django-encrypted-field>=1.0.5,<2.0.0',
 'django-extensions>=3.1.5,<4.0.0',
 'django-filter>=21.1,<22.0',
 'django-markdownify>=0.9.1,<0.10.0',
 'django-mathfilters>=1.0.0,<2.0.0',
 'django-redis>=5.2.0,<6.0.0',
 'django-simple-history>=3.1.1,<4.0.0',
 'django-taggit>=2.1.0,<3.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'honcho>=1.1.0,<2.0.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'psycopg2>=2.9.3,<3.0.0',
 'pylast>=5.1.0,<6.0.0',
 'pysportsdb>=0.1.0,<0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'redis>=4.2.2,<5.0.0',
 'whitenoise>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['vrobbler = vrobbler.cli:main']}

setup_kwargs = {
    'name': 'vrobbler',
    'version': '0.11.12',
    'description': '',
    'long_description': 'None',
    'author': 'Colin Powell',
    'author_email': 'colin@unbl.ink',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
