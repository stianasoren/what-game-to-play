# What Game To Play Tonight?

<p align="center">
  <img src="assets/avatar.png" alt="Avatar" width="200" />
</p>

This project helps you decide what game to play tonight. It includes both a Python GUI script and a Discord bot for game suggestions.

## Getting Started

1. Make sure you have Python installed
2. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. For the Discord bot, create a `.env` file with your bot token:
   ```
   DISCORD_BOT_TOKEN=your_token_here
   ```

## Project Structure
- [`main.py`](main.py): The main script with a GUI for game suggestion logic.
- [`bot.py`](bot.py): A Discord bot that suggests games via chat commands.
- [`requirements.txt`](requirements.txt): List of Python dependencies
- [`start_bot.bat`](start_bot.bat): Windows batch script for auto-starting the bot
- [`games.csv`](games.csv): Database of games that can be suggested
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md): Custom Copilot instructions for this workspace.

## How to Run

### GUI Script

```sh
python main.py
```

### Discord Bot

You can run the bot in two ways:

#### Manual Start
```sh
python bot.py
```

#### Auto-start on Windows
1. Edit the `start_bot.bat` script to match your project path
2. Create a shortcut to `start_bot.bat` in your Windows Startup folder:
   - Press `Win + R`
   - Type `shell:startup`
   - Create a shortcut to `start_bot.bat` in this folder

#### Bot Commands

- `!suggest` — Suggests a random multiplayer game.
- `!games` — Lists all available multiplayer games.
- `!spell` — Suggests a game based on channel names in the "🎮 Spell" category.
- `!add <game>` — Add a new game to the list.
- `!remove <game>` — Remove a game from the list.
- `!help` — Show all available commands and their usage.

Feel free to customize and expand the scripts as needed!
