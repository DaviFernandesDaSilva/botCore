import yt_dlp as yt_dlp
import discord
from discord.ext import commands
import asyncio
import os

from func.checks import check_delay

class Music(commands.Cog, name="Comandos de Música"):
    def __init__(self, bot):
        self.bot = bot

    async def search_music(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch5:{query}", download=False)  # Limitando para 5 resultados
            return search_results['entries']

    @commands.command(help="Toca uma música do YouTube. Pesquise pelo nome!")
    @commands.check(check_delay)
    async def play(self, ctx, *, search_query):
        """Comando para tocar música do YouTube, pesquisa pelo nome"""
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        search_results = await self.search_music(search_query)

        # Prepara a lista de opções para exibir (Top 5)
        options = []
        for i, entry in enumerate(search_results, 1):
            options.append(f"{i}. {entry['title']}")

        result_message = "\n".join(options[:5])  # Limita a 5 opções

        # Se a mensagem for muito grande, corta o excesso
        if len(result_message) > 2000:
            result_message = result_message[:1997] + "..."

        await ctx.send(f"Escolha um número para a música:\n{result_message}")

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit()

        try:
            response = await self.bot.wait_for('message', check=check, timeout=30)
            choice = int(response.content)
            if choice < 1 or choice > len(search_results):
                await ctx.send("Escolha inválida.")
                return
            selected_url = search_results[choice - 1]['url']

            # Perguntar se deseja parar a música atual antes de tocar a nova
            try:
                if ctx.voice_client.is_playing():
                    await ctx.send("Já estou tocando uma música! Você quer parar a música atual para tocar a nova? Responda 'sim' ou 'não'.")
                    
                    def stop_check(msg):
                        return msg.author == ctx.author and msg.content.lower() in ['sim', 'não']
                    
                    response = await self.bot.wait_for('message', check=stop_check, timeout=30)
                    
                    if response.content.lower() == 'sim':
                        ctx.voice_client.stop()  # Para a música atual
                    else:
                        await ctx.send("A música atual continuará tocando.")
                        return  # Se o usuário não quiser parar a música atual, não faz nada
            except:
                print("Ctx.voice_client não tem is_playing")

            # Toca a música escolhida
            await self.play_music(ctx, selected_url)
            
        except asyncio.TimeoutError:
            await ctx.send("Você não escolheu nenhuma opção a tempo!")
        except ValueError:
            await ctx.send("Escolha inválida! Tente novamente com um número válido.")


    async def play_music(self, ctx, url):
        """Função para tocar música a partir de um URL"""
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        # Verifica se o bot já está no canal de voz
        if ctx.voice_client is not None:
            # Se o bot está no canal correto, mas já está tocando, pare a música
            if ctx.voice_client.is_playing():
                await ctx.voice_client.stop()
                await asyncio.sleep(1)  # Dá um tempo para o player parar

        # Conecta ao canal de voz se o bot não estiver em nenhum
        if ctx.voice_client is None:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()  # Conecta ao canal de voz

        # Verifica se o bot está em um canal de voz e está pronto para tocar
        if ctx.voice_client.is_playing():
            await ctx.voice_client.stop()  # Para qualquer música que já esteja tocando

        try:
            # Baixa o áudio do link
            audio_url = await self.download_audio(url)
            if audio_url:
                # Inicia o processo de reprodução do áudio
                audio_source = discord.FFmpegPCMAudio(audio_url, executable="ffmpeg")
                ctx.voice_client.play(audio_source, after=lambda e: print(f'Erro ao tocar: {e}') if e else None)
                await ctx.send(f"Tocando agora: {url}", allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.send("Não foi possível obter o áudio da música.")
                await ctx.voice_client.disconnect()
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao tentar tocar a música: {e}")
            await ctx.voice_client.disconnect()

    async def download_audio(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',  # A melhor qualidade de áudio disponível
            'extractaudio': True,  # Extrai apenas o áudio
            'audioquality': 1,  # Melhor qualidade de áudio
            'outtmpl': './downloads/%(id)s.%(ext)s',  # Define o diretório de saída para o áudio
            'quiet': True,  # Não exibe mensagens do yt-dlp
            'noplaylist': True,  # Evita baixar playlists inteiras
            'simulate': True,  # Simula o download (não faz o download real, apenas obtém o link)
            'forceurl': True  # Força a obtenção do link diretamente
        }

        loop = asyncio.get_event_loop()

        def fetch_audio_url():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                # Procura por links de áudio direto que são compatíveis com o FFmpeg
                for format in info_dict['formats']:
                    # Filtra para pegar um formato de áudio adequado
                    if format.get('acodec') != 'none' and format.get('url'):
                        return format['url']
                return None

        # Chama a função de forma assíncrona e captura a URL
        audio_url = await loop.run_in_executor(None, fetch_audio_url)

        if audio_url:
            print(f"URL do áudio: {audio_url}")
        else:
            print("Nenhuma URL de áudio encontrada.")
        
        return audio_url



# Configuração do bot para carregar o cog
async def setup(bot):
    await bot.add_cog(Music(bot))