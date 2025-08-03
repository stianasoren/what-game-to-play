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
    """
    Get a random game suggestion from the list of multiplayer games.
    Usage: !suggest
    """
    game = random.choice(multiplayer_games)
    await ctx.send(f"🎮 You should play: **{game}** tonight!")

@bot.command(name="games")
async def list_games(ctx):
    """
    Display a list of all available multiplayer games.
    Usage: !games
    """
    # Format games in a single column with alternating emojis for better mobile readability
    games_str = "\n".join(f"🎮 {game}" for game in sorted(multiplayer_games))
    # Split message if it's too long for Discord (2000 char limit)
    if len(games_str) > 1900:  # Leave room for the header text
        messages = []
        current_msg = "Here are some multiplayer games you can play:\n"
        for game in sorted(multiplayer_games):
            line = f"🎮 {game}\n"
            if len(current_msg) + len(line) > 1900:
                messages.append(current_msg)
                current_msg = line
            else:
                current_msg += line
        messages.append(current_msg)
        for msg in messages:
            await ctx.send(msg)
    else:
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

@bot.command(name="add")
async def add_game(ctx, *, game_name: str):
    """
    Add a new game to the list.
    Usage: !add <game_name>
    """
    if game_name in multiplayer_games:
        await ctx.send(f"Game '{game_name}' is already in the list.")
        return
    multiplayer_games.append(game_name)
    pd.DataFrame(multiplayer_games, columns=['game']).to_csv('games.csv', index=False)
    await ctx.send(f"Game '{game_name}' has been added to the list.")

@bot.command(name="remove")
async def remove_game(ctx, *, game_name: str):
    """
    Remove a game from the list.
    Usage: !remove <game_name>
    """
    if game_name not in multiplayer_games:
        await ctx.send(f"Game '{game_name}' is not in the list.")
        return
    multiplayer_games.remove(game_name)
    pd.DataFrame(multiplayer_games, columns=['game']).to_csv('games.csv', index=False)
    await ctx.send(f"Game '{game_name}' has been removed from the list.")

load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
