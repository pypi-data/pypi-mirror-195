from .errors import MissingDeviceAuth
from typing import Optional, Union
import json
import aiofiles


class DeviceAuth:
    def __init__(self,
                 device_id: Optional[str] = None,
                 account_id: Optional[str] = None,
                 secret: Optional[str] = None,
                 **kwargs
                 ) -> None:
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret


class DeviceAuths:
    def __init__(self, filename: str) -> None:
        self.device_auth = None
        self.filename = filename

    async def load_device_auths(self) -> None:
        try:
            async with aiofiles.open(self.filename, mode='r') as fp:
                data = await fp.read()
                raw_device_auths = json.loads(data)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            raw_device_auths = {}

        if 'device_id' not in raw_device_auths or \
            'account_id' not in raw_device_auths or \
                'secret' not in raw_device_auths:
            raise MissingDeviceAuth('Missing required device auth key.')

        self.device_auth = DeviceAuth(
            device_id=raw_device_auths.get('device_id'),
            account_id=raw_device_auths.get('account_id'),
            secret=raw_device_auths.get('secret')
        )

    async def save_device_auths(self) -> None:
        async with aiofiles.open(self.filename, mode='w') as fp:
            await fp.write(json.dumps(
                {
                    "account_id": self.device_auth.account_id,
                    "device_id": self.device_auth.device_id,
                    "secret": self.device_auth.secret
                },
                sort_keys=False,
                indent=4
            ))

    def set_device_auth(self, **kwargs) -> None:
        self.device_auth = DeviceAuth(
            **kwargs
        )

    def get_device_auth(self) -> Union[DeviceAuth, None]:
        return self.device_auth