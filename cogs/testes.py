import discord
from discord.ext import commands
from PIL import Image, ImageSequence
import io

from func.checks import check_delay

# Definindo um cog com comandos
class CommandsCogTeste(commands.Cog, name="Comandos para testes"):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command()
    @commands.check(check_delay)
    async def ping(self, ctx):
        latencia = round(self.bot.latency * 1000)  # Latência em milissegundos
        await ctx.message.reply(f"Pong! A latência é de `{latencia}ms.`")

    @commands.command(help="Testar uma mensagem básica com reação de emoji")
    @commands.check(check_delay)
    # Comando !!olaMundo para testar um print básico com emoji
    async def olaMundo(self, ctx):  # Adicionando 'self' e 'ctx'
        message = await ctx.send("**Olá mundo!**")
        await message.add_reaction("🌎")
        
    # Comando !!embedTest para testar o discord.embed
    @commands.command(help="Fazer teste do embed do discord")
    @commands.check(check_delay)
    async def embedTest(self, ctx):  # Adicionando 'self' para garantir que seja um método de instância
        embed = discord.Embed(
            title="Título", 
            description="Descrição!", 
            color=discord.Color.blue()
        )
        
        # Adicionando campos
        embed.add_field(name="Campo 1", value="Valor 1", inline=True)
        embed.add_field(name="Campo 2", value="Valor 2", inline=True)
        
        # Definindo o autor
        embed.set_author(name="Bot do Davi", icon_url="https://placecats.com/millie/300/300")
        
        # Definindo a imagem de capa
        embed.set_thumbnail(url="https://placehold.co/600x400")
        
        # Definindo a imagem principal
        embed.set_image(url="https://placehold.co/600x600")
        
        # Rodapé
        embed.set_footer(text="Bot do Davipbr15", icon_url="https://placehold.co/200x200")
        
        # Timestamp
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed)
    
    # Testar Emoji Personalizado
    @commands.command(help="Testar o emoji personalizado.")
    @commands.check(check_delay)
    async def testarEmoji(self, ctx):
        await ctx.send("<:catcrying:1315507542864171060>")
        
    @commands.command(name="shrek", help="Assista o filme do Shrek inteiro.")
    @commands.check(check_delay)
    async def shrek(self, ctx):
        file_path = "./downloads/shrekMovie.gif"
        
        try:
            await ctx.message.reply(file=discord.File(file_path))
        except FileNotFoundError:
            await ctx.send("❌ O arquivo do filme não foi encontrado.")
        except Exception as e:
            await ctx.send(f"❌ Ocorreu ao enviar o arquivo: {e}")
        
# Função para configurar o cog
async def setup(bot):
    # Verifica se o cog já foi carregado antes de adicionar novamente
    if "CommandsCogTeste" not in bot.cogs:
        await bot.add_cog(CommandsCogTeste(bot))  # Await ao adicionar o cog
    else:
        print("Cog 'CommandsCogTeste' já carregado!")
