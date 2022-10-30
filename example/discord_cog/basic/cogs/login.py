import discord

from typing import Dict

from discord import WebhookMessage, app_commands
from discord.ext import commands

from logingateway import HuTaoLoginAPI
from logingateway.model import Player, Ready

class LoginGatewayCog(commands.Cog):
    CLIENT_ID = "abc1234"
    CLIENT_SECRET = "abc1234"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.gateway = HuTaoLoginAPI(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET
        )
        self.tokenStore: Dict[str, WebhookMessage] = {}
        
        # Event
        self.gateway.ready(self.gateway_connect)
        self.gateway.player(self.gateway_player)
        
        # Start gateway
        print("Connecting to Hu Tao Gateway")
        self.gateway.start()

    async def gateway_connect(self, data: Ready):
        print("Connected to Hu Tao Gateway")

    async def gateway_player(self, data: Player):
        if data.token not in self.tokenStore:
            return

        ctx = self.tokenStore[data.token]

        # Recieved data
        print(data.genshin)

        # Send if success
        await ctx.edit(content="🎉 Success to login genshin")

    @app_commands.command(name="login", description="Login Genshin account")
    async def login(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        url, token = self.gateway.generate_login_url(
            user_id=str(interaction.user.id),
            guild_id=str(interaction.guild_id),
            channel_id=str(interaction.channel_id),
            language="en"
        )

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            url=url,
            label="Login Genshin account"
        ))

        message = await interaction.followup.send(
            "Please login genshin to verify login via button", view=view
        )

        self.tokenStore[token] = message

async def setup(client: commands.Bot):
    await client.add_cog(LoginGatewayCog(client))