# Recipe Tuning Discord Bot

This was a small project for school. It is a Discord bot that helps users tune recipes according to their dietary needs using OpenAI's GPT models. The bot can analyze recipe ingredients and suggest modifications to accommodate various dietary restrictions.

## Features

- Recipe analysis and modification suggestions
- Natural language processing using GPT models
- Discord integration for easy interaction
- Relevance checking to ensure responses are recipe-related

## Prerequisites

- Python
- OpenAI API key
- Discord Bot Token
- Required Python packages:
  - discord.py
  - openai

## Project Structure

- `bot.py`: Core bot logic and OpenAI integration
- `discord_bot.py`: Discord bot implementation
- `data.json`: Few-shot examples for relevance checking
- `relevance_instructions.txt`: Instructions for relevance classification
- `assistant_instructions.txt`: Instructions for the GPT assistant

## Usage

1. Start the bot by running:
   ```bash
   python discord_bot.py
   ```
2. Invite the bot to your Discord server
3. Mention the bot in a message with your recipe or dietary requirements
4. The bot will analyze your request and provide appropriate suggestions

## How It Works

1. The bot uses few-shot learning to determine if a user's message is recipe-related
2. If relevant, it processes the request using GPT models to provide recipe modifications
3. Responses are tailored to specific dietary needs and restrictions
4. The conversation history is maintained to provide context-aware responses

## Author

Basil Ali
