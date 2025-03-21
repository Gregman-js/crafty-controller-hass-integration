import aiohttp


class CraftyControllerAPI:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = aiohttp.ClientSession(
            headers={"Authorization": self.auth_token},
            connector=aiohttp.TCPConnector(ssl=False)
        )

    async def get_servers(self):
        async with self.session.get(f"{self.base_url}/api/v2/servers") as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["data"] if data["status"] == "ok" else []

    async def get_server_stats(self, server_id):
        async with self.session.get(f"{self.base_url}/api/v2/servers/{server_id}/stats") as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["data"] if data["status"] == "ok" else {}

    async def send_server_action(self, server_id, action):
        async with self.session.post(
                f"{self.base_url}/api/v2/servers/{server_id}/action/{action}"
        ) as resp:
            resp.raise_for_status()

    async def close(self):
        await self.session.close()