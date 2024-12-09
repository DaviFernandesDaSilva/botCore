import discord
from discord.ext import commands
import aiohttp
class ApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
async def setup(bot):
    # Verifica se o cog já foi carregado antes de adicionar novamente
    if "ApiCog" not in bot.cogs:
        await bot.add_cog(ApiCog(bot))  # Await ao adicionar o cog
    else:
        print("Cog 'ApiCog já carregado!")