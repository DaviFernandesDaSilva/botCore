import discord
import random
from discord.ext import commands

# Definindo um cog com comandos
class CommandsCog(commands.Cog, name="Comandos básicos"):
    def __init__(self, bot):
        self.bot = bot
        
    # Comando !!infoUsuario para exibir informações do bot
    @commands.command(help="Mostra a latência do bot.", description="Descrição detalhada sobre o comando.")
    async def infoBot(self, ctx):
        embed = discord.Embed(title="Informações do Bot", description="Este é um bot de testes", color=discord.Color.blue())
        embed.add_field(name="Versão", value="0.1.5")
        embed.add_field(name="Criador", value="Davipbr15", inline=True)
        embed.set_footer(text="Exemplo de comando com embed incluído.")

        await ctx.send(embed=embed)

    # Comando !!infoUsuario para pegar informações de um usuário
    @commands.command(help="Mostra informações de um usuário mencionado ou si próprio")
    async def infoUsuario(self, ctx, usuario: discord.User = None):  # Adicionando 'self' e 'ctx'
        if usuario is None:
            usuario = ctx.author  # Se nenhum usuário for mencionado, pega o autor do comando
        
        # Mapeando os status para versões em português
        status_map = {
            discord.Status.online: "Online",
            discord.Status.idle: "Ausente",
            discord.Status.dnd: "Não Perturbe",
            discord.Status.offline: "Offline",
        }

        if isinstance(usuario, discord.Member):  # Verificando se é um membro
            status = status_map.get(usuario.status, "Desconhecido")
            activity = usuario.activity.name if usuario.activity else "Nenhuma atividade"
        else:
            status = "Desconhecido"
            activity = "Nenhuma atividade"

        embed = discord.Embed(title=f"Informações de {usuario.name}", color=discord.Color.green())
        embed.add_field(name="ID", value=usuario.id)
        embed.add_field(name="Nome", value=usuario.name)
        
        # Adicionando o status e a atividade (se houver) do usuário
        embed.add_field(name="Status", value=status)
        embed.add_field(name="Atividade", value=activity)
        
        # Verificando se o usuário tem um avatar
        if usuario.avatar:
            embed.set_thumbnail(url=usuario.avatar.url)
        else:
            embed.set_thumbnail(url="https://placekitten.com/200/200")  # Imagem padrão caso não tenha avatar
        
        # Mencionando o usuário no início da resposta
        await ctx.send(f"Aqui estão as informações de {usuario.mention}:")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rolarDado(self, ctx, faces: int = 20):
        usuario = ctx.author

        # Rolando o dado
        resultado = random.randint(1, faces)

        # Definindo o emoji com base no resultado
        if resultado < 5:
            emoji = "😞"  # Emoji triste para resultado abaixo de 5
        elif resultado < 10:
            emoji = "😐"  # Emoji meio meh para resultado abaixo de 10
        elif resultado < 15:
            emoji = "😊"  # Emoji feliz para resultado abaixo de 15
        elif resultado < 20:
            emoji = "😁"
        else:
            emoji = "🤩"  # Emoji felizão para resultado entre 15 e 20

        # Criando o embed com um título e cores
        embed = discord.Embed(
            title="🎲 Resultado da Rolagem",  # Título do embed
            description=f"Você rolou um dado de **{faces} faces** e tirou..",  # Adicionando o emoji ao lado do resultado
            color=discord.Color.red(),  # Cor do embed
        )
        embed.add_field(name=f"{emoji}", value=f"**{resultado}**", inline=False)  # Resultado em negrito
        embed.set_thumbnail(url=usuario.avatar.url)  # Foto do usuário
        embed.timestamp = discord.utils.utcnow()

        # Enviando o embed para o canal
        await ctx.send(embed=embed)

# Função para configurar o cog
async def setup(bot):
    await bot.add_cog(CommandsCog(bot))  # Await ao adicionar o cog
