import asyncio
import discord
from discord.ext import commands
import os
import random
import json
import aiofiles
from dotenv import load_dotenv

load_dotenv()

PARTICIPANTES_FILE = "gayDaSemana.json"

# Função para carregar os dados de contagem
async def load_command_counts():
    if os.path.exists(PARTICIPANTES_FILE):
        async with aiofiles.open(PARTICIPANTES_FILE, "r") as f:
            try:
                data = await f.read()
                if data:
                    return json.loads(data)
                else:
                    return []  # Retorna lista vazia caso o arquivo esteja vazio
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                return []
    else:
        print(f"O arquivo {PARTICIPANTES_FILE} não foi encontrado.")
        return []  # Retorna lista vazia se o arquivo não existir

# Função para salvar os dados
async def save_command_counts(ids_usuarios):
    async with aiofiles.open(PARTICIPANTES_FILE, 'w') as f:
        try:
            await f.write(json.dumps(ids_usuarios, indent=4))
            print(f"Dados salvos: {ids_usuarios}")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

class GayDaSemana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ids_usuarios = []

        # Carregar dados dos usuários
        self.bot.loop.create_task(self.load_user_data())

    async def load_user_data(self):
        self.ids_usuarios = await load_command_counts()

    async def save_user_data(self):
        await save_command_counts(self.ids_usuarios)

    @commands.command(name="gaydasemana")
    @commands.has_permissions(manage_roles=True)
    async def dar_role(self, ctx, action=None, user: discord.Member = None):
        if ctx.guild.id != 610969108179320864:
            await ctx.send("❌ Este comando só pode ser usado no Universo Retardado!")
            return

        if action == "add" and user:
            if user.id not in self.ids_usuarios:
                self.ids_usuarios.append(user.id)
                await self.save_user_data()
                await ctx.message.reply(f"✅ O usuário {user.mention} foi adicionado à lista de participantes do gay da semana!")
            else:
                await ctx.message.reply(f"❌ O usuário {user.mention} já está na lista!")
            return

        if action == "remover" and user:
            if user.id in self.ids_usuarios:
                self.ids_usuarios.remove(user.id)
                await self.save_user_data()
                await ctx.message.reply(f"✅ O usuário {user.mention} foi removido da lista de participantes do gay da semana!")
            else:
                await ctx.message.reply(f"❌ O usuário {user.mention} não está na lista de participantes!")
            return

        if action == "participantes":
            # Usando fetch_member para garantir que todos os membros sejam recuperados
            membros = await asyncio.gather(*[ctx.guild.fetch_member(user_id) for user_id in self.ids_usuarios])
            membros_validos = [membro for membro in membros if membro is not None]

            if not membros_validos:
                await ctx.send("Não foi possível encontrar participantes da lista.")
                return

            participantes_mention = [membro.mention for membro in membros_validos]
            participantes_str = "\n".join(participantes_mention)

            embed = discord.Embed(
                title="🏳️‍🌈 Participantes do Gay da Semana 🏳️‍🌈",
                description=participantes_str,
                color=discord.Color.pink()
            )
            await ctx.send(embed=embed)
            return

        # Caso contrário, escolher um gay da semana aleatório
        membros = await asyncio.gather(*[ctx.guild.fetch_member(user_id) for user_id in self.ids_usuarios])
        membros_validos = [membro for membro in membros if membro is not None]

        if not membros_validos:
            await ctx.send("Não foi possível encontrar nenhum usuário da lista.")
            return

        usuario_aleatorio = random.choice(membros_validos)

        embed = discord.Embed(
            title="🏳️‍🌈 Gay da Semana 🏳️‍🌈",
            description=f"**🏳️‍🌈 {usuario_aleatorio.display_name}** é o gay da semana! 🏳️‍🌈",
            color=discord.Color.pink()
        )
        embed.set_image(url=usuario_aleatorio.avatar.url)
        embed.set_footer(text=f"Escolhido por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.send(f"🎲 O Gay da Semana é....  🏳️‍🌈")
        await asyncio.sleep(1)  # Espera de 1 segundo com await
        await ctx.send(embed=embed)

        role_name = "GAY DA SEMANA"
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not role:
            await ctx.send("❌ O cargo 'GAY DA SEMANA' não existe no servidor!")
            return

        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("🚫 **Sem permissão para gerenciar cargos!**")
            return

        if role.position >= ctx.guild.me.top_role.position:
            await ctx.send("🚫 **O cargo bot está abaixo da hierarquia.**")
            return

        for current_member in ctx.guild.members:
            if role in current_member.roles:
                await current_member.remove_roles(role)
                break

        try:
            if role in usuario_aleatorio.roles:
                await ctx.send(f"🏳️‍🌈 {usuario_aleatorio.mention} já tem o cargo {role_name}. 🏳️‍🌈")
            else:
                await usuario_aleatorio.add_roles(role)
                await ctx.send(f"🏳️‍🌈 {usuario_aleatorio.mention} agora é o novo {role_name}! 🏳️‍🌈")
        except discord.Forbidden:
            await ctx.reply(f"🚫  **Você não tem permissão para isso!**", mention_author=False)
        finally:
            await self.save_user_data()

# Setup do Cog
async def setup(bot):
    await bot.add_cog(GayDaSemana(bot))
