# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать сопрограмму (coroutine) send_config_commands. Сопрограмма
должна подключаться по SSH с помощью asyncssh к одному устройству,
переходить в режим enable, в конфигурационный режим, выполнять указанные команды,
а затем выходить из конфигурационного режима.

Параметры функции:

* host - IP-адрес устройства
* username - имя пользователя
* password - пароль
* enable_password - пароль на режим enable
* config_commands - список команд или одна команда (строка), которые надо выполнить

Функция возвращает строку с результатами выполнения команды:

In [1]: import asyncio

In [2]: from task_17_1 import send_config_commands

In [3]: commands = ['interface loopback55', 'ip address 10.5.5.5 255.255.255.255']

In [4]: print(asyncio.run(send_config_commands('192.168.100.1', 'cisco', 'cisco', 'cisco', commands)))
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface loopback55
R1(config-if)#ip address 10.5.5.5 255.255.255.255
R1(config-if)#end
R1#

In [5]: asyncio.run(send_config_commands(**r1, config_commands=commands))
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loopback55\r\nR1(config-if)#ip address 10.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'


Запустить сопрограмму и проверить, что она работает корректно.
При необходимости можно создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import asyncio
import asyncssh

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
    
    

r1 = {
    "host": "10.210.255.2",
    "username": "cisco",
    "password": "cisco",
    "enable_password": "cisco",
}


if __name__ == "__main__":
    commands= ['interface loopback55', 'ip address 10.5.5.5 255.255.255.255']
    
    loop = asyncio.get_event_loop()
    print ( loop.run_until_complete(send_config_commands(**r1,  config_commands =commands  )))