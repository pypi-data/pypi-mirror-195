# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quant_candles',
 'quant_candles.controllers',
 'quant_candles.exchanges',
 'quant_candles.exchanges.alpaca',
 'quant_candles.exchanges.binance',
 'quant_candles.exchanges.bitfinex',
 'quant_candles.exchanges.bitflyer',
 'quant_candles.exchanges.bitmex',
 'quant_candles.exchanges.bybit',
 'quant_candles.exchanges.coinbase',
 'quant_candles.exchanges.kucoin',
 'quant_candles.exchanges.upbit',
 'quant_candles.filters',
 'quant_candles.lib',
 'quant_candles.management',
 'quant_candles.management.commands',
 'quant_candles.migrations',
 'quant_candles.models',
 'quant_candles.models.candle_types',
 'quant_candles.serializers',
 'quant_candles.signals',
 'quant_candles.tests',
 'quant_candles.tests.controllers',
 'quant_candles.tests.lib',
 'quant_candles.tests.models',
 'quant_candles.tests.models.candle_types',
 'quant_candles.views']

package_data = \
{'': ['*']}

install_requires = \
['django-polymorphic',
 'djangorestframework',
 'httpx',
 'pandas',
 'pyarrow',
 'randomname']

setup_kwargs = {
    'name': 'django-quant-candles',
    'version': '0.1.2',
    'description': 'Django Quant Candles downloads and aggregate candlesticks from tick data',
    'long_description': '# What?\n\nDjango Quant Candles downloads and aggregate candlesticks from tick data.\n\n<img src="https://raw.githubusercontent.com/globophobe/django-quant-candles/main/docs/assets/volume-candles.png" />\n\n# Why?\n\nCandlesticks aggregated by `django-quant-candles` are informationally dense. Such data can be useful for analyzing financial markets. As an example, refer to ["Low-Frequency Traders in a High-Frequency World: A Survival Guide"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2150876) and ["The Volume Clock: Insights into the High Frequency Paradigm"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2034858). Lopez de Prado recommends volume bars, however they are are computationally expensive to generate.\n\nBy aggregating and filtering raw ticks, they can be computed faster, with little loss in precision.\n\nThis optional aggregation is by equal symbol, timestamp, nanoseconds and tick rule. As described in the accompanying project [cryptofeed-werks](https://github.com/globophobe/cryptofeed-werks), aggregating trades in this way can increase information, as they are either orders of size or stop loss cascades.\n\nAs well, the number of rows can be reduced by 30-50%\n\nBy filtering aggregated rows, for example only writing a row when an aggregated trade is greater than `significant_trade_filter >= 1000`, the number of rows can be reduced more.\n\n# How?\n\nWhenever possible, data is downloaded from the exchange\'s AWS S3 repositories. Otherwise, it is downloaded using their REST APIs. \n\nA database, preferably PostgreSQL, is required. Data is saved to the database after aggregation and filtering. \n\nCandles are aggregated at 1 minute intervals, and validated with the exchange\'s historical candle API.\n\n[Notes](https://github.com/globophobe/django-quant-candles/blob/main/NOTES.md).\n\nSupported exchanges\n-------------------\n\n:white_medium_square: Binance REST API (requires API key, which requires KYC)\n* <em style="font-size: 0.9em">Other exchanges validate trade data downloaded from exchanges using candle data provided by exchanges. However, I did not complete KYC, and as a resident of Japan am not currently able to do so. Support is incomplete. Pull requests are welcome.</em>\n\n:white_check_mark: Bitfinex REST API\n\n:white_check_mark: BitMEX REST API, and [S3](https://public.bitmex.com/) repository\n\n:white_check_mark: Bybit [S3](https://public.bybit.com/) repository. \n* <em style="font-size: 0.9em">The REST API is no longer paginated, so data may be delayed 24 hours or more.</em>\n\n:white_check_mark: Coinbase Pro REST API\n\nNote: Exchanges without paginated REST APIs or an S3 repository, will never be supported.\n\nInstallation\n------------\n\nFor convenience, `django-quant-candles` can be installed from PyPI:\n\n```\npip install django-quant-candles\n```\n\nDeployment\n----------\n\nFor deployment, there are Dockerfiles. As well, there are invoke tasks for deployment to Google Cloud Run. Just as easily, the demo could be deployed to AWS or a VPS.\n\nIf using GCP, it is recommended to use the Cloud SQL Auth proxy, and run the management commands to collect data from your local machine. Django Quant Candles will upload the trade data to the cloud.\n\n```\ncd demo\ninvoke start-proxy\npython proxy.py trades\n```\n\nThen, configure a Cloud Workflow to collect data in the cloud. There is an example workflow in the [invoke tasks](https://github.com/globophobe/django-quant-candles/blob/main/demo/tasks.py).\n\nEnvironment\n-----------\n\nTo use the scripts or deploy to GCP, rename `.env.sample` to `.env`, and add the required settings.\n',
    'author': 'Alex',
    'author_email': 'globophobe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/globophobe/django-quant-candles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
