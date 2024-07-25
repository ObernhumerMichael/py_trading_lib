> WARNING: This project is under very active development and major changes are expected to occur. In the current state the project does not work yet!

# Overview

Welcome to the `py_trading_lib`, your ultimate tool for simplifying the creation and management of cryptocurrency trading bots.
This project is designed to streamline the entire process, making it accessible for both beginners and experienced developers.

# Features

- **Live Trading:** Seamlessly execute trades in real-time across multiple cryptocurrency exchanges.
- **Backtesting:** Test your trading strategies against historical data to evaluate their performance before deploying them live.
- **Charting:** Visualize your trading strategies and market data with integrated charting capabilities.
- **Telegram Bot Integration:** Receive real-time notifications and interact with your trading bot via Telegram messenger.
- **Extensibility:** Easily extend the library with your custom indicators and strategies to tailor the bot to your specific needs.

# Technical indicators

The technical indicators are calculated with the help of [pandas_ta](https://github.com/twopirllc/pandas-ta).
If you want to know more about how a specific indicator is calculated or what each property does exactly have a look at the corresponding doc from `pandas_ta`.
This can be done by viewing the help page:
```python
import pandas_ta as ta
help(ta.sma)
```

For other details please refer to the official website: [https://twopirllc.github.io/pandas-ta](https://twopirllc.github.io/pandas-ta)


# Developers

## Installation and Setup

You have to set up the virtual python environment.
Use the commands below in the project root folder.

```sh
python -m venv venv

# On Linux
source venv/bin/activate

# On Windows
# venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

## When finished

Use the following command to exit the virtual environment.

```sh
deactivate
```

## Tests

The project uses [pytest](https://docs.pytest.org) for testing. 
To run the tests just execute:

```sh
pytest
```
