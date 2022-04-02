from twitchio.ext import commands
from dotenv import load_dotenv
import os
from ossapi import OssapiV2, serialize_model
import re
import asyncio

load_dotenv()
user_id = os.getenv("USER_ID")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.getenv("TWITCH_ACCESS_TOKEN"), prefix='!', initial_channels=['xavTTV'])

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')
    @commands.command()
    async def track(self, ctx: commands.Context):
        if (ctx.author.name == "xavttv"):
            fecha = 0
            while True:
                print("nuevo bucle")
                url = osu.user_recent_activity(user_id)[0].beatmap.url
                match = re.fullmatch(r"\/b\/(?P<id>\d+)\?m=0", url)
                beatmap_id = match.group("id")
                if fecha != int(serialize_model(osu.user_recent_activity(user_id)[0].created_at)):
                    fecha = int(serialize_model(osu.user_recent_activity(user_id)[0].created_at))
                    fecha_top = int(serialize_model(osu.beatmap_user_score(beatmap_id=beatmap_id, user_id=user_id).score.created_at))
                    beatmap_name = serialize_model(osu.user_recent_activity(user_id)[0].beatmap.title)
                    if fecha != fecha_top:
                        rank = osu.user_recent_activity(user_id)[0].rank
                        scoreRank = osu.user_recent_activity(user_id)[0].scoreRank
                        # TODO : agregar el link al mapa
                        await ctx.send(f'Jugada reciente en el mapa {beatmap_name}, lugar obtenido {rank} con un rango de {scoreRank}')
                    else:
                        pp = round(float(serialize_model(osu.beatmap_user_score(beatmap_id=beatmap_id, user_id=user_id).score.pp)),2)
                        acc = str(round(float(serialize_model(osu.beatmap_user_score(beatmap_id=beatmap_id, user_id=user_id).score.accuracy)) * 100,2)) + '%'
                        combo = str(serialize_model(osu.beatmap_user_score(beatmap_id=beatmap_id, user_id=user_id).score.max_combo))
                        await ctx.send(f'Jugada reciente en el mapa {beatmap_name} con un pp de {pp} y una acc de {acc} y un combo de {combo}')
                await asyncio.sleep(10)
    @commands.command()
    async def profile(self, ctx: commands.Context):
        await ctx.send(f'Mi perfil de osu es {osu.user(user_id).username}, tengo {osu.user(user_id).statistics.pp} de pp, mi acc es de {round(float(osu.user(user_id).statistics.hit_accuracy),2)}% .  El link a mi perfil es el siguiente: https://osu.ppy.sh/users/{user_id}')
    @commands.command()
    async def top(self, ctx: commands.Context):
        string = ''
        res = osu.user_scores(user_id, "best")
        for i in range(3):
            string += f'{i+1}. {res[i].beatmapset.title} ({res[i].beatmap.difficulty_rating}) con un pp de {round(float(res[i].pp),2)}, un acc de {round(float(res[i].accuracy),2)*100}% y una rango de {str(res[i].rank).split("Grade.")[1]}\n'
        await ctx.send(string)
osu = OssapiV2(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), os.getenv("REDIRECT_URL"))
bot = Bot()
bot.run()




