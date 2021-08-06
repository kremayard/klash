<div align="center">
<h1>Klash</h1>
<p>Slash command framework for Krema.</p>
<p><i>This project is a part of Krema.</i></p>
<br>
</div>

## Documentation

Check https://kremayard.github.io/klash/

## Installation

Run `unikorn add kremayard klash` and you are ready to go!

## Example

```py
from unikorn import krema, klash

client = krema.Client(intents=krema.types.Intents().All())
handler = klash.Klash()


@client.event()
async def ready(_):  # Add ready event
    await handler.load(client)  # Load all of the commands.


@handler.add(867158078025629716, None, description="test command", options=[  # Simple example from discord.
    {
        "name": "animal",
        "description": "The type of animal",
        "type": 3,
        "required": True,
        "choices": [
            {
                "name": "Dog",
                "value": "animal_dog"
            },
            {
                "name": "Cat",
                "value": "animal_cat"
            },
            {
                "name": "Penguin",
                "value": "animal_penguin"
            }
        ]
    }
])
async def example(interaction):
    await interaction.reply(4, content="hello!")  # Reply to interaction.


handler.prepare(client)  # Prepare commands
client.start("client token", bot=True)
```
