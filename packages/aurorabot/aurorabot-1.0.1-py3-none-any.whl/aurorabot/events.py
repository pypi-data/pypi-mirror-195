from .settings import BotSettings
import datetime
from fortnitepy.ext import commands
import fortnitepy
import FortniteAPIAsync
import os
from pathlib import Path

from aurorabot.settings import BotSettings


class events(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: BotSettings) -> None:
        self.bot = bot
        self.settings = settings
        self.fortnite_api = FortniteAPIAsync.APIClient()



    @commands.Cog.event()
    async def event_ready(self):
        print('\033[1;37;49m Client is ready as: ' + f'\033[1;34;49m {self.bot.party.me}'.format(self))
        await self.bot.party.me.set_outfit(asset=self.settings.cid)
        await self.bot.party.me.set_pickaxe(asset=self.settings.pickaxe_id)
        await self.bot.party.me.set_backpack(asset=self.settings.bid)
        await self.bot.party.me.set_banner(icon = self.settings.banner, color=self.settings.banner_colour, season_level=self.settings.level)
        if self.settings.invite_on_start:
            try:
                for friend in self.bot.friends:
                    await self.bot.party.invite(friend.id)

            except fortnitepy.Forbidden:
                pass
            except fortnitepy.PartyError:
                pass
            except fortnitepy.HTTPException:
                pass
        else:
            pass

        my_file = Path("./friendlist.txt")
        if my_file.exists():
            os.remove(my_file)
            with open(my_file, 'w', encoding="utf8") as file:
                for friend in self.bot.friends:
                     file.write(f"{friend.display_name} + ({friend.id})\n")
        else:
            with open(my_file, 'w', encoding="utf8") as file:
                for friend in self.bot.friends:
                     file.write(f"{friend.display_name} + ({friend.id})\n")



    @commands.Cog.event()
    async def event_friend_request(self, IncommingPendingFriend):
        hours = self.settings.hours
        if self.settings.friend_accept:
            await IncommingPendingFriend.accept()
            d = datetime.datetime.now()
            print("\033[1;37;49m User: " + f"\033[1;34;49m {IncommingPendingFriend.display_name} " + "\033[1;37;49m Action:" + "\033[1;32;49m friend request (accept) " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))          
        else:
            await IncommingPendingFriend.decline()
            d = datetime.datetime.now()
            print("\033[1;37;49m User: " + f"\033[1;34;49m {IncommingPendingFriend.display_name} " + "\033[1;37;49m Action:" + "\033[1;32;49m friend request (declined) " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    @commands.Cog.event()
    async def event_party_invite(self, ReceivedPartyInvitation):
        owner = self.settings.owner
        if (ReceivedPartyInvitation.sender.display_name) == owner:
            await ReceivedPartyInvitation.accept()
            await self.bot.party.me.set_outfit(asset=self.settings.cid)
            await self.bot.party.me.set_pickaxe(asset=self.settings.pickaxe_id)
            await self.bot.party.me.set_backpack(asset=self.settings.bid)
            await self.bot.party.me.set_emote(asset='EID_Wave')
            await self.bot.party.me.set_banner(icon = self.settings.banner, color=self.settings.banner_colour, season_level=self.settings.level)
            await self.bot.party.send("Hello " + owner + "! Thanks for the invite. :)")
        else:
            pass


    @commands.Cog.event()
    async def event_party_member_join(self, member):
        try:
            if (member.display_name) == f"{self.bot.party.me}".format(self):
                return
            else:
                member.add()
        except fortnitepy.DuplicateFriendship:
            return
        except fortnitepy.Forbidden:
            return


        
    @commands.Cog.event()
    async def event_party_member_join(self, member):
        if (member.display_name) == f"{self.bot.party.me}".format(self):
            return
        else:
            d = datetime.datetime.now()
            hours = self.settings.hours
            print("\033[1;37;49m User: " + f"\033[1;34;49m {member.display_name} ({member.id}) " + "\033[1;37;49m Action:" + "\033[1;32;49m joined " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            await self.bot.party.send("Hey " + member.display_name + "! If you need help... please join our discord server: https://dsc.gg/zockerwolf or use my !help command")


    
    @commands.Cog.event()
    async def event_party_member_leave(self, member):
        hours = self.settings.hours
        if (member.display_name) == f"{self.bot.party.me}".format(self):
            return
        else:
            d = datetime.datetime.now()
            print("\033[1;37;49m User: " + f"\033[1;34;49m {member.display_name} ({member.id}) " + "\033[1;37;49m Action:" + "\033[1;31;49m leaved " + "\033[1;37;49m Bot:" + f"\033[1;34;49m {self.bot.party.me}".format(self)  +  "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))



    # @commands.Cog.event()
    # async def event_party_member_outfit_change(self, member , before , after):
    #     if member == self.bot.party.me:
    #         skin = await self.fortnite_api.cosmetics.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", asset = after, backendType="AthenaCharacter")
    #         print(skin)
    #         print(after)
    #         print(before)