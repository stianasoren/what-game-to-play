import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pandas as pd
from typing import Optional


# Helper: load games CSV with optional tags column. If no tags column exists,
# create an empty tags column. Tags are stored lowercase and as a comma-separated string.
def load_games_df() -> pd.DataFrame:
    try:
        df = pd.read_csv('games.csv', header=0)
        # If CSV has more than two columns (game + tags), combine all columns after the first into tags
        if df.shape[1] > 2:
            game_col = df.columns[0]
            other_cols = df.columns[1:]
            tags_series = df[other_cols].astype(str).fillna('').agg(','.join, axis=1)
            tags_series = tags_series.str.strip().str.strip(',')
            df = df[[game_col]].copy()
            df.columns = ['game']
            df['tags'] = tags_series
        else:
            if 'tags' not in df.columns:
                cols = df.columns.tolist()
                if len(cols) == 1:
                    df['tags'] = ''
                else:
                    df.columns = ['game', 'tags']
            df['tags'] = df['tags'].fillna('').astype(str)
        # normalize
        df['tags'] = df['tags'].astype(str).str.lower()
        df['game'] = df['game'].astype(str)
        return df
    except Exception as e:
        print(f"Error reading games.csv: {e}")
        return pd.DataFrame(columns=['game', 'tags'])


def save_games_df(df: pd.DataFrame) -> None:
    df.to_csv('games.csv', index=False)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def _choose_random_from_df(df: pd.DataFrame) -> Optional[str]:
    if df.empty:
        return None
    return random.choice(df['game'].tolist())


def _normalize_category_token(token: str) -> str:
    token = token.strip().lower()
    # support short flags -> map to tag names
    flags = {
        '-p': 'party',
        '--party': 'party',
        '-f': 'fps',
        '--fps': 'fps',
        '-b': 'battle-royale',
        '--br': 'battle-royale',
        '-m': 'mmo',
        '--mo': 'moba',
        '-e': 'extraction-shooter',
        '--extraction': 'extraction-shooter',
    }
    return flags.get(token, token)


def get_suggestion(category: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    """Return a tuple (game, category) for a random suggestion.
    If category is provided but no game is found, returns (None, normalized_category).
    If no category is provided and no games exist, returns (None, None).
    """
    df = load_games_df()
    if category:
        cat = _normalize_category_token(category)
        # filter rows where the tags column contains the tag as a discrete value
        def has_tag(s: str) -> bool:
            return cat in [t.strip() for t in s.split(',') if t.strip()]

        filtered = df[df['tags'].apply(has_tag)]
        if filtered.empty:
            return None, cat
        return _choose_random_from_df(filtered), cat
    # no category given -> pick from all games
    game = _choose_random_from_df(df)
    return (game, None) if game else (None, None)


@bot.command(name="suggest")
async def suggest_game(ctx, *, arg: str = None):
    """
    Get a random game suggestion. Optionally provide a category or a short flag.
    Usage: !suggest
           !suggest party
           !suggest -p
    """
    # Use shared helper to pick a suggestion
    game, used_category = get_suggestion(arg)
    if arg and not game:
        # tag was requested but nothing found
        await ctx.send(f"No games found for tag '{used_category}'.")
        return
    if not game:
        await ctx.send("No games available to suggest.")
        return
    if used_category:
        await ctx.send(f"🎮 You should play (tag: **{used_category}**): **{game}** tonight!")
    else:
        await ctx.send(f"🎮 You should play: **{game}** tonight!")


@bot.command(name="party")
async def suggest_party(ctx):
    """Convenience command: suggest a random party game."""
    game, cat = get_suggestion('party')
    if not game:
        await ctx.send("No party games found.")
        return
    await ctx.send(f"🎮 You should play (tag: **{cat}**): **{game}** tonight!")


@bot.command(name="fps")
async def suggest_fps(ctx):
    """Convenience command: suggest a random FPS game."""
    game, cat = get_suggestion('fps')
    if not game:
        await ctx.send("No FPS games found.")
        return
    await ctx.send(f"🎮 You should play (tag: **{cat}**): **{game}** tonight!")

@bot.command(name="mmo")
async def suggest_mmo(ctx):
    """Convenience command: suggest a random MMO game."""
    game, cat = get_suggestion('mmo')
    if not game:
        await ctx.send("No MMO games found.")
        return
    await ctx.send(f"🎮 You should play (tag: **{cat}**): **{game}** tonight!")


@bot.command(name="extraction-shooter")
async def suggest_extraction(ctx):
    """Convenience command: suggest a random extraction-shooter game."""
    game, cat = get_suggestion('extraction-shooter')
    if not game:
        await ctx.send("No extraction-shooter games found.")
        return
    await ctx.send(f"🎮 You should play (tag: **{cat}**): **{game}** tonight!")

@bot.command(name="moba")
async def suggest_fps(ctx):
    """Convenience command: suggest a random MOBA game."""
    game, cat = get_suggestion('moba')
    if not game:
        await ctx.send("No MOBA games found.")
        return
    await ctx.send(f"🎮 You should play (tag: **{cat}**): **{game}** tonight!")


@bot.command(name="games")
async def list_games(ctx, *, arg: str = None):
    """
    Display a list of available games. Optionally provide a category to filter.
    Usage: !games
           !games party
    """
    df = load_games_df()
    if arg:
        tag = _normalize_category_token(arg)

        def has_tag(s: str) -> bool:
            return tag in [t.strip() for t in s.split(',') if t.strip()]

        df = df[df['tags'].apply(has_tag)]
        header = f"Here are the games with tag '{tag}':\n"
    else:
        header = "Here are some multiplayer games you can play:\n"

    if df.empty:
        await ctx.send("No games found.")
        return

    games_sorted = sorted(df['game'].tolist())
    games_str = "\n".join(f"🎮 {g}" for g in games_sorted)
    # Split messages if too long for Discord
    if len(games_str) > 1900:
        messages = []
        current_msg = header
        for game in games_sorted:
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
        await ctx.send(f"{header}{games_str}")


@bot.command(name="tags")
async def list_tags(ctx):
    """List available tags found in `games.csv`. Shows short flag hints when available."""
    df = load_games_df()
    if df.empty or 'tags' not in df.columns:
        await ctx.send("No tags found.")
        return

    # Build a set of tags seen across all rows
    tags_set = set()
    for s in df['tags'].dropna().astype(str):
        for t in [x.strip() for x in s.split(',') if x.strip()]:
            tags_set.add(t)

    cats = sorted(tags_set)
    if not cats:
        await ctx.send("No tags found.")
        return

    # Map some well-known tags to short flags for convenience
    flags_map = {
        'party': '-p',
        'fps': '-f',
        'battle-royale': '-b',
        'mmo': '-m',
        'moba': '-mo',
        'extraction-shooter': '-e',
    }

    lines = []
    for c in cats:
        hint = f" ({flags_map[c]})" if c in flags_map else ""
        lines.append(f"📂 {c}{hint}")

    header = "Available tags:\n"
    body = "\n".join(lines)
    msg = header + body

    # Split message if it's too long for Discord
    if len(msg) > 1900:
        # chunk lines into multiple messages
        messages = []
        current = header
        for line in lines:
            if len(current) + len(line) + 1 > 1900:
                messages.append(current)
                current = line + "\n"
            else:
                current += line + "\n"
        messages.append(current)
        for m in messages:
            await ctx.send(m)
    else:
        await ctx.send(msg)


def _parse_game_and_tags(payload: str):
    """Parse payload in format: <game name> | <tag1,tag2>
    If no '|' present, tags defaults to empty string. Returns (game, tags_csv).
    Tags are normalized to lowercase and stored as a comma-separated string.
    """
    if '|' in payload:
        parts = payload.split('|', 1)
        game = parts[0].strip()
        tags_raw = parts[1].strip().lower()
        tags = ','.join([t.strip() for t in tags_raw.split(',') if t.strip()])
    else:
        game = payload.strip()
        tags = ''
    return game, tags


@bot.command(name="add")
@commands.has_permissions(administrator=True)
async def add_game(ctx, *, payload: str):
    """
    Add a new game with an optional category.
    Usage: !add <game name> | <category>
    Example: !add Among Us | party
    If no category given, 'general' is used.
    Requires administrator permissions.
    """
    game_name, tags = _parse_game_and_tags(payload)
    if len(game_name) > 100:
        await ctx.send("Game name is too long. Please keep it under 100 characters.")
        return
    if not game_name:
        await ctx.send("Game name cannot be empty.")
        return

    df = load_games_df()
    # case-insensitive check
    if any(df['game'].str.lower() == game_name.lower()):
        await ctx.send(f"Game '{game_name}' is already in the list.")
        return

    new_row = pd.DataFrame([{'game': game_name, 'tags': tags}])
    df = pd.concat([df, new_row], ignore_index=True)
    save_games_df(df)
    tag_display = tags if tags else 'general'
    await ctx.send(f"Game '{game_name}' has been added to the list (tags: {tag_display}).")


@bot.command(name="remove")
@commands.has_permissions(administrator=True)
async def remove_game(ctx, *, payload: str):
    """
    Remove a game by name. Optionally include a category after '|' for clarity, but
    only the game name is used for removal.
    Usage: !remove <game name>
           !remove <game name> | <category>
    Requires administrator permissions.
    """
    game_name, _ = _parse_game_and_tags(payload)
    df = load_games_df()
    mask = df['game'].str.lower() == game_name.lower()
    if not mask.any():
        await ctx.send(f"Game '{game_name}' is not in the list.")
        return
    df = df[~mask]
    save_games_df(df)
    await ctx.send(f"Game '{game_name}' has been removed from the list.")


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
