import discord
from discord.ext import commands
import logging
import os
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()  # Ativa todos os intents

# Inicializando o bot
bot = commands.Bot(
    command_prefix="!!", 
    help_command=None,  
    intents=intents,  
    application_id=int(os.getenv("BOT_ID"))  
)

# Ao ligar
@bot.event
async def on_ready():
    # Obtendo a data e hora atual
    now = datetime.now()
    data_hora = now.strftime("%d/%m/%Y %H:%M:%S") 
    
    canal_id = 1315495514132971583  # ID do canal pessoal para testes/debug
    canal = bot.get_channel(canal_id)
    
    if canal:
        await canal.send(f"**🟢 Bot ligado em {data_hora}** 🚀")
    
    print(f"🟢 Bot conectado como {bot.user}. Data e Hora de Conexão: {data_hora}")

    # Agora que o bot está pronto, chamamos a sincronização dos comandos
    await reload_cogs()

is_syncing = False

@bot.command(name="syncReload", aliases=["sync", "reload"], hidden=True)
@commands.is_owner()
async def syncReload(ctx, guild=None):
    """Comando para sincronizar e recarregar cogs."""
    global is_syncing
    
    if is_syncing:
        await ctx.send("O processo de recarga já está em andamento. Tente novamente mais tarde.")
        return

    is_syncing = True
    start_time = time.time()

    canal_id = 1315495514132971583  # ID do canal de um dos servidores
    canal = bot.get_channel(canal_id)
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if canal:
        await canal.send(f"🔄 O Bot começou a recarregar às {data_hora}...")

    try:
        # Sincroniza os comandos
        synced = await bot.tree.sync(guild=discord.Object(id=int(guild)) if guild else None)
        print(f"Comandos sincronizados: {synced}")

        # Recarrega os cogs
        await reload_cogs()

        # Marca o tempo de término e calcula o tempo total de execução
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tempo total de execução: {execution_time:.2f} segundos")

        # Envia mensagens de confirmação
        if canal:
            await canal.send(f"✅ Sincronizado e módulos recarregados com sucesso! (Tempo: {execution_time:.2f} segundos)")
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            await canal.send(f"🔄 O Bot terminou de ser Recarregado em {data_hora} ✅")

        await ctx.send("Tudo sincronizado! ✅")

    except Exception as e:
        print(f"Erro durante o syncReload: {e}")
        await ctx.send(f"⚠️ Erro durante o syncReload: {e}")

    finally:
        is_syncing = False


async def unload(extension_name):
    if extension_name in bot.extensions:
        try:
            await bot.unload_extension(extension_name)
        except Exception as e:
            print(f"Erro ao descarregar a extensão {extension_name}: {e}")


async def load(extension_name):
    try:
        await bot.load_extension(extension_name)
    except Exception as e:
        print(f"Erro ao carregar a extensão {extension_name}: {e}")

async def reload_cogs():
    cogs_dir = './cogs'

    # Carregar as extensões novamente
    for root, _, files in os.walk(cogs_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                extension_name = os.path.join(root, file).replace('./', '').replace('/', '.').replace('\\', '.').replace('.py', '')
                await unload(extension_name)  
                await load(extension_name)

    # Sincronizar os comandos após recarregar todos os cogs
    await bot.tree.sync()


async def main():
    # Espera o carregamento dos cogs
    async with bot:
        # Recupera o TOKEN do ambiente
        TOKEN = os.getenv("DISCORD_TOKEN")
        # Inicia o bot com o token
        await bot.start(TOKEN)


asyncio.run(main())
