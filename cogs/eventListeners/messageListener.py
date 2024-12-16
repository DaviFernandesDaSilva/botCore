from datetime import datetime
import discord
from discord.ext import commands

class MessageListenerCog(commands.Cog, name="Listener de Mensagens"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command(self, ctx):
        # Obtendo as informações
        server_name = ctx.guild.name if ctx.guild else "DM"  # Nome do servidor ou "DM" se for uma mensagem direta
        user_name = ctx.author.name  # Nome do usuário que invocou o comando
        command_name = ctx.command.name  # Nome do comando
        args = ctx.args  # Argumentos do comando
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Hora do comando

        # Registrando as informações no console
        print("-" * 30)
        print(f"Comando usado: {command_name}")
        print(f"Servidor: {server_name}")
        print(f"Usuário: {user_name}")
        print(f"Argumentos: {args if args else 'Nenhum argumento'}")
        print(f"Data e Hora: {timestamp}")
        print("-" * 30)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # Corrigido para aceitar 'self' corretamente
        if isinstance(error, commands.MissingRequiredArgument):
            command = ctx.command
            # Obtém o help completo do comando
            await ctx.message.reply(f"❌ Estão faltando argumentos! Para mais informações, use: `{ctx.prefix}ajuda {command}`")
        elif isinstance(error, commands.CommandNotFound):
            # Tratamento específico para comando não encontrado
            await ctx.message.reply("❌ Comando não encontrado. Use `!!ajuda` para ver a lista de comandos disponíveis.")
        elif isinstance(error, commands.CheckFailure):
            # Tratamento para falha no check (ex: delay de comando)
            print("⚠️ Você não pode usar este comando agora. Aguarde o tempo de delay.")  # Remova o await
        else:
            # Para outros tipos de erro, se necessário
            await ctx.send(f"⚠️ Ocorreu um erro: {str(error)}")
            print(f"Erro em {ctx.command}: {error}")

# Setup da cog
async def setup(bot):
    # Verifica se o cog já foi carregado antes de adicionar novamente
    if "MessageListenerCog" not in bot.cogs:
        await bot.add_cog(MessageListenerCog(bot))  # Await ao adicionar o cog
    else:
        print("Cog 'MessageListenerCog' já carregado!")
