import discord
from discord.ext import commands
import aiohttp

class ApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
async def setup(bot):
    await bot.add_cog(ApiCog(bot))