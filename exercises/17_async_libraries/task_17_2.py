# -*- coding: utf-8 -*-
"""
Задание 17.2

Создать сопрограмму (coroutine) configure_devices. Сопрограмма
должна настраивать одни и те же команды на указанных устройствах с помощью asyncssh.
Все устройства должны настраиваться параллельно.

Параметры функции:

* devices - список словарей с параметрами подключения к устройствам
* config_commands - команды конфигурационного режима, которые нужно отправить на каждое устройство

Функция возвращает список строк с результатами выполнения команды на каждом устройстве.
Запустить сопрограмму и проверить, что она работает корректно с устройствами
в файле devices.yaml и командами в списке commands.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""

import asyncio
import asyncssh
import yaml

async def send_config_commands(host, username, password, enable_password, config_commands):
    
    result = ""
    
    if type(config_commands) == str:
        config_commands= [config_commands]
    

    ssh = await asyncssh.connect(
        host=host,
        username=username,
        password=password,
        encryption_algs="+aes128-cbc,aes256-cbc"
    )
    
    writer, reader, stderr = await ssh.open_session(
        term_type="Dumb", term_size=(200, 24)
    )
    
    await asyncio.wait_for(reader.readuntil(">"), timeout=3)
    writer.write("enable\n")
    await asyncio.wait_for(reader.readuntil("Password"), timeout=3)
    writer.write(f"{enable_password}\n")
    await asyncio.wait_for(reader.readuntil([">", "#"]), timeout=3)
    writer.write("terminal length 0\n")
    await asyncio.wait_for(reader.readuntil("#"), timeout=3)
    
    writer.write("conf t\n")
    result = result + await asyncio.wait_for(reader.readuntil("#"), timeout=3)
    
    for command in commands:
        writer.write(command+"\n")
        result = result + await asyncio.wait_for(reader.readuntil("#"), timeout=3)

    return result


commands = [
    "router ospf 55",
    "auto-cost reference-bandwidth 1000000",
    "network 0.0.0.0 255.255.255.255 area 0",
]

async def run(devices, commands):
    
    tasks =  [asyncio.ensure_future(send_config_commands(**device, config_commands =commands)) for device in devices]
    result = await asyncio.gather(*tasks)
    return result

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    loop = asyncio.get_event_loop()
    
    print ( loop.run_until_complete( run(devices, commands =commands) ) )
    
    
    
    
    
    