import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

from func.checks import check_delay

# Carrega as variáveis do arquivo .env
load_dotenv()

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_url = "https://meme-api.com/gimme/MemesBR"
        self.blocked_subreddits = [
            "nsfw", "porn", "hentai", "gore", "adultcontent", "violence", "18+", 
            "darkhumor", "offensive", "deepfakes", "realgirls", "rule34", "gonewild", 
            "blowjobs", "nudes", "erotica", "incest", "bdsm", "fetish", "hardcore", 
            "cumsluts", "asianporn", "blackporn", "gayporn", "lesbianporn", 
            "milf", "teenporn", "amateurporn", "extreme", "rape", "abuse", "snuff", 
            "scat", "pedobait", "bestiality", "necrophilia", "drugs", "cartel", 
            "murder", "suicide", "selfharm", "watchpeopledie", "fights", "torture", 
            "graphic", "shocking", "beheadings", "creepy", "cursedimages", 
            "illegal", "piracy", "scams", "cringeanarchy", "coomer", 
            "hardcoreahegao", "homemade", "kink", "sex", "weirdporn", "amateursgonewild",
            "blood", "cutting", "edgelord", "loli", "shota", "rapeplay", "cryingfetish",
            "vomit", "darkweb", "extremefetish", "publicfreakout", "childfree", 
            "traphentai", "tiktoknsfw", "dubcon", "nonconsent", "bdsmgonewild", 
            "sexwithrobots", "unethical", "cannibalism", "cartelviolence", 
            "deadkids", "disturbing", "gruesome", "traumatica", "guro", 
            "porninseconds", "hardcorecumsluts", "onlyfansleaks", "camgirls", 
            "hotwife", "megathreads", "totallynotporn", "wtf", "rageporn", "gross",
            "baddragon", "furryporn", "animalabuse", "humiliationfetish"
        ]


    @commands.command(name="meme", help="Busca um meme. Use sem parâmetro para MemesBR ou especifique um subreddit.")
    @commands.check(check_delay)
    @commands.is_owner()
    async def meme(self, ctx, subreddit: str = None):  
        # Valida o subreddit ou usa o padrão
        if subreddit and subreddit.lower() in self.blocked_subreddits:
            await ctx.send(f"❌ O subreddit `{subreddit}` está bloqueado devido a conteúdo inadequado.")
            return

        url = self.default_url if not subreddit else f"https://meme-api.com/gimme/{subreddit}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    # Verifica se o meme retornado é NSFW
                    if data.get("nsfw", False):  # "nsfw" é uma chave na resposta da meme-api
                        await ctx.send("❌ O meme retornado é marcado como NSFW. Tente novamente!")
                        return

                    # Cria e envia o embed
                    embed = discord.Embed(
                        title=f"{data['title']}",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=data['url'])
                    embed.set_footer(text=f"Subreddit: {data['subreddit']}")
                    await ctx.send(embed=embed)

                elif response.status == 404:
                    await ctx.send("❌ Post não encontrado ou subreddit inválido.")
                elif response.status == 403:
                    await ctx.send("❌ O Subreddit é privado ou está trancado.")
                elif response.status == 400:
                    await ctx.send("❌ O Subreddit citado existe, porém não há posts válidos.")
                else:
                    await ctx.send(f"❌ Erro ao acessar a API. Código: {response.status}")

async def setup(bot):
    if "MemeCog" not in bot.cogs:
        await bot.add_cog(MemeCog(bot))
    else:
        print("Cog 'MemeCog' já carregado!")
