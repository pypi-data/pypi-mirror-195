import json
import aiofiles


class BotSettings:
    def __init__(self,
                 email: str = "",
                 password: str = "",
                 cid: str = "",
                 bid: str = "",
                 eid: str = "",
                 pickaxe_id: str = "",
                 banner: str = "",
                 banner_colour: str = "",
                 level: int = 0,
                 bp_tier: int = 0,
                 status: str = "",
                 platform: str = "",
                 debug: bool = False,
                 friend_accept: bool = True,
                 owner: str = "",
                 hours: int = 0,
                 invite_on_start: bool = True
                 ) -> None:
        self.email = email
        self.password = password
        self.cid = cid
        self.bid = bid
        self.eid = eid
        self.pickaxe_id = pickaxe_id
        self.banner = banner
        self.banner_colour = banner_colour
        self.level = level
        self.bp_tier = bp_tier
        self.status = status
        self.platform = platform
        self.debug = debug
        self.friend_accept = friend_accept
        self.owner = owner
        self.hours = hours
        self.invite_on_start = invite_on_start

    async def load_settings_from_file(self, filename: str) -> None:
        async with aiofiles.open(filename, mode='r+') as f:
            raw = await f.read()

        data = json.loads(raw)

        self.email = data.get('email', self.email)
        self.password = data.get('password', self.password)
        self.cid = data.get('cid', self.cid)
        self.bid = data.get('bid', self.bid)
        self.eid = data.get('eid', self.eid)
        self.pickaxe_id = data.get('pickaxe_id', self.pickaxe_id)
        self.banner = data.get('banner', self.banner)
        self.banner_colour = data.get('banner_colour', self.banner_colour)
        self.level = data.get('level', self.level)
        self.bp_tier = data.get('bp_tier', self.bp_tier)
        self.status = data.get('status', self.status)
        self.platform = data.get('platform', self.platform)
        self.debug = data.get('debug', self.debug)
        self.friend_accept = data.get('friend_accept', self.friend_accept)
        self.owner = data.get('owner', self.owner)
        self.hours = data.get('hours', self.hours)
        self.invite_on_start = data.get('invite_on_start', self.invite_on_start)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "cid": self.cid,
            "bid": self.bid,
            "eid": self.eid,
            "pickaxe_id": self.pickaxe_id,
            "banner": self.banner,
            "banner_colour": self.banner_colour,
            "level": self.level,
            "bp_tier": self.bp_tier,
            "status": self.status,
            "platform": self.platform,
            "debug": self.debug,
            "friend_accept": self.friend_accept,
            "owner": self.owner,
            "hours": self.hours,
            "invite_on_start": self.invite_on_start
        }
