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
    # Substitui caracteres inválidos do Windows por underline ou os remove
    return re.sub(r'[\\/:*?"<>|]', ' ', filename)

class DownloaderVideo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Faz o download do vídeo de um link e envia no Discord. ( twitter, dailymotion, vimeo , instagram )")
    @commands.check(check_delay)
    async def downloadVideo(self, ctx, *, url):
        if not self.is_valid_audio_url(url):
            await ctx.send("❌ A URL fornecida não é válida por enquanto.\n Aguarde atualizações ou forneça uma URL válida.")
            return

        processingMessage = await ctx.send("<a:loading:1316093726111698974> **Processando o download do vídeo...**")

        try:
            output_dir = "./downloads"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            def download_video():
                try:
                    with yt_dlp.YoutubeDL() as ydl:
                        info = ydl.extract_info(url, download=False)
                        clean_title = clean_filename(info['title'])
                        ydl_opts = {
                            'format': 'bestvideo+bestaudio/best',
                            'outtmpl': f'{output_dir}/{clean_title}.%(ext)s',
                            'quiet': True,
                            'extractor_args': {
                                'twitter': {
                                    'guest_token': 'new',
                                }
                            }
                        }
                        ydl_opts['outtmpl'] = f'{output_dir}/{clean_title}.%(ext)s'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            return ydl.extract_info(url, download=True)
                except Exception as e:
                    print(f"Erro ao baixar o vídeo: {e}")
                    return None

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, download_video)

            clean_title = clean_filename(info['title'])
            downloaded_file = f"{output_dir}/{clean_title}.mp4"

            file_size = os.path.getsize(downloaded_file)
            max_size = 8 * 1024 * 1024 # 8MB

            if file_size > max_size:
                compressMsg = await ctx.send("❌ O arquivo é muito grande para ser enviado diretamente. Comprimindo...")
                compressed_file = f"{output_dir}/{clean_title}_compressed.mp4"
                
                run(['ffmpeg', '-i', downloaded_file, '-vcodec', 'libx264', '-crf', '28', '-preset', 'fast', compressed_file])
                
                compressed_size = os.path.getsize(compressed_file)
                await compressMsg.delete()
                
                if compressed_size <= max_size:
                    await ctx.message.reply(f"✅ O vídeo `{clean_title}.mp4` foi comprimido e enviado com sucesso!", file=discord.File(compressed_file))
                    print(f"Arquivo comprimido {clean_title}_compressed.mp4 enviado com sucesso!")
                else:
                    compressFail = await ctx.send("❌ O arquivo ainda ficou está muito grande após a compressão.\n❌ Não foi possível enviar no Discord.")
            else:
                await ctx.message.reply(f"✅ O vídeo `{clean_title}.mp4` foi enviado com sucesso!", file=discord.File(downloaded_file))
                print(f"Arquivo {clean_title}.mp4 enviado com sucesso!")
            os.remove(downloaded_file)
        except Exception as e:
            await processingMessage.delete()
            print(f"❌ Erro: {e}")
            await ctx.send(f"❌ Ocorreu um erro no download do vídeo. Tente novamente.")
        finally:
            await processingMessage.delete()
            

        
    def is_valid_audio_url(self, url):
        """Verifica se a URL é válida para sites de áudio/vídeo suportados pelo yt-dlp."""

        # Dicionário com plataformas e suas expressões regulares
        platform_regex = {
            'soundcloud': r'(https?://(?:www\.)?soundcloud\.com/[\w\-]+/[\w\-]+)',
            'vimeo': r'(https?://(?:www\.)?vimeo\.com/\d+)',
            'dailymotion': r'(https?://(?:www\.)?dailymotion\.com/video/[\w-]+)',
            'x': r'(https?://(?:www\.)?x\.com/[\w\-]+/status/\d+)',
            'instagram': r'(https?://(?:www\.)?instagram\.com/p/[\w\-]+)',
        }

        # Itera sobre as expressões regulares para as plataformas e verifica a URL
        for platform, regex in platform_regex.items():
            if re.match(regex, url):
                return True  # URL válida para a plataforma encontrada

        return False  # Nenhuma plataforma válida encontrada

async def setup(bot):
    if "DownloaderVideo" not in bot.cogs:
        await bot.add_cog(DownloaderVideo(bot))
    else:
        print("Cog 'DownloaderVideo' já carregado!")
