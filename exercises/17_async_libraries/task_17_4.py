# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать сопрограмму (coroutine) configure_router. Сопрограмма подключается
по SSH (с помощью scrapli) к устройству и выполняет перечень команд
в конфигурационном режиме на основании переданных аргументов.

При выполнении каждой команды, скрипт должен проверять результат на ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка, должно генерироваться
исключение ScrapliCommandFailure с информацией о том, какая ошибка возникла,
при выполнении какой команды и на каком устройстве. Шаблон сообщения:
'Команда "{}" выполнилась с ошибкой\n"{}" на устройстве {}'

Параметры функции:

* device - словарь с параметрами подключения к устройству
* config_commands - список команд или одна команда (строка), которые надо выполнить

Функция возвращает строку с результатами выполнения команды (вывод метода send_config(s)).
Функция должна перехватывать все остальные исключения scrapli, кроме ScrapliCommandFailure.

Пример вызова функции:

In [2]: asyncio.run(configure_router(devices[0], 'username user1 password daslfhjaklsdfhalsdh'))
Out[2]: 'username user1 password daslfhjaklsdfhalsdh\n'

In [3]: asyncio.run(configure_router(devices[0], correct_commands))
Out[3]: 'logging buffered 20010\nip http server\n'

Команды с ошибками:

In [4]: asyncio.run(configure_router(devices[0], 'usernme user1 password userpass'))
---------------------------------------------------------------------------
...
ScrapliCommandFailure: Команда "usernme user1 password userpass" выполнилась с ошибкой
"^
% Invalid input detected at '^' marker." на устройстве 192.168.100.1

In [5]: asyncio.run(configure_router(devices[0], commands_with_errors))
---------------------------------------------------------------------------
...
ScrapliCommandFailure: Команда "logging 0255.255.1" выполнилась с ошибкой
"^
% Invalid input detected at '^' marker." на устройстве 192.168.100.1

In [6]: asyncio.run(configure_router(devices[0], commands_with_errors[1:]))
---------------------------------------------------------------------------
...
ScrapliCommandFailure: Команда "logging" выполнилась с ошибкой
"% Incomplete command." на устройстве 192.168.100.1


Запустить сопрограмму и проверить, что она работает корректно с одним из устройств
в файле devices_scrapli.yaml.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

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


if __name__ == '__main__':
    with open('devices_scrapli.yaml') as f:
        devices = yaml.safe_load(f)
        
    loop = asyncio.get_event_loop()
    
    print( loop.run_until_complete( configure_router(devices[0], correct_commands + commands_with_errors))  )
    print( loop.run_until_complete( configure_router(devices[0], correct_commands))  )
    print( loop.run_until_complete( configure_router(devices[0], commands_with_errors[1]))  )
    
    
    
    
    
