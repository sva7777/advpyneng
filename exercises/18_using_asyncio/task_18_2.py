# -*- coding: utf-8 -*-
'''
Задание 18.2

Создать сопрограмму (coroutine) ping_ip_addresses, которая проверяет
пингуются ли IP-адреса в списке.
Проверка IP-адресов должна выполняться параллельно (concurrent).

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:

* список доступных IP-адресов
* список недоступных IP-адресов


Для проверки доступности IP-адреса, используйте утилиту ping встроенную в ОС.

Запустить сопрограмму и проверить, что она работает корректно.
При необходимости можно создавать дополнительные функции.

Для заданий в этом разделе нет тестов!

'''
import asyncio
from pprint import pprint

async def internal_ping(ip):
    proc = await asyncio.create_subprocess_shell("ping -c 3 -n {}".format(ip),
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE,
                                                    encoding='utf-8')
    

    
    stdout, stderr= await proc.communicate()
    
    if proc.returncode == 0:
        return True
    else:
        return False



async def ping_ip_addresses(ip_v4_addresses):
   
    tasks = [asyncio.ensure_future(internal_ping(ip)) for ip in ip_v4_addresses]
    
    result = await asyncio.gather(*tasks)
    return result


ip_addresses = ["10.210.255.1", "10.210.255.2", "10.210.255.3", "10.210.255.4", "10.210.255.5", "10.210.255.6" ]

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    pprint(  loop.run_until_complete(ping_ip_addresses(ip_addresses)))