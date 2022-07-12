# -*- coding: utf-8 -*-
"""
Задание 5.2

В файле cisco_telnet_class.py создан класс CiscoTelnet и в классе есть log-сообщения.

Настроить логирование в задании таким образом, чтобы при выполнени кода в блоке if __name__ == "__main__":
был такой вывод:

$ python task_5_2.py
10:18:57 - cisco_telnet_class - DEBUG - Telnet подключение к 192.168.100.1
10:18:58 - cisco_telnet_class - DEBUG - Отправка команды sh clock на 192.168.100.1
sh clock
*10:19:43.886 UTC Fri Sep 11 2020
R1#

При этом нельзя менять код в файле cisco_telnet_class.py.

Для заданий этого раздела нет тестов.
"""
from cisco_telnet_class import CiscoTelnet
import logging

if __name__ == "__main__":
    
    log = logging.getLogger("cisco_telnet_class")
    log.setLevel(logging.DEBUG)
    
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s", "%H:%M:%S")
    ch.setFormatter(formatter)

    log.addHandler(ch)
    

    r1 = CiscoTelnet(
        "10.210.255.2", username="cisco", password="cisco", enable_password="cisco"
    )
    
    print(r1.send_show_command("sh clock"))