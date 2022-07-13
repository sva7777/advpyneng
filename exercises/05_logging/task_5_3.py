# -*- coding: utf-8 -*-
"""
Задание 5.3

Этот скрипт делает обход сети начиная с одного устройства - start.
Подключившись на устройство start, выполняется команда sh cdp neighbors.
Из вывода команды мы получаем соседей. По этим данным выполняется подключение к каждому соседу
и на каждом соседе аналогично проверяются соседи.

Задача скрипта в итоге получить информацию об устройствах в сети и к каким устройствам они подключены.
Результат представлен в виде списка словарей:
[{'local_host': 'R1', 'local_port': 'Ethernet0/0', 'remote_host': 'SW1', 'remote_port': 'Ethernet0/1'},
 {'local_host': 'SW1', 'local_port': 'Ethernet0/3', 'remote_host': 'R3', 'remote_port': 'Ethernet0/0'},
 {'local_host': 'SW1', 'local_port': 'Ethernet0/2', 'remote_host': 'R2', 'remote_port': 'Ethernet0/0'},
 {'local_host': 'SW1', 'local_port': 'Ethernet0/1', 'remote_host': 'R1', 'remote_port': 'Ethernet0/0'},
 {'local_host': 'R3', 'local_port': 'Ethernet0/0', 'remote_host': 'SW1', 'remote_port': 'Ethernet0/3'},
 {'local_host': 'R3', 'local_port': 'Ethernet0/1', 'remote_host': 'R2', 'remote_port': 'Ethernet0/1'},
 {'local_host': 'R2', 'local_port': 'Ethernet0/0', 'remote_host': 'SW1', 'remote_port': 'Ethernet0/2'},
 {'local_host': 'R2', 'local_port': 'Ethernet0/1', 'remote_host': 'R3', 'remote_port': 'Ethernet0/1'}]

В этом задании нужно разобраться с кодом и добавить логирование в скрипт с одновременным выводом
информации на стандартный поток вывода и в файл task_5_3_log.txt.
На стандартный поток вывода должны выводиться сообщения уровня INFO и более критичные, а в файле все вплоть до DEBUG.
Формат логов и сообщения надо определить из примеров вывода ниже.

Большиство настроек log-сообщений будут в функции explore_topology. Можно вносить небольшие изменения в код, чтобы получить
нужный вывод логов.

Пример вывода лога на stdout (полученные данные не отображаются)
$ python task_5_3.py
10:26:04 - __main__ - INFO - Начинается обход сети. Стартовое устройство 192.168.100.1
10:26:04 - __main__ - INFO - Подключение SSH к 192.168.100.1
10:26:05 - __main__ - INFO - Подключение SSH к 192.168.100.100
10:26:06 - __main__ - INFO - Подключение SSH к 192.168.100.3
10:26:07 - __main__ - INFO - Подключение SSH к 192.168.100.2

Логи в файле task_5_3_log.txt:

2020-09-11 10:26:04,418 - __main__ - INFO - Начинается обход сети. Стартовое устройство 192.168.100.1
2020-09-11 10:26:04,422 - __main__ - INFO - Подключение SSH к 192.168.100.1
2020-09-11 10:26:05,545 - __main__ - DEBUG - Новое устройство SW1 192.168.100.100, добавляем в ToDo
2020-09-11 10:26:05,545 - __main__ - INFO - Подключение SSH к 192.168.100.100
2020-09-11 10:26:06,497 - __main__ - DEBUG - Новое устройство R3 192.168.100.3, добавляем в ToDo
2020-09-11 10:26:06,497 - __main__ - DEBUG - Новое устройство R2 192.168.100.2, добавляем в ToDo
2020-09-11 10:26:06,497 - __main__ - DEBUG - Уже были на устройстве R1
2020-09-11 10:26:06,497 - __main__ - INFO - Подключение SSH к 192.168.100.3
2020-09-11 10:26:07,631 - __main__ - DEBUG - Уже были на устройстве SW1
2020-09-11 10:26:07,631 - __main__ - DEBUG - Новое устройство R2 10.100.23.2, добавляем в ToDo
2020-09-11 10:26:07,631 - __main__ - INFO - Подключение SSH к 192.168.100.2
2020-09-11 10:26:08,687 - __main__ - DEBUG - Уже были на устройстве SW1
2020-09-11 10:26:08,687 - __main__ - DEBUG - Уже были на устройстве R3
2020-09-11 10:26:08,688 - __main__ - DEBUG - Уже были на устройстве R2

Для заданий этого раздела нет тестов.
"""
import re
from pprint import pprint
from tabulate import tabulate
import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import SSHException

import logging

def parse_cdp(output):
    regex = (
        r"Device ID: (?P<remote_host>\w+)\."
        r".*?"
        r"IP address: (?P<remote_ip>\S+)\n"
        r".*?"
        r"Interface: (?P<local_port>\S+), +"
        r"Port ID \(outgoing port\): (?P<remote_port>\S+)"
    )
    neighbors = [match.groupdict() for match in re.finditer(regex, output, re.DOTALL)]
    return neighbors


def connect_ssh(params, command):
    try:
        logger.info("Подключение SSH к {}".format(params['host']))
        with ConnectHandler(**params) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            local_host = re.search(r"(\S+)[>#]", prompt).group(1)
            return local_host, ssh.send_command(command)
    except SSHException as error:
        print(error)


def explore_topology(start_device_ip, ssh_params):
    ip_hostname_dict = {}
    visited_hostnames = set()
    topology = []
    todo = [start_device_ip]
    
    logger.info("Начинается обход сети. Стартовое устройство {}".format(start_device_ip))

    while len(todo) > 0:
        current_ip = todo.pop(0)
        if ip_hostname_dict.get(current_ip) in visited_hostnames:
            continue
        ssh_params["host"] = current_ip

        current_host, sh_cdp_neighbors_output = connect_ssh(
            ssh_params, "sh cdp neig det"
        )
        neighbors = parse_cdp(sh_cdp_neighbors_output)
        visited_hostnames.add(current_host)

        for neighbor_link in neighbors:
            neighbor_ip = neighbor_link.pop("remote_ip")
            
            #vasily map
            if neighbor_ip =="192.168.255.2":
                neighbor_ip = "10.210.255.2"
            if neighbor_ip =="192.168.255.3":
                neighbor_ip = "10.210.255.3"
            if neighbor_ip =="192.168.255.4":
                neighbor_ip = "10.210.255.4"
            if neighbor_ip =="192.168.255.5":
                neighbor_ip = "10.210.255.5"
            
            neighbor = neighbor_link["remote_host"]
            ip_hostname_dict[neighbor_ip] = neighbor
            topology.append({"local_host": current_host, **neighbor_link})

            if neighbor not in visited_hostnames:
                logger.debug("Новое устройство {} {} , добавляем в ToDo".format(neighbor, neighbor_ip))
                todo.append(neighbor_ip)
            else:
                logger.debug("Уже были на устройстве {}".format(neighbor))
            
    return topology


if __name__ == "__main__":
    # setup loggers
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s- %(levelname)s - %(message)s", "%H:%M:%S")
    ch.setFormatter(formatter)
    
    file = logging.FileHandler("task_5_3_my_log.txt")
    file.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file.setFormatter(file_formatter)
    
    logger.addHandler(ch)
    logger.addHandler(file)
    
    common_params = {
        "device_type": "cisco_ios",
        "password": "cisco",
        "secret": "cisco",
        "username": "cisco",
        "timeout": 4,
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    start = "10.210.255.2"
    topology = explore_topology(start, ssh_params=common_params)
    pprint(topology, width=120)
    print(tabulate(topology, headers="keys"))