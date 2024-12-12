import discord
from discord.ext import commands


class ContextMenuCog(commands.Cog, name="Comandos de menu de contexto"):
    def __init__(self, bot):
        self.bot = bot
        
        @discord.app_commands.context_menu(name="Informação Rápida")
        async def quickInfo(interaction: discord.Interaction, member: discord.Member):
            info_embed = discord.Embed(title=f"Informações rápidas sobre {member.name}", description="Exibindo algumas informações sobre este usuário.", color=member.color)
            info_embed.add_field(name="Name:", value=member.name, inline=False)
            info_embed.add_field(name="ID:", value=member.id, inline=False)
            
            statusMap = {
                discord.Status.online: "Online",
                discord.Status.idle: "Ausente",
                discord.Status.dnd: "Não Perturbe",
                discord.Status.offline: "Offline",
            }   
            if isinstance(member, discord.Member):
                status = statusMap.get(member.status, "Desconhecido")
                activity = member.activity.name if member.activity else "Nenhuma atividade"
            else:
                status = "Desconhecido"
                activity = "Nenhuma atividade"

            info_embed.add_field(name="Status:", value=status, inline=False)
            
            info_embed.add_field(name="Registrado em:",
                                 value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"))
            info_embed.set_thumbnail(url=member.avatar)
            
            await interaction.response.send_message(embed=info_embed, ephemeral=True)
            
        self.bot.tree.add_command(quickInfo)

        # Comando de Menu de Contexto
        @discord.app_commands.context_menu(name="Teste de DM")
        async def send_dm(interaction: discord.Interaction, member: discord.Member):
            try:
                await member.send("Testando DM, parece que funcionou <:catcrying:1315507542864171060>")  # Envia a mensagem "Teste" para o usuário
                await interaction.response.send_message("Mensagem DM enviada com sucesso!", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Não consegui enviar a mensagem privada.", ephemeral=True)
                
        self.bot.tree.add_command(send_dm)

        
        async def cog_unload(self):
            # Remove o comando de menu de contexto ao descarregar o cog
            self.bot.tree.remove_command("Informação Rápida", type=discord.AppCommandType.user)
            self.bot.tree.remove_command("Teste", type=discord.AppCommandType.user)
        

async def setup(bot):
    if "ContextMenuCog" not in bot.cogs:
        await bot.add_cog(ContextMenuCog(bot))
    else:
        print("Cog 'ContextMenuCog já carregado!")