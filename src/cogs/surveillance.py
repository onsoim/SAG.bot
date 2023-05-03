
from datetime               import datetime
from discord                import Color, Embed
from discord.ext.commands   import Cog
from json                   import load


class Surveillance(Cog):
    def __init__(self, bot):
        print('init surveillance cog')
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print('ready surveillance cog')
        with open("res/channels.json", "r") as j: self.channel  = load(j)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            embed = self.embed(
                before,
                f"Edited in ⁠{before.channel.mention}",
                Color.blue()
            )
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After",  value=after.content,  inline=False)

            await self.bot.get_channel(self.channel['감시']).send(embed = embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        embed = self.embed(
            message,
            f"Message sent by {message.author.mention} Deleted in {message.channel.mention}\n{message.content}",
            Color.red()
        )

        if message.attachments:
            embed.set_image(url = message.attachments[0].url)

        await self.bot.get_channel(self.channel['감시']).send(embed = embed)

    def embed(self, message, description = None, color = None):
        return Embed(
            description = f"**{description}**",
            color = color,
            timestamp = datetime.now().astimezone()
        ).set_author(
            name = message.author,
            icon_url = message.author.avatar or "https://cdn.discordapp.com/embed/avatars/0.png"
        )


async def setup(bot):
    await bot.add_cog(Surveillance(bot))
