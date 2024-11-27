from aiogram.filters import BaseFilter
from typing import Union

from aiogram.types import Message

class BrawlStarsLinkFilter(BaseFilter):
    """Custom filter to check if a message contains a specific Brawl Stars invite link."""

    async def __call__(self, message: Message) -> bool:
        # Prefix to look for in the URL
        required_prefix = "https://link.brawlstars.com/invite/friend/"

        if message.entities:
            # Iterate through all entities in the message
            for entity in message.entities:
                # Check if the entity type is 'url'
                if entity.type == 'url':
                    # Extract the URL from the message based on the entity's offset and length
                    url = entity.extract_from(message.text)
                    # Check if the URL starts with the required prefix
                    if url.startswith(required_prefix):
                        return True
        return False