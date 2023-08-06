from .settings import BotSettings
from .deviceauths import DeviceAuth, DeviceAuths
from typing import Any
from fortnitepy.ext import commands
import fortnitepy
import FortniteAPIAsync

class AuroraBot(commands.Bot):
    def __init__(self, settings: BotSettings, device_auths: DeviceAuths) -> None:
        self.device_auths = device_auths.get_device_auth()
        self.settings = settings

        self.fortnite_api = FortniteAPIAsync.APIClient()

        super().__init__(
            command_prefix='!',
            auth=fortnitepy.DeviceAuth(
                device_id=self.device_auths.device_id,
                account_id=self.device_auths.account_id,
                secret=self.device_auths.secret
            ),
            status=self.settings.status,
            platform=fortnitepy.Platform(self.settings.platform),
            help_command=None
        )

    async def set_and_update_member_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.me.patch(updated=prop)

    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)

    async def event_device_auth_generate(self, details: dict, email: str) -> None:
        device_auth = DeviceAuth(
            email=email,
            **details
        )

        await self.device_auths.save_device_auth(device_auth)

