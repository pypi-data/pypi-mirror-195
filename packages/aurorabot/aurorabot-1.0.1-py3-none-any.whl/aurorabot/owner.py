import datetime
from fortnitepy.ext import commands
import fortnitepy
from .settings import BotSettings

from aurorabot.bot import AuroraBot

class OwnerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: BotSettings) -> None:
        self.bot = bot
        self.settings = settings
        

    @commands.command()
    async def promote(self,  ctx: fortnitepy.ext.commands.Context, * , content: str = None):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            if content == None:
                owner = await self.bot.fetch_user(ctx.author.display_name)
                member = self.bot.party.get_member(owner.id)
                await member.promote()
                await ctx.send("Promoted Member: " + ctx.author.display_name)
            
            else:
                user = await self.bot.fetch_user(content)
                rmember = self.bot.party.get_member(user.id)
                await rmember.promote()
                await ctx.send("Promoted Member: " + user.display_name)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)")  
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m TRIED Owner command:" + f"\033[1;31;49m !promote " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.command()
    async def cban(self, ctx: fortnitepy.ext.commands.Context, content: str):
        owner = self.settings.owner
        hours = self.settings.hours
        if (ctx.author.display_name) == owner:
            user = await self.bot.fetch_user(content)
            await self.bot.party.chatban_member(user.id)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !cban " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    
    @commands.command()
    async def sitin(self,  ctx: fortnitepy.ext.commands.Context):
        owner = self.settings.owner
        hours = self.settings.hours
        if (ctx.author.display_name) == owner:
            await self.bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !sitin " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        
    
    
    @commands.command()
    async def sitout(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            await self.bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !sitout " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    


    @commands.command()
    async def lobby(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        owner = self.settings.owner  
        if (ctx.author.display_name) == owner:
            d = datetime.datetime.now()
            await self.bot.party.me.clear_in_match()
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !lobby " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    
    @commands.command()
    async def match(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        owner = self.settings.owner  
        if (ctx.author.display_name) == owner:
            d = datetime.datetime.now()
            await self.bot.party.me.set_in_match(players_left=1, started_at=None)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !match " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    
    @commands.command()
    async def unready(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            await self.bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !unready " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
    


    @commands.command()
    async def ready(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            await self.bot.party.me.set_ready(fortnitepy.ReadyState.READY)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !ready " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    

    @commands.command()
    async def banner(self,  ctx: fortnitepy.ext.commands.Context, * ,content: str):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            d = datetime.datetime.now()
            await self.bot.party.me.set_banner(icon=content)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !banner " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.command()
    async def banner(self,  ctx: fortnitepy.ext.commands.Context, * ,content: str):
        hours = self.settings.hours
        owner = self.settings.owner
        if (ctx.author.display_name) == owner:
            d = datetime.datetime.now()
            await self.bot.party.me.set_banner(season_level=content)
        else:
            d = datetime.datetime.now()
            await ctx.send(f"{owner} is my owner, not you! :)") 
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !level " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
             