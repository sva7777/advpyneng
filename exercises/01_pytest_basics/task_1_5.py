# -*- coding: utf-8 -*-
"""
Задание 1.5

Написать тест(ы), который проверяет есть ли маршрут 192.168.100.0/24 в таблице
маршрутизации (команда sh ip route) на маршрутизаторах, которые указаны в файле devices_reachable.yaml.

Для проверки надо подключиться к каждому маршрутизатору с помощью scrapli
и проверить маршрут командой sh ip route или разновидностью команды sh ip route.

Тест(ы) должен проходить, если маршрут есть.
Тест может быть один или несколько.

Тест(ы) написать в файле задания.

Для заданий этого раздела нет тестов для проверки тестов :)
"""

import yaml
import socket  
import pytest
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from paramiko.ssh_exception import SSHException
from pprint import pprint

class VasilyException(Exception):
    pass

def send_show(device, show_commands):
    transport = device.get("transport") or "system"
    host = device.get("host")
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    print(f">>> Connecting to {host}")
    try:
        with Scrapli(**device) as ssh:
            for cmd in show_commands:
                reply = ssh.send_command(cmd)
                structured_result= reply.textfsm_parse_output()
                cmd_dict[cmd] = structured_result
        print(f"<<< Received output from {host}")
        return cmd_dict
    except (ScrapliException, SSHException, socket.timeout, OSError) as error:
        print(f"Device {host}, Transport {transport}, Error {error}")
        raise VasilyException("Ошибка соединения")


  


if __name__ == "__main__":
    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)
    
    for dev in devices:
        output = send_show(dev, "sh ip route")
        for res in output:
            pprint(res)

def test_connection_successful():
    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)
    
    for dev in devices:
        try: 
            output = send_show(dev, "sh ip route")
        except (VasilyException, Exception):
            pytest.fail("не возможно соедениться с = {}".format(dev['host']) )

def test_route_exists():
    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        output = send_show(dev, "sh ip route")
        found_route = False
       
        
        for res in output['sh ip route']:
            
            #print(type(res["mask"]) )
            if res["network"]== "192.168.100.0" and res["mask"] == "24":
                found_route = True
                break
        
        if not found_route:
            
            pytest.fail("route 192.168.100.0/24 не найден в route table для host = {}".format(dev['host'] ) )
    