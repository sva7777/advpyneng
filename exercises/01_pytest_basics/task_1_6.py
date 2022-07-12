# -*- coding: utf-8 -*-
"""
Задание 1.6

Написать тест(ы), который проверяет находятся ли все интерфейсы, которые указаны
в файле net_interfaces_up.yaml в состоянии up (например, столбец Protocol в выводе sh ip int br).

Для проверки надо подключиться к каждому маршрутизатору, который указан
в файле net_interfaces_up.yaml с помощью scrapli/netmiko и проверить статус
интерфейсов. Можно использовать параметры из devices_reachable.yaml.

Тест(ы) должен проходить, если все интерфейсы из файла net_interfaces_up.yaml в состоянии up.
Тест может быть один или несколько. Файл net_interfaces_up.yaml можно менять - писать другие
интерфейсы или IP-адреса, главное чтобы формат оставался таким же.

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
                structured_result = reply.textfsm_parse_output()
                cmd_dict[cmd] = structured_result
        print(f"<<< Received output from {host}")
        return cmd_dict
    except (ScrapliException, SSHException, socket.timeout, OSError) as error:
        print(f"Device {host}, Transport {transport}, Error {error}")
        raise VasilyException("Ошибка соединения")


def get_devices_params_to_connect(devices, interfaces):
    
    
    result = list ()
    
    for dev in devices:
        host = dev['host']
        flag_found = False
        
        for key in interfaces.keys():
            if host == key: 
                flag_found = True
                break
        
        if flag_found:
            result.append(dev)
        
    return result


if __name__ == "__main__":
    
    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)
    
    with open("net_interfaces_up.yaml") as f:
        interfaces = yaml.safe_load(f)

    pprint(interfaces)
    
    devices = get_devices_params_to_connect(devices, interfaces)
    
    for dev in devices:
        output = send_show(dev, "sh ip int br")
        pprint(output)

def test_connection_successful():

    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)
    
    with open("net_interfaces_up.yaml") as f:
        interfaces = yaml.safe_load(f)

    devices = get_devices_params_to_connect(devices, interfaces)
    
    for dev in devices:
        try: 
            output = send_show(dev, "sh ip int br")
        except (VasilyException, Exception):
            pytest.fail("не возможно соедениться с = {}".format(dev['host']) )


def check_interface_status(dev_info, intf):
    flag_found= False
    
    for dev in dev_info:
        if dev['intf'] == intf:
            flag_found = True
            if dev['proto'] != "up":
                pytest.fail("Интерфейс = {} у устройства {} не в статусе up".format(intf, dev) )
    
    if flag_found == False:
        pytest.fail("Не найден интерфейс = {} в ={}".format(intf, dev_info) )
    


def test_protocols_up():
    with open("devices_reachable.yaml") as f:
        devices = yaml.safe_load(f)
    
    with open("net_interfaces_up.yaml") as f:
        interfaces = yaml.safe_load(f)

    devices = get_devices_params_to_connect(devices, interfaces)
    
    for dev in devices:
        output = send_show(dev, "sh ip int br")
        host = dev['host']
        dev_info= output['sh ip int br']        
        flag_passed = True
        
        for intf in interfaces[host]:
            check_interface_status(dev_info, intf)

    
    