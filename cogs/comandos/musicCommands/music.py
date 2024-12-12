import yt_dlp as yt_dlp
import discord
from discord.ext import commands
import asyncio
from func.checks import check_delay

class Music(commands.Cog, name="Comandos de Música"):
    def __init__(self, bot):
        self.bot = bot
        self.current_ffmpeg_process = None  # Variável para armazenar o processo FFmpeg em execução

    async def search_audio(self, query):
        """Realiza a pesquisa de áudio no YouTube."""
        print(f"Buscando áudio para: {query}")  # Depuração
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                search_results = ydl.extract_info(f"ytsearch5:{query}", download=False)
                if 'entries' not in search_results or not search_results['entries']:
                    print("Nenhum resultado encontrado.")  # Depuração
                    return []  # Retorna uma lista vazia se não houver resultados
                return search_results['entries']
            except Exception as e:
                print(f"Erro ao buscar áudio: {e}")  # Depuração
                return []  # Caso ocorra algum erro na busca, retorna uma lista vazia

    async def download_audio(self, url):
        """Baixa o áudio do YouTube para reproduzir no canal de voz."""
        print(f"Baixando áudio de: {url}")  # Depuração
        ydl_opts = {
            'format': 'bestaudio/best',
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
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    for format in info_dict['formats']:
                        if format.get('acodec') != 'none' and format.get('url'):
                            print(f"URL do áudio encontrado: {format['url']}")  # Depuração
                            return format['url']
                    print("URL não encontrada.")  # Depuração
                    return None
            except Exception as e:
                print(f"Erro ao baixar áudio: {e}")  # Depuração
                return None  # Retorna None se houver erro ao extrair a URL

        # Chama a função de forma assíncrona e captura a URL
        audio_url = await loop.run_in_executor(None, fetch_audio_url)

        print(f"URL final do áudio: {audio_url}")  # Depuração
        return audio_url if audio_url else None  # Retorna a URL ou None

    async def play_music(self, ctx, url):
        """Função para tocar a música no canal de voz."""
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        # Baixa o áudio do link
        print(f"Tentando tocar música de URL: {url}")  # Depuração
        audio_url = await self.download_audio(url)
        if not audio_url:
            await ctx.send("Não foi possível obter o áudio da música.")
            return

        # Conecta ao canal de voz se o bot não estiver em nenhum
        if ctx.voice_client is None:
            channel = ctx.author.voice.channel
            try:
                voice_client = await channel.connect()  # Conecta ao canal de voz
                print("Conectado ao canal de voz!")  # Depuração
            except Exception as e:
                print(f"Erro ao conectar no canal de voz: {e}")
                await ctx.send("Não foi possível conectar ao canal de voz.")
                return
        else:
            voice_client = ctx.voice_client  # Usamos a conexão existente

        # Verifica se o bot já está tocando alguma música
        if voice_client.is_playing():
            await self.stop_audio(ctx)  # Para a música atual antes de tocar a nova

        try:
            # Inicia o processo de reprodução do áudio
            audio_source = discord.FFmpegPCMAudio(audio_url, executable="ffmpeg")
            voice_client.play(audio_source, after=lambda e: print(f'Erro ao tocar: {e}') if e else None)
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao tentar tocar a música: {e}")
            await self.stop_audio(ctx)  # Para e limpa ao ocorrer um erro
            await self.disconnect_voice(ctx)  # Desconecta se houver erro

    async def stop_audio(self, ctx):
        """Função para parar a música e liberar recursos"""
        if ctx.voice_client is not None and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Para a música atual

        # Limpar processo do FFmpeg se houver
        if self.current_ffmpeg_process:
            self.current_ffmpeg_process.kill()  # Encerra o processo FFmpeg
            self.current_ffmpeg_process = None

    async def disconnect_voice(self, ctx):
        """Função para desconectar do canal de voz de forma segura"""
        if ctx.voice_client:
            try:
                # Verifica se o bot está conectado antes de tentar desconectar
                if ctx.voice_client.is_connected():
                    await ctx.voice_client.disconnect()
                    print("Bot desconectado do canal de voz.")  # Depuração
                else:
                    print("Bot não estava conectado ao canal de voz.")  # Depuração
            except Exception as e:
                print(f"Erro ao tentar desconectar: {e}")  # Depuração

    @commands.command(name="play", aliases=["tocar","p"], help="Toca uma música do YouTube. Pesquise pelo nome!")
    @commands.check(check_delay)
    async def play(self, ctx, *, search_query):
        """Comando para tocar música do YouTube, pesquisa pelo nome"""
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return
        
        # Realiza a pesquisa e filtra os resultados
        print(f"Pesquisando músicas para a consulta: {search_query}")  # Depuração
        search_results = await self.search_audio(search_query)

        if not search_results:  # Verifica se não há resultados
            await ctx.send("Nenhuma música encontrada para a pesquisa.")
            return

        # Criando o embed de resultados
        embed = discord.Embed(
            title=f"🔍 Resultados da pesquisa para: {search_query}",
            description="Escolha uma música abaixo para ouvir:",
            color=discord.Color.blue()  # Usando uma cor mais vibrante
        )

        # Loop para adicionar cada resultado no embed
        for i, entry in enumerate(search_results[:5], 1):
            # Verifica se a duração existe e é um valor numérico
            if entry.get('duration') is not None and isinstance(entry['duration'], (int, float)):
                # Formatando a duração para o formato 1:35, 5:30, etc.
                minutes = int(entry['duration'] // 60)
                seconds = int(entry['duration'] % 60)
                duration = f"{minutes}:{seconds:02}"
            else:
                # Se a duração não for válida, define como "Desconhecido"
                duration = "Desconhecido"

            # Verificando se a chave 'thumbnail' existe
            thumbnail_url = entry.get('thumbnail', None)

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
        lista = await ctx.send(embed=embed)

        # Criando o menu suspenso
        class AudioSelect(discord.ui.View):
            def __init__(self, results):
                super().__init__(timeout=30)
                self.selected_url = None

                select = discord.ui.Select(placeholder="Escolha uma das opções de áudio...")

                for i, entry in enumerate(search_results[:5], 1):
                    select.add_option(label=f"{i}. {entry['title'][:95]}", value=entry['url'])

                select.callback = self.select_callback
                self.add_item(select)

            async def select_callback(self, interaction: discord.Interaction):
                self.selected_url = interaction.data['values'][0]
                await interaction.response.defer()
                self.stop()

        view = AudioSelect(search_results)
        await ctx.send("🔍 Escolha o áudio desejado no menu abaixo:", view=view)

        await view.wait()

        if view.selected_url:
            # Após a seleção, cria o embed com as informações da música
            selected_entry = next(entry for entry in search_results if entry['url'] == view.selected_url)
            
            # Criação do embed de música selecionada
            embed = discord.Embed(
                title="Tocando Agora: "+selected_entry['title'],
                description=f"Canal: {selected_entry['uploader']}\nDuração: {int(selected_entry['duration'] // 60)}:{int(selected_entry['duration'] % 60):02}",
                color=discord.Color.green()
            )

            # Adicionando a thumbnail se houver
            thumbnail_url = selected_entry.get('thumbnail')
            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)

            await ctx.send(embed=embed)
            # Agora, toca a música
            await self.play_music(ctx, view.selected_url)
        else:
            await ctx.send("❌ Você não escolheu nenhuma opção a tempo!")
            
        await lista.delete()

async def setup(bot):
    await bot.add_cog(Music(bot))
