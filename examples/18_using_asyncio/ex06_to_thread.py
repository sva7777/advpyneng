import asyncio
import time


def netmiko_connect(device):
    print(f"sync Подключаюсь к {device}")
    time.sleep(5)
    print(f"sync Получили результат {device}")


async def scrapli_connect(device):
    print(f"async Подключаюсь к {device}")
    await asyncio.sleep(1)
    print(f"async Получили результат {device}")


async def main():
    devices = list(range(10))
    coroutines = []
    for dev in devices:
        if dev % 2:
            coro = asyncio.to_thread(netmiko_connect, dev)
        else:
            coro = scrapli_connect(dev)
        coroutines.append(coro)
    await asyncio.sleep(5)
    print("coroutines")
    results = await asyncio.gather(*coroutines)
    return results


if __name__ == "__main__":
    asyncio.run(main())
