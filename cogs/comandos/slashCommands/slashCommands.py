import discord
from discord import app_commands
from discord.ext import commands

from func.checks import check_delay

class DMSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mandardm", description="Envia uma mensagem privada para você.")
    @commands.check(check_delay)
    async def send_dm(self, interaction: discord.Interaction):
        try:
            user = interaction.user
            dm_message = "Oi. Esta é uma mensagem privada enviada pelo BotCore como teste!"
            
            # Envia a mensagem para a DM do usuário
            await user.send(dm_message)
            await interaction.response.send_message("✅ Mensagem enviada para sua DM!", ephemeral=True)  # Ephemeral faz a resposta ser visível só para quem usou o comando
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não consegui enviar a mensagem. Verifique se suas DMs estão abertas.", ephemeral=True)

async def setup(bot):
    if "DMSlash" not in bot.cogs:
        await bot.add_cog(DMSlash(bot))
    else:
        print("Cog 'DMSlash' já carregado!")