import pdfcrowd
import discord
from discord.ext import commands
import config
import datetime
import os
from PIL import Image

client = pdfcrowd.HtmlToImageClient(config.username, config.api_token)
client.setOutputFormat('jpg')
bot = commands.Bot(command_prefix=config.prefix)


def Combine(time, text):
    html = config.part1 + time + config.part2 + text + config.part3
    return html


def Crop(length, way):
    if length < 126:
        if length*7.6+70 > 180:
            x = length*7.6+100
        else:
            x = 180
        im = Image.open(way)
        im1 = im.crop((0, 0, int(x), 48))
        im1.save(way)


@bot.command(name='SAS')
async def answer(ctx, *args):
    way = 'users/' + str(ctx.author.id)
    if not os.path.exists(way):
        os.makedirs(way)
    file = open(way+"/sas.html", "a", encoding='utf-8')
    text = ''
    for g in args:
        text += str(g) + ' '
    file.write(Combine(datetime.datetime.now().strftime("%d.%m.%Y"), text))
    file.close()
    client.convertFileToFile(way+'/sas.html', way+'/sas.jpg')
    Crop(len(text), way + "/sas.jpg")
    await ctx.send(file=discord.File(way + "/sas.jpg"))
    os.remove(way+'/sas.html')
    os.remove(way+'/sas.jpg')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=config.bot_activity))


bot.run(config.TOKEN)
