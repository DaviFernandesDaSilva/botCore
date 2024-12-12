import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

from func.checks import check_delay

load_dotenv()

class Cambio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    @commands.command(name="cambio", help="Exibe a taxa de câmbio de BRL para outras moedas.")
    @commands.check(check_delay)
    async def cambio(self, ctx, moeda: str):
        """Exibe a taxa de câmbio de BRL para uma moeda solicitada."""
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/BRL"
        
        # Fazendo a requisição assíncrona
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Verificando se a moeda está disponível
                        if moeda.upper() in data['conversion_rates']:
                            rate = data['conversion_rates'][moeda.upper()]
                            embed = discord.Embed(
                                title=f"Taxa de Câmbio - BRL para {moeda.upper()}",
                                description=f"A taxa de câmbio de 1 BRL para {moeda.upper()} é **{rate}**.",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"❌ Moeda `{moeda.upper()}` não encontrada ou não suportada.")
                    else:
                        await ctx.send(f"❌ Não foi possível obter as taxas de câmbio. Status code: {response.status}")
            except Exception as e:
                await ctx.send(f"⚠️ Erro ao fazer a requisição: {str(e)}")

async def setup(bot):
    if "Cambio" not in bot.cogs:
        await bot.add_cog(Cambio(bot))
    else:
        print("Cog 'Cambio' já carregado!")