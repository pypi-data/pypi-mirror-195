import datetime
from fortnitepy.ext import commands
import fortnitepy
from .settings import BotSettings

class PartyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: BotSettings) -> None:
        self.bot = bot
        self.settings = settings


    @commands.command()
    async def help(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        await ctx.send("---------------Commands 1/1---------------\n"+"- !skin (name)  /  equip (name) skin\n"+"- !emote (name)  /  equip (name) emote\n"+"- !backpack (name)  /  equip (name) backpack\n"+"- !pickaxe (name)  /  equip (name) pickaxe\n"+"- !emoji (name)  /  equip (name) emoji\n"+"- !purpleskull  /  Skull Trooper (purple)\n"+"- !pinkghoul  /  Ghoul Trooper (pink)\n"+"- !checkeredrenegade  /  Renegade Raider (checkered)\n"+"- !renegade  /  equip Renegade Raider\n"+"- !floss  /  Floss emote\n"+"- !hologram  /  Star Wars hologram\n"+"- !tbd  /  equip tbd\n"+"- !friends  /  list of my friends\n"+"- !dc  /  dc-sever link\n"+"- !help  /  List of all commands")
        d = datetime.datetime.now()
        print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m executed command: " + f"\033[1;32;49m !help " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        


    @commands.command()
    async def friends(self,  ctx: fortnitepy.ext.commands.Context): 
        hours = self.settings.hours
        online = 0
        offline = 0
        for friend in self.bot.friends:
            if friend.is_online():
                online = online + 1
            else:
                offline = offline + 1 
        await ctx.send(f"Online Friends = {online} / Offline Friends = {offline}\n")
        d = datetime.datetime.now()
        print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m executed command: " + f"\033[1;32;49m !friends " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    
    @commands.command()
    async def dc(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        await ctx.send("Zockerwolf76s dc-server:  https://dsc.gg/zockerwolf")
        d = datetime.datetime.now()
        print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m executed command: " + f"\033[1;32;49m !dc " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        