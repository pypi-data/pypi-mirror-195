# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coinglass_api']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'coinglass-api',
    'version': '0.3.4',
    'description': 'Unofficial Python client for Coinglass API',
    'long_description': '# Coinglass API\n[![PyPi version](https://img.shields.io/pypi/v/coinglass-api)](https://pypi.python.org/pypi/coinglass-api/)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100//)\n[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110//)\n\n## Unofficial Python client for Coinglass API\n\nWrapper around the [Coinglass API](https://coinglass.com/pricing) to fetch data about the crypto markets.\nAll data is output in pandas DataFrames (single or multi-index) and all time series data uses a DateTimeIndex.\n\n**Note**: This is work in progress. Currently only supports the `indicator` API endpoint.\n\n![Example Plot](https://github.com/dineshpinto/coinglass-api/blob/main/examples/example_plot.jpg?raw=true)\n\n## Installation\n\n```bash\npip install coinglass-api\n```\n\n### or with poetry \n\n```bash\npoetry add coinglass-api\n```\n\n## Usage\n\n\n```python\nfrom coinglass_api import CoinglassAPI\n\ncg = CoinglassAPI(api_key="abcd1234")\n\n# Funding rate of ETH on dYdX\nfr_btc_dydx = cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")\n\n# Get average funding for BTC\nfr_avg_btc = cg.funding_average(symbol="BTC", interval="h4")\n\n# Get funding OHLC for ETHUSDT on Binance\nfr_ohlc_eth_binance = cg.funding_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")\n\n# Get aggregated OI OHLC data for BTC\noi_agg_eth = cg.open_interest_aggregated_ohlc(symbol="ETH", interval="h4")\n\n# Get OHLC liquidations data for ETHUSDT on dYdX\nliq_ohlc_eth_dydx = cg.liquidation_pair(ex="dYdX", pair="ETH-USD", interval="h4")\n\n# Get liquidation data for BTC\nliq_btc = cg.liquidation_symbol(symbol="BTC", interval="h4")\n\n# Get long/short ratios for BTC\nlsr_btc = cg.long_short_symbol(symbol="BTC", interval="h4")\n```\n\n## Examples\n\n```\n>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").head()\n```\n\n| <br/>time           | exchangeName<br/> | symbol<br/> | quoteCurrency<br/> | fundingRate<br/> |\n|:--------------------|:------------------|:------------|:-------------------|:-----------------|\n| 2022-08-22 08:00:00 | dYdX              | ETH         | USD                | -0.001151        |\n| 2022-08-22 16:00:00 | dYdX              | ETH         | USD                | 0.001678         |\n| 2022-08-23 00:00:00 | dYdX              | ETH         | USD                | 0.003743         |\n| 2022-08-23 08:00:00 | dYdX              | ETH         | USD                | 0.003561         |\n| 2022-08-23 16:00:00 | dYdX              | ETH         | USD                | 0.000658         |\n\n```\n>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").info()\n```\n\n```\n<class \'pandas.core.frame.DataFrame\'>\nDatetimeIndex: 500 entries, 2022-08-22 08:00:00 to 2023-02-04 16:00:00\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype  \n---  ------         --------------  -----  \n 0   exchangeName   500 non-null    object \n 1   symbol         500 non-null    object \n 2   quoteCurrency  500 non-null    object \n 3   fundingRate    500 non-null    float64\ndtypes: float64(1), object(3)\nmemory usage: 19.5+ KB\n```\n\n```\n>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").plot(y="fundingRate")\n```\n![funding_rate](https://github.com/dineshpinto/coinglass-api/blob/main/examples/funding_rate.jpg?raw=true)\n\n## Disclaimer\n\nThis project is for educational purposes only. You should not construe any such information or other material as legal,\ntax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation,\nendorsement, or offer by me or any third party service provider to buy or sell any securities or other financial\ninstruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the\nsecurities laws of such jurisdiction.\n\nUnder no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs,\nor liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.',
    'author': 'dineshpinto',
    'author_email': 'annual.fallout_0z@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dineshpinto/coinglass-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
