import discord
from discord.ext import commands
from func.checks import check_delay

class CustomHelp(commands.Cog, name="Comandos de ajuda"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["ajuda"], help="Exibe a lista de comandos disponíveis ou ajuda específica para um comando.")
    @commands.check(check_delay)
    async def help(self, ctx, comando: str = None):
        """Comando personalizado para exibir a lista de comandos ou detalhes de um comando específico."""
        
        if comando is None:
            # Exibe a lista de comandos organizados por categoria (Cog)
            comandos = {}
            for cog_name, cog in self.bot.cogs.items():
                comandos_cog = [cmd for cmd in cog.get_commands() if not cmd.hidden]
                if comandos_cog:
                    comandos[cog_name] = [f"`{cmd.name}`" for cmd in comandos_cog]
            
            # Inclui comandos que não pertencem a uma Cog
            comandos_sem_cog = [cmd for cmd in self.bot.commands if not cmd.cog_name and not cmd.hidden]
            if comandos_sem_cog:
                comandos["Sem Categoria"] = [f"`{cmd.name}`" for cmd in comandos_sem_cog]

            # Organiza os comandos em páginas (10 comandos por página)
            comandos_por_pagina = 10
            pages = []
            page = []
            for cog_name, cmds in comandos.items():
                for cmd in cmds:
                    if len(page) == comandos_por_pagina:
                        pages.append(page)
                        page = []
                    page.append(f"{cmd}")
            if page:  # Adiciona a última página se houver comandos restantes
                pages.append(page)
            
            # Envia as páginas com os comandos
            current_page = 0
            await self.send_help_page(ctx, pages, current_page)

        else:
            # Exibe os detalhes de um comando específico
            comando_encontrado = self.bot.get_command(comando)
            if comando_encontrado is None or comando_encontrado.hidden:
                await ctx.send(f"❌ Comando `{comando}` não encontrado ou está oculto.")
                return

            embed = discord.Embed(
                title=f"Ajuda para `{comando_encontrado.name}`",
                description=comando_encontrado.help or "Sem descrição disponível.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Uso",
                value=f"`{ctx.prefix}{comando_encontrado.name} {comando_encontrado.signature or ''}`",
                inline=False
            )
            if comando_encontrado.aliases:
                embed.add_field(
                    name="Outras formas de chamar o mesmo comando",
                    value=", ".join([f"`!!{alias}`" for alias in comando_encontrado.aliases]),
                    inline=False
                )
            embed.set_footer(text="Bot do Davipbr15 - 2024")
            await ctx.send(embed=embed)

    async def send_help_page(self, ctx, pages, current_page):
        embed = discord.Embed(
            title="Comandos Disponíveis",
            description=f"Use `!!ajuda <comando>` para obter detalhes sobre um comando específico.\n\n" + "\n".join(pages[current_page]),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Página {current_page + 1} de {len(pages)} | Bot do Davipbr15 - 2024")
        message = await ctx.send(embed=embed)

        # Adiciona as reações para navegação
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        # Função para capturar as reações e navegar pelas páginas
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            if str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
            elif str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                current_page += 1

            # Atualiza a página
            embed = discord.Embed(
                title="Comandos Disponíveis",
                description=f"Use `!!ajuda <comando>` para obter detalhes sobre um comando específico.\n\n" + "\n".join(pages[current_page]),
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Página {current_page + 1} de {len(pages)} | Bot do Davipbr15 - 2024")
            await message.edit(embed=embed)

            # Remove as reações antigas para evitar problemas de múltiplas reações
            await message.remove_reaction(reaction, user)

# Configuração para adicionar o cog
async def setup(bot):
    await bot.add_cog(CustomHelp(bot))