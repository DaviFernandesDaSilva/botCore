import asyncio
import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os
from translate import Translator

from func.checks import check_delay

# Carrega as variáveis do arquivo .env
load_dotenv()

class JokeCog(commands.Cog, name="Piadas"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="piada", help="Busca uma piada aleatória.")
    @commands.check(check_delay)
    async def piada(self, ctx, categoria="Any"):  
        url = f"https://v2.jokeapi.dev/joke/{categoria}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()               
                    if data['error']:
                        await ctx.send("❌ Não foi possível encontrar uma piada.")
                    else:
                        if 'setup' in data:
                            tradutor = Translator(to_lang="pt")
                            jokeSetup = f"{data['setup']}"
                            jokeDelivery = f"{data['delivery']}"
                            await ctx.send(f" > {tradutor.translate(jokeSetup)}")
                            await asyncio.sleep(2)
                            await ctx.send(f" > || {tradutor.translate(jokeDelivery)} ||")
                        else:
                            await ctx.send("❌ Não foi possível encontrar uma piada!!!")


                elif response.status == 404:
                    await ctx.send("❌ Argumento inválido!")
                elif response.status == 403:
                    await ctx.send("❌ Argumento inválido!")
                elif response.status == 400:
                    await ctx.send("❌ Argumento inválido!")
                else:
                    await ctx.send(f"❌ Erro ao acessar a API. Código: {response.status}")

async def setup(bot):
    if "JokeCog" not in bot.cogs:
        await bot.add_cog(JokeCog(bot))
    else:
        print("Cog 'JokeCog' já carregado!")
