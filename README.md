# What Game To Play Tonight?

This project helps you decide what game to play tonight. It includes both a Python GUI script and a Discord bot for game suggestions.

## Getting Started

1. Make sure you have Python installed.
2. Add your list of games and preferences to the scripts.
3. Run either the GUI script or the Discord bot to get a game suggestion!

## Project Structure
- [`main.py`](main.py): The main script with a GUI for game suggestion logic.
- [`bot.py`](bot.py): A Discord bot that suggests games via chat commands.
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md): Custom Copilot instructions for this workspace.

## How to Run

### GUI Script

```sh
python main.py
```

### Discord Bot

1. Add your Discord bot token to the `.env` file as `DISCORD_BOT_TOKEN`.
2. Install dependencies:
   ```sh
   pip install discord.py python-dotenv
   ```
3. Run the bot:
   ```sh
   python bot.py
   ```

#### Bot Commands

- `!suggest` — Suggests a random multiplayer game.
- `!games` — Lists all available multiplayer games.
- `!spell` — Suggests a game based on channel names in the "🎮 Spell" category.

Feel free to customize and expand the scripts as needed!
