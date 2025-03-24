import discord
from bot import *

"""
This file integrates the bot into discord
Basil Ali
"""
class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.docs, self.labels = read_few_shots("data.json")
        self.relevance_instructions = read_text_file("relevance_instructions.txt")
        self.assistant_instructions = read_text_file("assistant_instructions.txt")
        self.relevance_prompt = build_relevance_prompt(self.docs, self.labels, self.relevance_instructions)
        self.dialog = [
        {"role": "system", "content": self.assistant_instructions}
    ]

    async def on_ready(self):
        """
        Called when the bot logs in
        """
        print('Logged on as', self.user)

    async def on_message(self, message):
        """
        Called when a message is received.
        :param message: The message received.
        """

        # only respond to pings
        if self.user not in message.mentions:
            return

        # don't respond to ourselves
        if message.author == self.user:
            return

        # get the utterance and generate the response
        utterance = message.content

        relevance = get_relevance(self.relevance_prompt, utterance)

        if relevance == "1":
            self.dialog.append({ "role": "user", "content": utterance })
            dialog = get_response(self.dialog)
            response = dialog[len(dialog) - 1].content
        else:
            response = "Sorry, I can't help you with that."

        # send the response
        await message.channel.send(response)

## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()
client.run(token)