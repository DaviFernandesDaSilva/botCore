import yt_dlp as yt_dlp
import discord
from discord.ext import commands
import asyncio
import os

from func.checks import check_delay
class CustomHelp(commands.Cog, name="Comandos de ajuda"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help", aliases=["ajuda"],help="Exibe a lista de comandos disponíveis ou ajuda específica para um comando.")
    async def help(self, ctx, comando: str = None):
        """Comando personalizado para exibir a lista de comandos ou detalhes de um comando específico."""
        if comando is None:
            # Exibe a lista de comandos organizados por categoria (Cog)
            embed = discord.Embed(
                title="Comandos Disponíveis",
                description="Use `!!ajuda <comando>` para obter detalhes sobre um comando específico.",
                color=discord.Color.blue()
            )
            
            for cog_name, cog in self.bot.cogs.items():
                # Obtém os comandos de cada Cog
                comandos_cog = [cmd for cmd in cog.get_commands() if not cmd.hidden]
                if comandos_cog:
                    comandos_formatados = [f"`{cmd.name}`" for cmd in comandos_cog]
                    embed.add_field(name=cog_name, value=", ".join(comandos_formatados), inline=False)

            # Inclui comandos que não pertencem a uma Cog
            comandos_sem_cog = [cmd for cmd in self.bot.commands if not cmd.cog_name and not cmd.hidden]
            if comandos_sem_cog:
                comandos_formatados = [f"`{cmd.name}`" for cmd in comandos_sem_cog]
                embed.add_field(name="Sem Categoria", value=", ".join(comandos_formatados), inline=False)

            embed.set_footer(text="Bot do Davipbr15 - 2024")
            await ctx.send(embed=embed)

        else:
            # Exibe os detalhes de um comando específico
            comando_encontrado = self.bot.get_command(comando)
            if comando_encontrado is None or comando_encontrado.hidden:
                await ctx.send(f"❌ Comando `{comando}` não encontrado ou está oculto.")
                return

            embed = discord.Embed(
                title=f"Ajuda para `{comando_encontrado.name}`",
                description=comando_encontrado.help or "Sem descrição disponível.",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Uso",
                value=f"`{ctx.prefix}{comando_encontrado.name} {comando_encontrado.signature or ''}`",
                inline=False
            )
            if comando_encontrado.aliases:
                embed.add_field(
                    name="Apelidos",
                    value=", ".join([f"`{alias}`" for alias in comando_encontrado.aliases]),
                    inline=False
                )
            embed.set_footer(text="Bot do Davipbr15 - 2024")
            await ctx.send(embed=embed)


# Configuração para adicionar o cog
async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
