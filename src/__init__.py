"""
Klash source file.
"""

import asyncio
from typing import Optional, Callable


class Klash:
    """Base class for Klash."""

    def __init__(self) -> None:
        self.__commands: list = []

    def add(self, guild_id: Optional[int], name: Optional[str], description: str, options: list):
        """Add new global slash command decorator.

        Args:
            guild_id (int, None): Guild ID. (if None, it will be global command.).
            name (str, None): Command name. (if None, it will get the function name as command name.).
            description (str): Command description
            options (list): Commad options. (see https://discord.com/developers/docs/interactions/slash-commands#application-command-object-application-command-option-structure.)
        """

        def decorator(fn: Callable):
            def wrapper():
                self.__commands.append({
                    "scope": "global" if guild_id is None else guild_id,
                    "name": name or fn.__name__,
                    "description": description,
                    "options": options,
                    "execute": fn
                })

                return self.__commands

            return wrapper()

        return decorator

    async def load(self, client):
        """Load commands. (recommended to use in ready event.)

        Args:
            client (krema.models.Client): Client.
        """

        # Load commands
        urls = []

        for command in self.__commands:
            url = f"/applications/{client.user.id}"

            if command.get("scope") == "global":
                url += "/commands"
            else:
                url += f"/guilds/{command.get('scope')}/commands"

            urls.append({"url": url, "data": {
                "name": command["name"],
                "description": command["description"],
                "options": command["options"]
            }})

        await asyncio.gather(*[
            client.http.request("POST", i.get("url"), json=i.get("data")) for i in urls
        ])

    def prepare(self, client):
        """Prepare commands.

        Args:
            client (krema.models.Client): Client.
        """

        # Add Interaction Create event.
        async def wrapper(i):
            for command in self.__commands:
                if command.get("name") == i.data.get("name"):
                    await command.get("execute")(i)
                    return

        client.events.append(
            ("interaction_create", wrapper)
        )
