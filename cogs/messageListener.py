import discord
from discord.ext import commands

class MessageListenerCog(commands.Cog, name="Listener de Mensagens"):
    def __init__(self, bot):
        self.bot = bot

    # def load_responses(self):
    #     """Carrega as respostas do arquivo JSON."""
    #     try:
    #         with open('responses.json', 'r', encoding='utf-8') as f:
    #             data = json.load(f)
    #             responses = {}
    #             for key, value in data.items():
    #                 # Armazena cada palavra em um frozenset para comparação
    #                 responses[frozenset(value['words'])] = value['response']
    #             return responses
    #     except FileNotFoundError:
    #         print("Arquivo 'responses.json' não encontrado. As respostas não serão carregadas.")
    #         return {}

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     """Este evento é disparado sempre que uma mensagem é enviada."""
    #     # Ignora mensagens enviadas pelo próprio bot
    #     if message.author == self.bot.user:
    #         return

    #     # Normaliza a mensagem (remove acentos e coloca em minúsculas)
    #     normalized_message = self.normalize_text(message.content.lower())

    #     # Verifica se qualquer combinação de palavras existe na mensagem
    #     for words_set, response in self.responses.items():
    #         if words_set.issubset(normalized_message.split()):
    #             await message.reply(response, mention_author=True)
    #             break

    # def normalize_text(self, text):
    #     """Normaliza o texto para remover acentos e tornar a comparação mais flexível."""
    #     return ''.join(
    #         c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'
    #     )

async def setup(bot):
    # Verifica se o cog já foi carregado antes de adicionar novamente
    if "MessageListenerCog" not in bot.cogs:
        await bot.add_cog(MessageListenerCog(bot))  # Await ao adicionar o cog
    else:
        print("Cog 'MessageListenerCog' já carregado!")
