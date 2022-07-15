# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать сопрограмму (coroutine) config_device_and_check. Сопрограмма
должна подключаться по SSH с помощью scrapli к одному устройству,
переходить в режим enable, в конфигурационный режим, выполнять указанные команды,
а затем выходить из конфигурационного режима. После  настройки команд, функция
должна проверять, что они настроены корректно. Для проверки используется словарь (пояснение ниже).
Если проверка не прошла, должно генерироваться исключение ValueError с текстом на каком
устройстве не прошла проверка. Если проверка прошла, функция должна возвращать строку
с результатами выполнения команды.

Параметры функции:

* device - словарь с параметрами подключения к устройству
* config_commands - список команд или одна команда (строка), которые надо выполнить
* check - словарь, который указывает как проверить настройку команд config_commands. По умолчанию значение None.

Словарь, который передается в параметр check должен содержать две пары ключ-значение:
* command - команда, которая используется для проверки конфигурации
* search_line - какая строка должна присутствовать в выводе команды command

Запустить сопрограмму и проверить, что она работает корректно одним из устройств
в файле devices_scrapli.yaml и командами в списке commands.
Пример команд и словаря для проверки настройки есть в задании.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""

import asyncio
import yaml
import re
from scrapli import AsyncScrapli
from pprint import pprint


commands = [
    "router ospf 55",
    "auto-cost reference-bandwidth 1000000",
    "network 0.0.0.0 255.255.255.255 area 0",
]

check_ospf = {
    "command": "sh ip ospf",
    "search_line": 'Routing Process "ospf 55" with ID',
}

async def config_device_and_check(device, config_commands, check_command =None):
    result = ""
    
    if type (config_commands)== str:
        config_commands = [config_commands]
        
    async with AsyncScrapli(**device) as ssh:
        reply = await ssh.send_configs(config_commands)
        result = result + reply.result
        
        output = await ssh.send_command(check_command['command'])
       
        
        
        r_search_line = repr(check_command['search_line'])[1:-1]
        
        re_comp= re.compile(r_search_line)        
        
        match_re = re.search(re_comp, output.result)
        
        
        if not match_re:
            raise ValueError("ошибка на :{}".format(device['host']))
    
    return result


async def run(devices, commands, check = None):
    
    
    tasks =  [asyncio.ensure_future(config_device_and_check(device, config_commands =commands, check_command= check)) for device in devices]
    result = await asyncio.gather(*tasks, return_exceptions= True)
    
    print(result)
    return result

if __name__ == "__main__":
    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete( run(devices, commands =commands, check = check_ospf) ) 