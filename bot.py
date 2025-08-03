import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pandas as pd

# Read games from CSV file
multiplayer_games = pd.read_csv('games.csv')['game'].tolist()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="suggest")
async def suggest_game(ctx):
    game = random.choice(multiplayer_games)
    await ctx.send(f"🎮 You should play: **{game}** tonight!")

@bot.command(name="games")
async def list_games(ctx):
    games_str = "\n".join(f"- {game}" for game in multiplayer_games)
    await ctx.send(f"Here are some multiplayer games you can play:\n{games_str}")

@bot.command(name="spell")
async def category_suggest(ctx):
    """
    Suggest a game based on the names of the channels within the Spell Category.
    Usage: !spell
    """
    category_name = "🎮 Spell"

    # Find the category by name (case-insensitive)
    category = discord.utils.find(lambda c: c.name.lower() == category_name.lower() and isinstance(c, discord.CategoryChannel), ctx.guild.categories)
    if not category:
        await ctx.send(f"Category '{category_name}' not found.")
        return
    # Get all text and voice channels in the category
    channel_names = [ch.name for ch in category.channels if isinstance(ch, (discord.TextChannel, discord.VoiceChannel))]
    if not channel_names:
        await ctx.send(f"No channels found in category '{category_name}'.")
        return
    suggestion = random.choice(channel_names)
    await ctx.send(f"🎲 Random {category_name}: **{suggestion}**")


load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
