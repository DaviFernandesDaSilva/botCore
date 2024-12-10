import discord
from discord.ext import commands
import aiohttp

class ExchangeRateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="converter", help="Converter um valor X de uma moeda pra outra")
    async def converter(self, ctx, amount: float, base_currency: str, target_currency: str):
        """Converte o valor de uma moeda para outra."""
        # URL da API de câmbio
        url = EXCHANGE_TOKEN

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

    @commands.command(name="cambio", help="Exibe a taxa de câmbio de BRL para outras moedas.")
    async def cambio(self, ctx, moeda: str):
        """Exibe a taxa de câmbio de BRL para uma moeda solicitada."""
        url = EXCHANGE_TOKEN
        
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

# Função para adicionar o cog
async def setup(bot):
    await bot.add_cog(ExchangeRateCog(bot))
