# Trading Robot for IBKR and Tradovate

This project is a trading robot that connects to Interactive Brokers (IBKR) and Tradovate to automate trading strategies.

## Features

*   **Dual Broker Support**: Connects to both Interactive Brokers and Tradovate.
*   **Asset Class Specialization**: Trades options on IBKR and futures on Tradovate.
*   **Real-time Data**: Subscribes to real-time tick data from both brokers.
*   **Automated Trading**: Places orders based on a customizable trading strategy.
*   **Modular Design**: The project is structured with separate modules for each broker and a core module for the main logic, making it easy to extend and maintain.

## Project Structure

```
/
- ibkr_bot/
  - __init__.py
  - client.py         # IBKR client for connecting to TWS/Gateway
  - options_trader.py # Options trading logic for IBKR
- tradovate_bot/
  - __init__.py
  - client.py         # Tradovate client for WebSocket API
  - futures_trader.py # Futures trading logic for Tradovate
- core/
  - __init__.py
  - main.py           # Main application entry point
  - strategy.py       # Trading strategy logic
- tests/
  - __init__.py
  - test_strategy.py
  - test_ibkr_client.py
  - test_tradovate_client.py
- requirements.txt    # Python dependencies
- README.md           # This file
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Credentials:**

    This application requires credentials for both Interactive Brokers and Tradovate. It is recommended to use environment variables to store your credentials securely.

    **For Interactive Brokers:**
    The IBKR connection does not require a username and password in the code, but you need to have the Trader Workstation (TWS) or IB Gateway running and configured to accept API connections.

    **For Tradovate:**
    You need to set the following environment variables:
    ```bash
    export TRADOVATE_USERNAME="your_tradovate_username"
    export TRADOVATE_PASSWORD="your_tradovate_password"
    export TRADOVATE_DEVICE_ID="your_unique_device_id"
    ```
    You will also need to update the `tradovate_bot/client.py` to read these environment variables.

## Running the Bot

To run the trading bot, you need to execute the `core/main.py` file:

```bash
python core/main.py
```

**Note:** The bot is not fully implemented to run end-to-end yet. The `main.py` file contains the basic structure, but the main loop that connects the components is commented out as it cannot be run in a sandbox environment without live broker connections.

## Running the Tests

To run the unit tests, use the `unittest` module:

```bash
python -m unittest discover tests
```
