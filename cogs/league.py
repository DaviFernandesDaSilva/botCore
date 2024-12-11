import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

class LeagueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("RIOT_API_KEY")
        self.base_url = "https://americas.api.riotgames.com/" 

    @commands.command(name="summoner", help="Busca informações sobre um invocador (summoner) no BR1")
    async def summoner(self, ctx, gameName: str, tagLine: str): 
        """Obtém informações sobre um invocador usando a API da Riot Games na região BR1."""
        url = f"{self.base_url}riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        headers = {"X-Riot-Token": self.api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(
                        title=f"Invocador: {data['name']}",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Nível", value=data['summonerLevel'], inline=True)
                    embed.set_footer(text="Informações da API da Riot Games")
                    await ctx.send(embed=embed)
                elif response.status == 404:
                    await ctx.send("❌ Invocador não encontrado.")
                else:
                    await ctx.send(f"❌ Erro ao acessar a API. Código: {response.status}")

async def setup(bot):
    if "LeagueCog" not in bot.cogs:
        await bot.add_cog(LeagueCog(bot))
    else:
        print("Cog 'LeagueCog' já carregado!")
