import os
from subprocess import run
from discord.ext import commands
import yt_dlp
import asyncio
import discord
import re

# Função para limpar o nome do arquivo
def clean_filename(filename):
    # Substitui caracteres inválidos do Windows por underline ou os remove
    return re.sub(r'[\\/:*?"<>|]', ' ', filename)

class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Faz o download do áudio de um vídeo do YouTube.")
    async def downloadAudio(self, ctx, *, url):
        """Comando para baixar o áudio de um vídeo do YouTube"""
        processingMessage = await ctx.send("🔄 Processando o download do áudio...")

        try:
            # Diretório de saída
            output_dir = "./downloads"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Função para baixar o áudio
            def download_audio():
                with yt_dlp.YoutubeDL() as ydl:
                    # Obtém informações do vídeo
                    info = ydl.extract_info(url, download=False)
                    # Limpa o título do vídeo para criar um nome válido
                    clean_title = clean_filename(info['title'])
                    # Configura a opção de saída com o nome limpo
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{output_dir}/{clean_title}.%(ext)s',  # Usando o título limpo
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True
                    }
                    # Realiza o download com o título já limpo
                    ydl_opts['outtmpl'] = f'{output_dir}/{clean_title}.%(ext)s'
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.extract_info(url, download=True)

            # Executa o download de forma assíncrona
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, download_audio)

            clean_title = clean_filename(info['title'])
        
            # Caminho do arquivo baixado
            downloaded_file = f"{output_dir}/{clean_title}.mp3"

            # Verifica o tamanho do arquivo antes de enviar
            file_size = os.path.getsize(downloaded_file)
            max_size = 8 * 1024 * 1024  # 8 MB

            if file_size > max_size:
                # Compacta o arquivo
                compressed_file = f"{output_dir}/{clean_title}_compressed.mp3"
                self.compress_audio(downloaded_file, compressed_file)

                # Envia o arquivo compactado ou avisa sobre o tamanho
                if os.path.exists(compressed_file):
                    print("Arquivo COMPACTADO " + clean_title + ".mp3 enviado com sucesso!")
                    await ctx.message.reply(f"✅  O áudio `{clean_title}.mp3` foi enviado com sucesso!", file=discord.File(downloaded_file))
                    os.remove(compressed_file)
                    os.remove(downloaded_file)
                else:
                    await ctx.send("❌ Não foi possível compactar o arquivo.")
            else:
                # Envia o arquivo diretamente
                await ctx.message.reply(f"✅  O áudio `{clean_title}.mp3` foi enviado com sucesso!", file=discord.File(downloaded_file))
                print("Arquivo " + clean_title + ".mp3 enviado com sucesso!")
                os.remove(downloaded_file)

        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")
            
        await processingMessage.delete()
        

    def compress_audio(self, input_file, output_file, bitrate="96k"):
        """Função para compactar o áudio usando FFmpeg"""
        run(["ffmpeg", "-i", input_file, "-b:a", bitrate, output_file, "-y"])

async def setup(bot):
    if "Downloader" not in bot.cogs:
        await bot.add_cog(Downloader(bot))
    else:
        print("Cog 'Downloader' já carregado!")
