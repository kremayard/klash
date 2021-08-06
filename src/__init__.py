"""
Klash source file.
"""

import asyncio
from typing import Optional, Callable


class Klash:
    """Base class for Klash."""

    def __init__(self) -> None:
        self.commands: list = []
        self._ids: list = []

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
                self.commands.append({
                    "scope": "global" if guild_id is None else guild_id,
                    "name": name or fn.__name__,
                    "description": description,
                    "options": options,
                    "execute": fn
                })

                return self.commands

            return wrapper()

        return decorator

    async def load(self, client):
        """Load commands. (recommended to use in ready event.)

        Args:
            client (krema.models.Client): Client.
        """

        urls = []

        for command in self.commands:
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

        result = await asyncio.gather(*[
            client.http.request("POST", i.get("url"), json=i.get("data")) for i in urls
        ])

        self._ids = result
