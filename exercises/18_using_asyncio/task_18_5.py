# -*- coding: utf-8 -*-
'''
Задание 18.5

Создать асинхронный аналог enumerate. Для это надо создать сопрограмму (coroutine)
aenumerate. Сопрограмма aenumerate должна быть генератором и работать с
асинхронными итераторами (и генераторами).

Проверить работу aenumerate заменив ручное увеличение индекса index на aenumerate.

В итоге функция должна работать в таком виде:

async def open_csv(filename):
    async with aiofiles.open(filename) as f:
        headers = await f.readline()
        headers = list(csv.reader([headers]))[0]
        async for index, line in aenumerate(f):
            print(index)
            yield dict(list(csv.DictReader([line], fieldnames=headers))[0])

'''

import csv
import asyncio
import aiofiles
from pprint import pprint

class aenumerate:
    def __init__(self, file_handler):
        self.__index =0 
        self.__file_handler = file_handler
    
    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        index = self.__index
        line = await self.__file_handler.readline()
        
        if len(line) == 0:
            raise StopAsyncIteration
            
        self.__index += 1
        return (index, line)
        

async def open_csv(filename):
    async with aiofiles.open(filename) as f:
        headers = await f.readline()
        headers = list(csv.reader([headers]))[0]
        async for index, line in aenumerate(f):
            print(index)
            yield dict(list(csv.DictReader([line], fieldnames=headers))[0])



#async def open_csv(filename):
#    async with aiofiles.open(filename) as f:
#        headers = await f.readline()
#        headers = list(csv.reader([headers]))[0]
#        index = 0
#        async for line in f:
#            print(index)
#            yield dict(list(csv.DictReader([line], fieldnames=headers))[0])
#            index += 1


async def filter_prefix_next_hop(async_iterable, nexthop):
    async for line in async_iterable:
        if line['nexthop'] == nexthop:
            yield line


async def main(filename):
    data = open_csv(filename)
    nhop_45 = filter_prefix_next_hop(data, "200.219.145.45")
    async for line in nhop_45:
        print(line)


if __name__ == "__main__":
    filename = 'rib.table.lg.ba.ptt.br-BGP.csv'
    
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(main(filename))