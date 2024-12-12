import time
from discord.ext import commands

# Dicionário para armazenar o tempo do último comando de cada usuário
user_last_command_time = {}

# Função que será usada como o "check" para todos os comandos
async def check_delay(ctx):
    delay_time = 5  # Tempo de delay em segundos
    current_time = time.time()  # Tempo atual em segundos

    # Verifica se o usuário é o dono do bot
    if await commands.is_owner().predicate(ctx):
        return True  # Sem delay para o dono do bot

    # Verifica o tempo do último comando enviado pelo usuário
    last_command_time = user_last_command_time.get(ctx.author.id)

    # Se o usuário não tem registro de tempo ou respeitou o delay, retorna True
    if last_command_time is None or current_time - last_command_time >= delay_time:
        # Atualiza o tempo do último comando
        user_last_command_time[ctx.author.id] = current_time
        return True
    else:
        # Se não respeitou o delay, retorna False
        remaining_time = delay_time - (current_time - last_command_time)
        await ctx.send(f":warning: {ctx.author.mention}, por favor, espere {remaining_time:.1f} segundos antes de usar outro comando.")
        return False  # Bloqueia o comando