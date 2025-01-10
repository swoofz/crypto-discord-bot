import os
import ccxt
import discord
import requests
import pandas as pd
import mplfinance as mpf
from typing import Literal
from dotenv import load_dotenv
from discord.ext import commands


# Load Tokens/keys from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
GUILD_ID = discord.Object(id = os.getenv('DISCORD_GUILD_ID'))
EXCHANGE = ccxt.coinbase()

class Client(commands.Bot):
    async def on_ready(self): 
        print(f'Logged in as {self.user}')

        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to guild {GUILD_ID.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    def clear_synced_commands(self):
        self.tree.clear_commands(guild=GUILD_ID)


# Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = Client(intents=intents, command_prefix=PREFIX)

def get_currency_info(symbol):
    market = EXCHANGE.load_markets()
    df = pd.DataFrame(market)
    if not symbol in df: 
        print("Symbol not found")
        return
    
    return df[symbol]['info']


# Bot Commands
@client.tree.command(name="message_check", description="Check last 3 messages of user", guild=GUILD_ID)
async def message_check(interaction: discord.Interaction, user_name:str): # /message_check user
    members = client.get_all_members()
    user = next((member for member in members if member.name == user_name), None)

    if not user:
        await interaction.response.send_message(f"User not found: {user_name}", ephemeral=True)
        return

    if user.bot: 
        await interaction.response.send_message("Can't get messages from a bot.", ephemeral=True)
        return
    
    count = 0
    messages = []
    async for message in interaction.channel.history(limit=5000):
        if message.author == user:
            messages.append(message.content)
            count += 1
            if count == 3: break

    await interaction.response.send_message(f"{user.name.capitalize()} last 3 messages:```\n" + '\n'.join(messages) + "```", ephemeral=True)

@client.tree.command(name="price", description="Check the current price of a crypto currency and percentage change within the last 24 hours", guild=GUILD_ID)
async def price(interaction: discord.Interaction, symbol:str): # /price symbol
    currency_info = get_currency_info(symbol)
    price = float(currency_info['price'])
    precentage = float(currency_info['price_percentage_change_24h'])
    await interaction.response.send_message(f"{symbol}: ```Value: ${price:,.2f}\nPercentage Change: {precentage:.2f}%```")

@client.tree.command(name="marketcap", description="Check the current rank and market cap of a crypto currency", guild=GUILD_ID)
async def marketcap(interaction: discord.Interaction, symbol:str): # /marketcap symbol
    coin_id:str = get_currency_info(symbol)['base_name'].lower()
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    data = response.json()

    market_cap = data['market_data']['market_cap']['usd']
    rank = data['market_cap_rank']
    await interaction.response.send_message(f"```\t\t{coin_id.upper()}\nRank: {rank}\nMarket Cap: ${market_cap:,.2f}```")

@client.tree.command(name="volume", description="Check the current volume of a crypto currency within 24 hours", guild=GUILD_ID)
async def volume(interaction: discord.Interaction, symbol:str): # /volume symbol
    volume = float(get_currency_info(symbol)['volume_24h'])
    await interaction.response.send_message(f"{symbol}```Volume: {volume}```")
    
@client.tree.command(name="chart", description="Get a chart of the a crypto currency within timeframe speficied", guild=GUILD_ID)
async def chart(interaction: discord.Interaction, symbol:str, timeframe:Literal['1m', '5m', '15m', '1h', '1d']): # /chart symbol timeframe
    try:
        if symbol not in EXCHANGE.load_markets():
            raise ValueError(f'Symbol {symbol} not found in markets')
    except ValueError as e:
        opts = [ crypto for crypto in EXCHANGE.load_markets() if crypto.startswith(symbol) ]
        if len(opts) == 0:
            await interaction.response.send_message(f"Didn't find any market matches with symbol: {symbol}")
        else:
            choices = ", ".join(list(filter(lambda x: not ":" in x, opts)))
            await interaction.response.send_message(f"Did you mean one of these ```{choices}```")
    else:
        ohlcv = EXCHANGE.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        red = "#db0b1c"
        green = "#2abd2e"
        custom_style = mpf.make_mpf_style (
            base_mpf_style='mike',
            marketcolors=mpf.make_marketcolors(
                up=green, down=red, wick={'up': green, 'down': red}, edge={'up': green, 'down': red}
            )
        )

        mpf.plot(df, type='candle', style=custom_style, title=symbol, ylabel='Price', savefig=dict(fname='chart.png', dpi=100, bbox_inches='tight'))
        await interaction.response.send_message(file=discord.File('chart.png'))

# Run Bot
if __name__ == '__main__':
    client.run(TOKEN)