import discord
from discord.ext import commands
import json
import os

from func.checks import check_delay

# Arquivo onde os dados de contagem serão armazenados
COMMANDS_FILE = "command_counts.json"

# Função para carregar os dados de contagem
def load_command_counts():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# Função para salvar os dados de contagem no arquivo
def save_command_counts(command_counts):
    with open(COMMANDS_FILE, "w") as f:
        json.dump(command_counts, f, indent=4)

# Classe do cog de contagem de comandos
class CommandCounterCog(commands.Cog, name="Comandos Contador"):
    def __init__(self, bot):
        self.bot = bot
        # Carregar contagens de comandos ao inicializar o cog
        self.command_counts = load_command_counts()

    # Evento que dispara toda vez que um comando é executado
    @commands.Cog.listener()
    @commands.check(check_delay)
    async def on_command(self, ctx):
        user_id = str(ctx.author.id)  # Usar o ID do autor como chave
        # Se o usuário ainda não tiver uma contagem registrada, inicialize
        if user_id not in self.command_counts:
            self.command_counts[user_id] = 0
        # Incrementar a contagem do comando para o usuário
        self.command_counts[user_id] += 1
        # Salvar a contagem no arquivo
        save_command_counts(self.command_counts)

    @commands.command(name="comandosUsados", help="Verificar quantidade de comandos usados de um usuário.")
    @commands.check(check_delay)
    async def comandosUsados(self, ctx, usuario: discord.User = None):
        if usuario is None:
            usuario = ctx.author
        """Exibe a quantidade de comandos usados pelo usuário."""
        user_id = str(usuario.id)
        count = self.command_counts.get(user_id, 0)
        await ctx.send(f"{usuario.name}, você usou {count} comandos.")

# Função para carregar o cog no bot
async def setup(bot):
    if "CommandCounterCog" not in bot.cogs:
        await bot.add_cog(CommandCounterCog(bot))
    else:
        print("Cog 'CommandsCog' já carregado!")
