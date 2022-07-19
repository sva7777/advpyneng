# -*- coding: utf-8 -*-

'''
Задание 18.4

Создать класс CiscoSSH, который наследует класс BaseSSH из файла base_ssh_class.py.

Переписать метод connect в классе CiscoSSH:

1. После подключения по SSH должен выполняться переход в режим enable.
   Для этого также необходимо добавить параметр secret к методу __init__.
2. После перехода в режим enable, отключить paging (команда terminal length 0)

Добавить методы:

* send_show_command - принимает как аргумент команду show и возвращает
  вывод полученный с обрудования
* send_config_commands - должен уметь отправлять одну команду конфигурационного
  режима или список команд. Метод дожен возвращать вывод аналогичный методу
  send_config_set у netmiko.

Проверить работу класса.
Ограничение: нельзя менять класс BaseSSH.

Для заданий в этом разделе нет тестов!
'''


import base_ssh_class
import yaml
import asyncio
from pprint import pprint


class CiscoSSH (base_ssh_class.BaseSSH):
    
    def __init__(self, host, username, password, secret, timeout=3):
        super().__init__(host, username, password, timeout)
        self.secret = secret
    async def connect(self):
        await super().connect()

        self._writer.write("enable\n")
        await asyncio.wait_for(self._reader.readuntil("Password"), self.timeout)
        self._writer.write(f"{self.secret}\n")
        await asyncio.wait_for(self._reader.readuntil([">", "#"]), self.timeout)
        self._writer.write("terminal length 0\n")
        await asyncio.wait_for(self._reader.readuntil("#"), self.timeout)

        return self
    
    async def send_show_command(self, command):
        result = ""

        self._writer.write(command+"\n")
        result = result + await asyncio.wait_for(self._reader.readuntil("#"), self.timeout)
        
        return result
    
    async def send_config_commands(self, commands):
        result = ""
        if type(commands)== str:
            commands = commands[commands]

        self._writer.write("conf t\n")
        result = result + await asyncio.wait_for(self._reader.readuntil("#"), self.timeout)

        for command in commands:
            self._writer.write(command+"\n")
            result = result + await asyncio.wait_for(self._reader.readuntil("#"), self.timeout)
        
        self._writer.write("exit\n")
        result = result + await asyncio.wait_for(self._reader.readuntil("#"), self.timeout)
        
        return result
        
    async def send_config_set(self, commands):
        return await self.send_config_commands(commands)


async def show_command_task(device, command):
    device.pop("device_type", None)
    
    async with CiscoSSH(**device) as cisco:
        result = await cisco.send_show_command(command)
    return result
    

async def config_commands_task(device, commands):
    device.pop("device_type", None)
    
    async with CiscoSSH(**device) as cisco:
        result = await cisco.send_config_commands(commands)
    return result

async def config_set_task(device, commands):
    device.pop("device_type", None)
    
    async with CiscoSSH(**device) as cisco:
        result = await cisco.send_config_set(commands)
    return result


async def show_command_main(devices, command):
    tasks = [asyncio.ensure_future(show_command_task(dev, command) ) for dev in devices]
    result = await asyncio.gather(*tasks)
    return result
    
async def config_commands_main(devices, commands):
    tasks = [asyncio.ensure_future(config_commands_task(dev, commands) ) for dev in devices]
    result = await asyncio.gather(*tasks)
    return result

async def config_set_main(devices, commands):
    tasks = [asyncio.ensure_future(config_set_task(dev, commands) ) for dev in devices]
    result = await asyncio.gather(*tasks)
    return result

if __name__ == "__main__":

    with open("devices.yaml") as f:
        devices_all = yaml.safe_load(f)

    devices =[]
    
    for dev in devices_all:
        if "device_type" in dev and dev["device_type"] == "cisco_ios":
            devices.append(dev)

    loop = asyncio.get_event_loop()
    
    pprint(loop.run_until_complete(show_command_main(devices,"sh clock"))) 
    
    commands = ['interface loopback55', 'ip address 10.5.5.5 255.255.255.255']
    
    pprint(loop.run_until_complete(config_commands_main(devices,commands))) 
    
    pprint(loop.run_until_complete(config_set_main(devices,commands))) 
    
    