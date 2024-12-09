import discord
from discord.ext import commands
from numpy import *
import numexpr
class CalculadoraCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        numexpr.set_num_threads(2)
        
    @commands.command(name="calc", aliases=["soma","mult","sub","div","calcular"], help="Fazer cálculos aritméticos")
    async def calcular(self, ctx, expression:str):
        try:
            response = numexpr.evaluate(expression)
            await ctx.send(f"{expression} = {response}")
        except:
            await ctx.send("Erro: Expressão inválida <-")
    
        
async def setup(bot):
    if "CalculadoraCog" not in bot.cogs:
        await bot.add_cog(CalculadoraCog(bot))
    else:
        print("Cog 'CalculadoraCog já carregado!")