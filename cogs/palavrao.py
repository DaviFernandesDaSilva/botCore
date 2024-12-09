import discord
from discord.ext import commands
import json
import re

# Carregar o arquivo JSON com os palavrões
with open('palavroes.json', 'r', encoding='utf-8') as f:
    palavroes_data = json.load(f)

class PalavroesCog(commands.Cog, name="Repreensão de Palavrões"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Não verificar mensagens do próprio bot
        if message.author == self.bot.user:
            return
        
        # Verificar se alguma palavra do JSON está na mensagem
        for palavrao in palavroes_data['palavroes']:
            # Verificar usando expressões regulares
            if re.search(palavrao['word'], message.content, re.IGNORECASE):
                try:
                    await message.delete()  # Tentar apagar a mensagem
                    await message.reply(f"{palavrao['response']}")  # Responder diretamente na mensagem
                except discord.errors.Forbidden:
                    # Se não conseguir apagar a mensagem, apenas envia a resposta
                    await message.reply(f"{palavrao['response']}")
                break  # Para não enviar múltiplas respostas para diferentes palavrões

async def setup(bot):
    if "PalavroesCog" not in bot.cogs:
        await bot.add_cog(PalavroesCog(bot))
    else:
        print("Cog 'PalavroesCog' já carregado!")
