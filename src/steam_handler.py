import aiohttp
import asyncio
from SteamGameRecommender.src.conf import API_KEY
import time


class SteamHandler:
    def __init__(self):
        self.base_url = 'https://api.steampowered.com'

    async def get_owned_games(self, steam_id, include_appinfo=True, include_played_free_games=True, format='json'):
        endpoint = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            'key': API_KEY,
            'steamid': steam_id,
            'include_appinfo': str(include_appinfo).lower(),
            'include_played_free_games': str(include_played_free_games).lower(),
            'format': format
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def get_recently_played_games(self, steam_id, count=None, format='json'):
        endpoint = f"{self.base_url}/IPlayerService/GetRecentlyPlayedGames/v0001/"
        params = {
            'key': API_KEY,
            'steamid': steam_id,
            'format': format
        }
        if count is not None:
            params['count'] = count
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                try:
                    return data['response']['games']
                except KeyError:
                    return None

    async def get_app_info(self, app_id, format='json'):
        endpoint = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                response.raise_for_status()
                return await response.json()

    async def get_steam_id64(self, url):
        username = url.strip('/').split('/')[-1]
        endpoint = f"{self.base_url}/ISteamUser/ResolveVanityURL/v0001/"
        params = {
            'key': API_KEY,
            'vanityurl': username
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:
                try:
                    response.raise_for_status()
                    data = await response.json()
                    if data['response']['success'] == 1:
                        return data['response']['steamid']
                    else:
                        raise Exception('Steam ID resolution failed')
                except aiohttp.ClientResponseError as e:
                    raise Exception(f"Error fetching data: {e}") from None
                except KeyError:
                    raise Exception('Invalid JSON response from Steam API') from None
                except Exception as e:
                    raise Exception(f"Error: {e}") from None


async def test_speed():
    steam_ids = ['76561198168015547']
    steam_handler = SteamHandler()
    tasks = []
    for steam_id in steam_ids:
        tasks.append(steam_handler.get_recently_played_games(steam_id))
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    print(f'Took {end_time - start_time} seconds to get {len(results)} results')


async def test_request():
    steam_ids = ['76561198168015547']
    steam_handler = SteamHandler()
    tasks = []
    for steam_id in steam_ids:
        tasks.append(steam_handler.get_recently_played_games(steam_id))
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


async def test_app_info():
    app_ids = ['570']
    steam_handler = SteamHandler()
    tasks = []
    for app_id in app_ids:
        tasks.append(steam_handler.get_app_info(app_id))
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    print(f'Took {end_time - start_time} seconds to get {len(results)} results')
    # for result in results:
    #    print(result)     

# asyncio.run(test_speed())
# asyncio.run(test_app_info())
# asyncio.run(test_request())
