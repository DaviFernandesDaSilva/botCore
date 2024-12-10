import discord
from discord.ext import commands
from numpy import *
import numexpr
class CalculadoraCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        numexpr.set_num_threads(2)
        
    @commands.command(
        name="calc",
        aliases=["soma", "mult", "sub", "div", "calcular"],
        help="Realiza cálculos aritméticos. Exemplo: `!!calc 2+2` ou `!!calc 5*3`."
    )
    async def calcular(self, ctx, *, expression: str = None):
        # Verifica se o argumento foi fornecido
        if not expression:
            await ctx.send("❌ Você precisa fornecer uma expressão. Exemplo: `!!calc 2+2`.")
            return

        try:
            # Valida a expressão para evitar uso de funções perigosas
            safe_expression = "".join(char for char in expression if char in "0123456789+-*/(). ")
            if safe_expression != expression:
                await ctx.send("⚠️ A expressão contém caracteres inválidos.")
                return

            # Avalia a expressão
            result = numexpr.evaluate(safe_expression)
            await ctx.send(f"✅ Resultado: `{expression} = {float(result):.4f}`")
        except ZeroDivisionError:
            await ctx.send("❌ Erro: Divisão por zero não é permitida.")
        except Exception as e:
            await ctx.send(f"❌ Erro: Expressão inválida. Detalhes: `{str(e)}`")
    
        
async def setup(bot):
    if "CalculadoraCog" not in bot.cogs:
        await bot.add_cog(CalculadoraCog(bot))
    else:
        print("Cog 'CalculadoraCog já carregado!")