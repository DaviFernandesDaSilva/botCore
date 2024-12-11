import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

class ExchangeRateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        
    @commands.command(name="converter", help="Converter um valor X de uma moeda pra outra")
    async def converter(self, ctx, amount: float, base_currency: str, target_currency: str):
        """Converte o valor de uma moeda para outra."""
        # URL da API de câmbio
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{base_currency.upper()}"

        # Fazer requisição para a API
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                # Verifica se a requisição foi bem-sucedida
                if response.status != 200:
                    await ctx.send(f"⚠️ Não foi possível obter dados para a moeda {base_currency.upper()}.")
                    return

                # Verifica se a moeda de destino existe
                if target_currency.upper() not in data['conversion_rates']:
                    await ctx.send(f"⚠️ Moeda de destino {target_currency.upper()} não encontrada.")
                    return

                # Pega a taxa de câmbio
                conversion_rate = data['conversion_rates'][target_currency.upper()]

                # Converte o valor
                converted_amount = amount * conversion_rate

                # Envia a mensagem com a conversão
                await ctx.send(f"🔄 **{amount} {base_currency.upper()}** é igual a **{converted_amount:.2f} {target_currency.upper()}**.")

async def setup(bot):
    if "ExchangeRateCog" not in bot.cogs:
        await bot.add_cog(ExchangeRateCog(bot))
    else:
        print("Cog 'ExchangeRateCog' já carregado!")