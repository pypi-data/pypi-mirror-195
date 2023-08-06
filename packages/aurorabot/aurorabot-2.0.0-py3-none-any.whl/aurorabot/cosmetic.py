from typing import Tuple

from fortnitepy.ext import commands
import fortnitepy
import aiohttp
import FortniteAPIAsync
import datetime
from .settings import BotSettings


class CosmeticCommands(commands.Cog):
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
    async def skin(self,  ctx: fortnitepy.ext.commands.Context, content: str) -> None:
        hours = self.settings.hours
        try:
            skin = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaCharacter")
            await self.bot.party.me.set_outfit(asset=skin.id)
            await ctx.send("Set skin to " + skin.name + "!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {skin.name} ({skin.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a skin with the name: {content}.")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {self}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    @commands.command()
    async def emote(self,  ctx: fortnitepy.ext.commands.Context, content: str) -> None:
        hours = self.settings.hours
        try:
            emote = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaDance")
            await self.bot.party.me.set_emote(asset=emote.id)
            await ctx.send("Set emote to " + emote.name + "!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;36;49m Emote " + "\033[1;37;49m Name: " + f"\033[1;32;49m {emote.name} ({emote.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a emote with the name: {content}.")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;36;49m Emote " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    
    @commands.command()
    async def backpack(self,  ctx: fortnitepy.ext.commands.Context, content: str) -> None:
        hours = self.settings.hours
        try:
            bp = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaBackpack")
            await self.bot.party.me.set_backpack(asset=bp.id)
            await ctx.send("Set backpack to " + bp.name + "!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;30;49m Backpack " + "\033[1;37;49m Name: " + f"\033[1;32;49m {bp.name} ({bp.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a emote with the name: {content}.")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;30;49m Backpack " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


    @commands.command()
    async def pickaxe(self,  ctx: fortnitepy.ext.commands.Context, content: str) -> None:
        hours = self.settings.hours
        try:
            pa = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaPickaxe")
            await self.bot.party.me.set_pickaxe(asset=pa.id)
            await ctx.send("Set pickaxe to " + pa.name + "!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;37;49m Pickaxe " + "\033[1;37;49m Name: " + f"\033[1;32;49m {pa.name} ({pa.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a emote with the name: {content}.")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;37;49m Pickaxe " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    
    @commands.command()
    async def emoji(self,  ctx: fortnitepy.ext.commands.Context, content: str) -> None:
        hours = self.settings.hours
        try:
            emoji = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaEmoji")
            await self.bot.party.me.set_emoji(asset=emoji.id)
            await ctx.send("Set emoticon to " + emoji.name + "!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;33;49m Emoji " + "\033[1;37;49m Name: " + f"\033[1;32;49m {emoji.name} ({emoji.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a emoji with the name: {content}.")
            d = datetime.datetime.now()
            print("\033[1;37;49m Type: " + "\033[1;33;49m Emoji " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {ctx.author} " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))