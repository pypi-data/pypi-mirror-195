from typing import Tuple
from fortnitepy.ext import commands
import fortnitepy
import aiohttp
import FortniteAPIAsync
import datetime
from .settings import BotSettings


class CosmeticCommandShortcuts(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: BotSettings) -> None:
        self.bot = bot
        self.fortnite_api = FortniteAPIAsync.APIClient()
        self.settings = settings


    async def set_vtid(self, variant_token: str) -> Tuple[str, str, int]:
        async with aiohttp.ClientSession() as session:
            request = await session.request(method='GET', url='https://benbot.app/api/v1/assetProperties', params={'path': 'FortniteGame/Content/Athena/' f'Items/CosmeticVariantTokens/{variant_token}.uasset'})
            response = await request.json()
            file_location = response['export_properties'][0]
            skin_cid = file_location['cosmetic_item']
            variant_channel_tag = file_location['VariantChanelTag']['TagName']
            variant_name_tag = file_location['VariantNameTag']['TagName']
            variant_type = variant_channel_tag.split('Cosmetics.Variant.Channel.')[1].split('.')[0]
            variant_int = int("".join(filter(lambda x: x.isnumeric(), variant_name_tag)))
            return skin_cid, variant_type if variant_type != 'ClothingColor' else 'clothing_color', variant_int



    @commands.command()
    async def renegade(self,  ctx: fortnitepy.ext.commands.Context) -> None:
        hours = self.settings.hours
        r = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name="Renegade Raider", backendType="AthenaCharacter")
        await self.bot.party.me.set_outfit(asset=r.id)
        await ctx.send("Set skin to " + r.name + "!")
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {r.name} ({r.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    
    @commands.command()
    async def purpleskull(self,  ctx: fortnitepy.ext.commands.Context) -> None:
        hours = self.settings.hours
        ps = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name="Skull Trooper", backendType="AthenaCharacter")
        purple = self.bot.party.me.create_variants(clothing_color=1)
        await self.bot.party.me.set_outfit(asset=ps.id, variants=purple)
        await ctx.send("Set skin to Purple " + ps.name + "!")
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {ps.name} (purple) ({ps.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.command()
    async def pinkghoul(self,  ctx: fortnitepy.ext.commands.Context) -> None:
        hours = self.settings.hours
        pg = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name="Ghoul Trooper", backendType="AthenaCharacter")
        pink = self.bot.party.me.create_variants(material=3)
        await self.bot.party.me.set_outfit(asset=pg.id, variants=pink)
        await ctx.send("Set skin to Pink " + pg.name + "!")
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {pg.name} (pink) ({pg.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    
    @commands.command()
    async def hologram(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        await self.bot.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await ctx.send('Skin set to Star Wars Hologram!')
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m Star Wars Hologram (CID_VIP_Athena_Commando_M_GalileoGondola_SG) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.command()
    async def checkeredrenegade(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        cr = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", asset='CID_028_Athena_Commando_F', name = "Renegade Raider")
        c = self.bot.party.me.create_variants(material=2)
        await self.bot.party.me.set_outfit(asset=cr.id, variants = c)
        await ctx.send("Skin set to Checkered " + cr.name + "!")
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {cr.name} (checkered) ({cr.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.command()
    async def tbd(self,  ctx: fortnitepy.ext.commands.Context):
        hours = self.settings.hours
        await self.bot.party.me.set_outfit(asset="CID_NPC_Athena_Commando_M_Fallback")
        await ctx.send("Skin set to TBD!")
        d = datetime.datetime.now()
        print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m TBD (CID_NPC_Athena_Commando_M_Scrapyard) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))