# Crypto Discord Bot

This is a Discord bot that provides various cryptocurrency-related functionalities, such as checking prices, market caps, volumes, and generating charts.

## Features

- Check the current price of a cryptocurrency.
- Check the market cap and rank of a cryptocurrency.
- Check the 24-hour trading volume of a cryptocurrency.
- Generate a chart for a cryptocurrency within a specified timeframe.
- Check the last 3 messages of a user in the server.

## Requirements

- Python 3.8+
- `ccxt`
- `discord.py`
- `requests`
- `pandas`
- `mplfinance`
- `python-dotenv`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/swoofz/crypto-discord-bot.git
    cd crypto-discord-bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your Discord bot token and other necessary environment variables:
    ```env
    DISCORD_TOKEN=your_discord_token
    PREFIX=!
    DISCORD_GUILD_ID=your_guild_id
    ```

## Usage

1. Run the bot:
    ```sh
    python main.py
    ```

2. Use the following commands in your Discord server:
    - `/price <symbol>`: Check the current price of a cryptocurrency.
    - `/marketcap <symbol>`: Check the market cap and rank of a cryptocurrency.
    - `/volume <symbol>`: Check the 24-hour trading volume of a cryptocurrency.
    - `/chart <symbol> <timeframe>`: Generate a chart for a cryptocurrency within a specified timeframe.
    - `/message_check <user_name>`: Check the last 3 messages of a user in the server.

## Example

```sh
/price BTC/USD
/marketcap BTC
/volume BTC/USD
/chart BTC/USD 1h
/message_check username