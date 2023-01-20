import asyncio
import json
import os

import aiohttp


async def send_request(session, url):
    async with session.get(url, ssl=False) as resp:
        js = await resp.text()
        data = json.loads(js)
        return data


async def api_1(session):
    print('api_1 -- start')
    res = await send_request(session, f'https://api.weatherbit.io/v2.0/current?lat=50.45&lon=30.52&key={os.getenv("OPEN_API_KEY")}')
    temperature = res['data'][0]['temp']
    print('api_1 -- end')
    return temperature


async def api_2(session):
    print('api_2 -- start')
    res = await send_request(session, 'https://api.open-meteo.com/v1/forecast?latitude=50.45&longitude=30.52&current_weather=True')
    temperature = res['current_weather']['temperature']
    print('api_2 -- end')
    return temperature


async def api_3(session):
    print('api_3 -- start')
    res = await send_request(session, f'http://api.weatherstack.com/current?access_key={os.getenv("ACCESS_KEY")}&query=Kiev')
    temperature = res['current']['temperature']
    print('api_3 -- end')
    return temperature


async def main():
    async with aiohttp.ClientSession(trust_env=True) as session:
        result = await asyncio.gather(api_1(session), api_2(session), api_3(session))

    temperature = round(sum(result)/len(result), 2)
    print(f'Temperature in Kyiv is {temperature} by Celsius')


if __name__ == '__main__':
    asyncio.run(main())
