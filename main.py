import random
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

bot = commands.Bot(command_prefix="!!",help_command=None, intents=discord.Intents.all(), application_id=int(os.getenv("BOT_ID")))

##CASO COMANDO INVÁLIDO
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Tratamento específico para comando não encontrado
        await ctx.send("❌ Comando não encontrado. Use `!!ajuda` para ver a lista de comandos disponíveis.")
    elif isinstance(error, commands.CheckFailure):
        # Tratamento para falha no check (ex: delay de comando)
        print("⚠️ Você não pode usar este comando agora. Aguarde o tempo de delay.")  # Remova o await
    else:
        # Para outros tipos de erro, se necessário
        await ctx.send(f"⚠️ Ocorreu um erro: {str(error)}")
        print(f"Erro em {ctx.command}: {error}")

# Variável global para verificar se o comando está sendo executado
is_syncing = False

@bot.command(hidden=True)
@commands.is_owner()
async def syncReload(ctx, guild=None):
    global is_syncing
    
    if is_syncing:
        await ctx.send("O processo de recarga já está em andamento. Tente novamente mais tarde.")
        return

    try:
        # Marca o tempo de início
        is_syncing = True
        start_time = time.time()

        canal_id = 1315495514132971583  # ID do canal de um dos servidores
        canal = bot.get_channel(canal_id)
        now = datetime.now()
        data_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        
        if canal:
            await canal.send(f"**🔄 O Bot começou a recarregar às {data_hora}... 🔄**")
        
        # Sincroniza os comandos
        if guild is None:
            synced = await bot.tree.sync()
        else:
            synced = await bot.tree.sync(guild=discord.Object(id=int(guild)))
        
        print(f"Comandos sincronizados: {synced}")

        # Recarrega todos os cogs na pasta 'cogs'
        cogs_dir = './cogs'
        cogs = [filename[:-3] for filename in os.listdir(cogs_dir) if filename.endswith('.py')]
        
        for cog_name in cogs:
            try:
                # Verifica se o cog está carregado e o descarrega
                if f'cogs.{cog_name}' in bot.extensions:
                    await bot.unload_extension(f'cogs.{cog_name}')
                    print(f"Módulo {cog_name} descarregado com sucesso!")

                # Carrega ou recarrega o cog
                await bot.load_extension(f'cogs.{cog_name}')
                print(f"Módulo {cog_name} carregado com sucesso!")
                await asyncio.sleep(0.5)  # Pausa para evitar sobrecarga
            except Exception as e:
                print(f"Erro ao recarregar o módulo {cog_name}: {e}")
                await ctx.send(f"⚠️ Erro ao recarregar o módulo `{cog_name}`: `{e}`")
        
        # Marca o tempo de término
        end_time = time.time()

        # Calcula o tempo total de execução
        execution_time = end_time - start_time
        print(f"Tempo total de execução: {execution_time:.2f} segundos")

        # Confirmação de sincronização
        await canal.send(f"✅ **Sincronizado e módulos recarregados com sucesso! ✔️** _(Tempo de execução: {execution_time:.2f} segundos)_")
        
        # Envia o horário de término do processo
        now = datetime.now()
        data_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        if canal:
            await canal.send(f"**🔄 O Bot terminou de ser Recarregado em {data_hora}** ✅")
        await ctx.send(f"**Tudo sincronizado!✅**")

    except Exception as e:
        # Tratamento de erros gerais
        print(f"Erro durante o syncReload: {e}")
        await ctx.send(f"⚠️ **Erro durante o syncReload:** `{e}`")

    finally:
        is_syncing = False


#AO LIGAR
@bot.event
async def on_ready():
    # Obtendo a data e hora atual
    await bot.tree.sync()
    now = datetime.now()
    data_hora = now.strftime("%d/%m/%Y %H:%M:%S")  # Formato: Dia/Mês/Ano Hora:Minuto:Segundo
    
    canal_id = 1315495514132971583  # ID do canal de um dos servidores
    canal = bot.get_channel(canal_id)
    
    if canal:
        await canal.send(f"**🟢 Bot ligado em {data_hora}** 🚀")
    
    print(f"🟢 Bot conectado como {bot.user}. Data e Hora de Conexão: {data_hora}")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load();
        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

asyncio.run(main())
