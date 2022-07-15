# -*- coding: utf-8 -*-
"""
Задание 17.5

Создать сопрограмму (coroutine) configure_net_devices.

Параметры configure_net_devices:
* devices - список словарей с параметрами подключения к устройствам
* device_commands_map - словарь в котором указано на какое устройство
  отправлять какие команды. Пример словаря - host_commands_dict

Функция возвращает словарь:

* ключ - IP-адрес устройства с которого получен вывод
* значение - вывод, который вернула функция configure_router для этого устройства или
  исключение

Сопрограмма configure_net_devices должна настраивать оборудование в соответствии
со словарем device_commands_map - отправлять команды в значении на то оборудование,
которое указано в ключе словаря. Оборудование должно настраиваться параллельно*.
Для непосредственной настройки оборудования, надо использовать функцию
configure_router из задания 17.4.

Между словарем device_commands_map и списком словарей devices (параметры функции)
может быть несоответствие. Например, в словаре device_commands_map могут быть
устройства для которых не указаны параметры подключения в списке devices. И наоборот.
Функция configure_net_devices должна отправлять команды только на те устройства
для которых есть словарь с параметрами подключения в списке devices и команды
в словаре device_commands_map.

Пример команд и словаря для проверки настройки есть в задании.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""

ospf = [
    "router ospf 55",
    "auto-cost reference-bandwidth 1000000",
    "network 0.0.0.0 255.255.255.255 area 0",
]
logging_with_error = "logging 0255.255.1"
logging_correct = "logging buffered 20010"

host_commands_dict = {
    "10.210.255.3": logging_correct,
    "10.210.255.4": logging_with_error,
    "10.210.255.2": ospf,
}

import asyncio
import yaml
import re
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliCommandFailure

def is_error(output):
    r_string = r"% (?P<errmsg>.+)"
    
    match = re.search (r_string, output)
    
    if match:
        return True
    
    return False

async def configure_router(device, config_commands):
    result = ""
    
    if type (config_commands)== str:
        config_commands = [config_commands]
    try:
        async with AsyncScrapli(**device) as ssh:
            for command in config_commands:
                reply = await ssh.send_config(command)
                if is_error(reply.result):
                    raise ScrapliCommandFailure('Команда "{}" выполнилась с ошибкой\n"{}" на устройстве {}'.format(command, reply.result, device['host']))
                result = result + reply.result
    except ScrapliCommandFailure:
        raise
    except Exception as e:
        print(e)
    
    return result


async def configure_net_devices(devices, device_commands_map):
    tasks =[] 
    ips = []
    ret = dict()
    
    for ip, command in device_commands_map.items():
        for device in devices:
            if device['host'] == ip:
                task = asyncio.ensure_future(configure_router(device, command) )
                ips.append (ip)
                tasks.append(task) 
    
    result = await asyncio.gather(*tasks, return_exceptions= True) 
    
    for ip, res in zip(ips, result):
        ret[ip] = res
    
    return ret

#Функция возвращает словарь:

#* ключ - IP-адрес устройства с которого получен вывод
#* значение - вывод, который вернула функция configure_router для этого устройства или
#  исключение



    #result = await asyncio.gather(*tasks, return_exceptions= True)

if __name__ == "__main__":
    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)
    
    
    loop = asyncio.get_event_loop()
    
    print ( loop.run_until_complete( configure_net_devices (devices, host_commands_dict) ) )
    print ( loop.run_until_complete( configure_net_devices (devices[1:], host_commands_dict) ) )
    
    