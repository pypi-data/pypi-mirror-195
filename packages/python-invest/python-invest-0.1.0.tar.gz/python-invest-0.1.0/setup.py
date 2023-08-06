# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_invest', 'python_invest.cli', 'python_invest.invest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'python-invest',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Python Invest\n\n![Python Invest Logo](./docs/images/logo.png "Python Invest Logo")\n\nFinancial data extraction with Python.\n\nThe Python Invest package is based on an unofficial data extraction API from the website [Investing.com](https://www.investing.com/). It\'s a package inspired by the amazing [Investpy](https://github.com/alvarobartt/investpy) library.\n\n<i>:warning:</i><b> This package consumes an unofficial open API and will validate the user\'s email before providing the data. After that, the user can consume all available services.</b>\n\nPython Invest its a Open Source package and Free to use, respecting the **MIT License**.\n\n\n## :material-list-status: Requirements\n\n:white_check_mark: Python >= 3.10\n\n## :hammer_and_wrench: Installation\n\n- pip\n\n```\n$ pip install python-invest\n```\n\n- poetry\n\n```\npoetry add python-invest\n```\n\n---\n\n## :chart_with_upwards_trend: Usage Examples\n\nGetting historical **BTC** data:\n\n```{.py3 linenums=1 hl_lines=5}\nfrom python_invest import Invest\n\ninv = Invest(\'youremail@email.com\')\n\ndata = inv.crypto.get_historical_data(\n        symbol=\'BTC\',\n        from_date=\'01/01/2023\',\n        to_date=\'01/02/2023\'\n    )\n```\n\nThe API can send a verification link to your email, it\'s a security measure you won\'t be charged for anything. If this happens, you will receive an error similar to this:\n\n```{hl_lines="3 5"}\nTraceback (most recent call last):\n File "...", line 5, in <module>\n    data = inv.crypto.get_historical_data(symbol=\'BTC\', from_date=\'01/01/2023\', to_date=\'01/02/2023\')\n    ...\nPermissionError: The Scrapper API sent to your email address the verification link. Please verify your email before run the code again.\n```\n\nIf you get this error: **Just open your email box and click on the verification link.**\n\nThe email would be a equal this:\n\n![Verification Email Link](./docs/images/emailValidation.png "Verification Email Link")\n\nAfter that, you can run the code:\n\n```{.py3 linenums=5}\ndata = inv.crypto.get_historical_data(\n        symbol=\'BTC\',\n        from_date=\'01/01/2023\',\n        to_date=\'01/02/2023\'\n    )\n\nprint(data)\n```\n```\n      Price      Open      High       Low     Vol Change        Date\n0  16,674.3  16,618.4  16,766.9  16,551.0  136027   0.34  01/02/2023\n1  16,618.4  16,537.5  16,621.9  16,499.7  107837   0.49  01/01/2023\n```\n\nThe default output is the [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).\n\n## :book: Documentation\n\nThe oficial [Documentation](https://pyinvest.readthedocs.io/en/latest/).\n\n## :computer: Social Medias\n* [Instagram](https://www.instagram.com/claudiogfez/)\n* [Linkedin](https://www.linkedin.com/in/clcostaf/)\n\n# :technologist: Author\n| [<img src="https://avatars.githubusercontent.com/u/83929403?v=4" width=120><br><sub>@clcostaf</sub>](https://github.com/clcosta) |\n| :---: |\n',
    'author': 'Claudio Lima',
    'author_email': 'clcostaf@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
