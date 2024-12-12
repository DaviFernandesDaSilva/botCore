import os
from subprocess import run
from discord.ext import commands
import yt_dlp
import asyncio
import discord
import re

from func.checks import check_delay

# Função para limpar o nome do arquivo
def clean_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', ' ', filename)  # Remove caracteres inválidos

class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def search_audio(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch5:{query}", download=False)
            return search_results['entries']

    @commands.command(name="downloadAudio",
                      aliases = ["dAudio", "baixarAudio", "audio", "baixaAudio", "baixar", "getAudio", "baixarMúsica"],
                      help="Faz o download do áudio de um vídeo ou pesquisa por áudio. (youtube, twitter, etc.). ( PESQUISA APENAS YOUTUBE )")
    @commands.check(check_delay)
    async def downloadAudio(self, ctx, *, query):
        """Comando para baixar o áudio de um vídeo ou pesquisar áudio."""

        if self.is_valid_audio_url(query):
            # É uma URL válida, inicia o download diretamente
            await self.download_from_url(ctx, query)
        else:
            # Realiza a pesquisa e permite escolher uma das opções
            await self.download_from_search(ctx, query)

    async def download_from_url(self, ctx, url):
        """Realiza o download de áudio diretamente de uma URL."""
        processing_message = await ctx.send("🔄 Processando o download do áudio...")

        try:
            output_dir = "./downloads"
            os.makedirs(output_dir, exist_ok=True)

            def download_audio():
                with yt_dlp.YoutubeDL() as ydl:
                    info = ydl.extract_info(url, download=False)
                    clean_title = clean_filename(info['title'])
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{output_dir}/{clean_title}.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.extract_info(url, download=True)

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, download_audio)
            clean_title = clean_filename(info['title'])
            downloaded_file = f"{output_dir}/{clean_title}.mp3"

            await ctx.message.reply(f"✅ O áudio `{clean_title}.mp3` foi baixado com sucesso!", file=discord.File(downloaded_file))
            os.remove(downloaded_file)

        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao tentar baixar o áudio: {e}")

        finally:
            await processing_message.delete()

    async def download_from_search(self, ctx, query):
        """Realiza a pesquisa de áudio e baixa a opção escolhida."""
        search_results = await self.search_audio(query)

        # Filtrando os resultados para limitar músicas de até 10 minutos (600 segundos)
        filtered_results = [entry for entry in search_results if entry['duration'] <= 600]

        if not filtered_results:
            await ctx.send("❌ Nenhuma música encontrada com duração de até 10 minutos.")
            return

        # Criação do embed de resultados
        embed = discord.Embed(
            title=f"🔍 Resultados da pesquisa para: {query}",
            description="Escolha uma música abaixo para fazer o download:",
            color=discord.Color.blue()  # Usando uma cor mais vibrante
        )

        # Adicionando uma imagem de capa (opcional)
        embed.set_thumbnail(url="https://link.da.imagem/de/capa.png")  # Adicione um link de imagem para a capa

        # Loop para adicionar cada resultado no embed
        for i, entry in enumerate(filtered_results[:5], 1):
            # Formatando a duração para o formato 1:35, 5:30, etc.
            minutes = int(entry['duration'] // 60)
            seconds = int(entry['duration'] % 60)
            duration = f"{minutes}:{seconds:02}"  # Formata os segundos para sempre ter 2 dígitos

            # Verificando se a chave 'thumbnail' existe
            thumbnail_url = entry.get('thumbnail', None)  # Usa 'None' se a chave não existir

            # Usando blockquote para destacar o título e as informações
            embed.add_field(
                name=f"**{i}. {entry['title'][:90]}**",  # Exibe o título da música, cortado para 90 caracteres
                value=f"> **Duração**: {duration}\n> **Canal**: {entry['uploader']}",
                inline=False
            )

            # Adicionando a thumbnail da música, caso exista
            if thumbnail_url:
                embed.set_footer(text="Clique na música para mais informações.")  # Sugerir ação
                embed.set_image(url=thumbnail_url)  # Adiciona a imagem da música

        # Enviando o embed para o canal
        await ctx.send(embed=embed)

        # Criando o menu suspenso
        class AudioSelect(discord.ui.View):
            def __init__(self, results):
                super().__init__(timeout=30)
                self.selected_url = None

                select = discord.ui.Select(placeholder="Escolha uma das opções de áudio...")

                for i, entry in enumerate(filtered_results[:5], 1):
                    select.add_option(label=f"{i}. {entry['title'][:95]}", value=entry['url'])

                select.callback = self.select_callback
                self.add_item(select)

            async def select_callback(self, interaction: discord.Interaction):
                self.selected_url = interaction.data['values'][0]
                await interaction.response.defer()
                self.stop()

        view = AudioSelect(filtered_results)
        await ctx.send("🔍 Escolha o áudio desejado no menu abaixo:", view=view)

        await view.wait()

        if view.selected_url:
            await self.download_from_url(ctx, view.selected_url)
        else:
            await ctx.send("❌ Você não escolheu nenhuma opção a tempo!")




    def is_valid_audio_url(self, url):
        """Verifica se a URL é válida para sites de áudio/vídeo suportados pelo yt-dlp."""
        platform_regex = {
            'youtube': r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://(?:www\.)?youtu\.be/[\w-]+)',
            'vimeo': r'(https?://(?:www\.)?vimeo\.com/\d+)',
            'dailymotion': r'(https?://(?:www\.)?dailymotion\.com/video/[\w-]+)',
        }

        for platform, regex in platform_regex.items():
            if re.match(regex, url):
                return True
        return False

async def setup(bot):
    await bot.add_cog(Downloader(bot))
