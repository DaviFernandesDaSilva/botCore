import discord
from discord.ext import commands

class MessageListenerCog(commands.Cog, name="Listener de Mensagens"):
    def __init__(self, bot):
        self.bot = bot
        
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
