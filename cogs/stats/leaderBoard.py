import discord
from discord.ext import commands
from discord import app_commands
import json

from func.checks import check_delay

COMMANDS_FILE = "command_counts.json"

# Função para carregar os dados de contagem
def load_command_counts():
    with open(COMMANDS_FILE, "r") as f:
        return json.load(f)

# Classe do cog de leaderboard
class LeaderboardCog(commands.Cog, name="Placares"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="topComandos")
    @commands.check(check_delay)
    async def leaderboard(self, ctx):
        """Mostra o leaderboard dos usuários com mais comandos executados"""
        # Carregar as contagens de comandos
        command_counts = load_command_counts()

        # Organizar os usuários pela quantidade de comandos, de forma decrescente
        sorted_counts = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)

        # Criar um embed para exibir o leaderboard
        embed = discord.Embed(title="Leaderboard de Comandos", description="Ranking dos usuários com mais comandos executados", color=discord.Color.purple())
        
        # Definir uma imagem no topo do embed
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9718/9718462.png")  # Substitua com sua imagem preferida

        # Adicionar um footer com o nome do bot
        embed.set_footer(text="Comando gerenciado por BotCore", icon_url=ctx.bot.user.avatar.url)

        # Adicionar os top 10 usuários ao embed
        for i, (user_id, count) in enumerate(sorted_counts[:10], start=1):
            user = await self.bot.fetch_user(int(user_id))  # Pegar o usuário a partir do ID
            embed.add_field(name=f"**{i}. {user.name}**", value=f"**{count} comandos**", inline=False)

        # Enviar o embed
        await ctx.send(embed=embed)

# Função para carregar o cog no bot
async def setup(bot):
    if "LeaderboardCog" not in bot.cogs:
        await bot.add_cog(LeaderboardCog(bot))
    else:
        print("Cog 'LeaderboardCog' já carregado!")
