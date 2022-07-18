# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать сопрограмму (coroutine) get_info_network_devices, которая
собирает вывод одной и той же команды со всех устройств в списке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - show команда, которую надо отправить на все устройства

Функция возвращает список с выводом команды с каждого устройства.

In [3]: asyncio.run(get_info_network_devices(devices, command="sh clock"))
Out[3]: ['*14:08:27.584 UTC Wed Sep 12 2021', '*14:08:27.752 UTC Wed Sep 12 2021',
'*14:08:27.755 UTC Wed Sep 12 2021', '*14:08:28.681 UTC Wed Sep 12 2021',
'*14:08:28.879 UTC Wed Sep 12 2021']

Список devices это список словарей в котором могут быть параметры для подключения
к оборудованию с помощюь scrapli и с помощью netmiko (пример в файле devices.yaml).
Функция get_info_network_devices должна распознать как подключаться к устройству -
с помощью scrapli или netmiko по параметру platform/device_type, соответственно.

Функция get_info_network_devices должна подключаться к оборудованию параллельно*
для scrapli - asyncio, а для netmiko - потоки. В идеале подключение в потоках
должно быть сделано так, чтобы оно не блокировало основной поток и другие асинхронные
задачи.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import asyncio
import yaml
import logging  
import re
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliCommandFailure

import netmiko
from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)


#функция get_info_network_devices должна распознать как подключаться к устройству -
#с помощью scrapli или netmiko по параметру platform/device_type, соответственно.

#Функция get_info_network_devices должна подключаться к оборудованию параллельно*
#для scrapli - asyncio, а для netmiko - потоки. В идеале подключение в потоках
#должно быть сделано так, чтобы оно не блокировало основной поток и другие асинхронные
#задачи.

# должна быть coroutine
def netmiko_task(device, command):
    try:
        logger.debug("netmiko device {} ".format(device['host']))
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
        return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        return None


def netmiko_thread(devices, command):
    
    future_list = list()
    result = list()

    with ThreadPoolExecutor(max_workers =2) as executor:
        for device in devices:
            future = executor.submit(netmiko_task, device, command)
            future_list.append(future)
    
    for res in future_list:
        result.append (res.result())
    
    return result 
    

def is_error(output):
    r_string = r"% (?P<errmsg>.+)"
    
    match = re.search (r_string, output)
    
    if match:
        return True
    
    return False
    
async def scrapli_task(device, command):
    result = ""
    if type (command)== str:
        command = [command]

    try:
        logger.debug("scrapli device {} ".format(device['host']))
        async with AsyncScrapli(**device) as ssh:
            for command in command:
                reply = await ssh.send_command(command)
                if is_error(reply.result):
                    raise ScrapliCommandFailure('Команда "{}" выполнилась с ошибкой\n"{}" на устройстве {}'.format(command, reply.result, device['host']))

                result = result + reply.result
    except ScrapliCommandFailure:
        raise
    except Exception as e:
        print(e)
    return result


async def scrapli_main(devices, command):
    tasks =[] 
    
    for device in devices:
        task = asyncio.ensure_future(scrapli_task(device, command) )
        tasks.append(task)
        
    result = await asyncio.gather(*tasks, return_exceptions= True) 
    return result

def scrapli_thread(devices, command):
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete( scrapli_main(devices, command ) ) 
    return result


def get_info_network_devices(devices, command):
    scrapli_list = list()
    netmiko_list = list()
    
    device_to_privider = list()
    
    for device in devices:
        if "platform" in device and device["platform"] == "cisco_iosxe":
            device_to_privider.append("scrapli")
            scrapli_list.append(device)
        elif "device_type" in device and device["device_type"] == "cisco_ios":
            device_to_privider.append("netmiko")
            netmiko_list.append(device)
        else:
            raise ValueError("can not determine transport for device {}".format(device["host"]) )
    
    
    
    with ProcessPoolExecutor(max_workers =2) as executor:
        future_netmiko = executor.submit(netmiko_thread, netmiko_list,command)
        future_asyncio = executor.submit(scrapli_thread, scrapli_list, command)
        
    
    res_netmiko = future_netmiko.result()
    res_asyncio = future_asyncio.result()
    
    iter_netmiko = iter(res_netmiko)
    iter_asyncio = iter(res_asyncio)
    
    result = list()
    
    for dev in device_to_privider:
        if dev == "scrapli":
            result.append(next(iter_asyncio))
        elif dev == "netmiko":
            result.append(next(iter_netmiko))
        else:
            raise ValueError("Unknown device type")
    
    return result

if __name__ == "__main__":
    
    logger = logging.getLogger("task18_1")
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s", "%H:%M:%S")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    result = get_info_network_devices(devices, command="sh clock")
    pprint(result)
  