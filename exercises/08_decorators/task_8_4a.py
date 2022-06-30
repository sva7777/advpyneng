# -*- coding: utf-8 -*-
"""
Задание 8.4a

Переделать декоратор retry из задания 8.4: добавить параметр delay,
который контролирует через какое количество секунд будет выполняться повторная попытка.
При каждом повторном запуске результат проверяется:

* если он был истинным, он возвращается
* если нет, функция запускается повторно заданное количество раз

Если в любое из повторений результат истинный, надо вернуть результат
и больше не вызывать функцию повторно.

Пример работы декоратора:
In [2]: @retry(times=3, delay=5)
    ..: def send_show_command(device, show_command):
    ..:     print('Подключаюсь к', device['host'])
    ..:     try:
    ..:         with ConnectHandler(**device) as ssh:
    ..:             ssh.enable()
    ..:             result = ssh.send_command(show_command)
    ..:         return result
    ..:     except (NetMikoAuthenticationException, NetMikoTimeoutException):
    ..:         return None
    ..:

In [3]: send_show_command(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Out[4]: '*16:35:59.723 UTC Fri Oct 18 2019'

In [5]: device_params['password'] = '123123'

In [6]: send_show_command(device_params, 'sh clock')
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1
Повторное подключение через 5 сек
Подключаюсь к 192.168.100.1


Тест проверяет декоратор на другой функции (не на send_show_command).
Значения в словаре device_params можно менять, если используются
другие адреса/логины.

Ограничение: Функцию send_show_command менять нельзя, можно только применить декоратор.
"""

from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)

import time

device_params = {
    "device_type": "cisco_ios",
    "host": "10.210.255.22",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}
def retry(times=0, delay =0):
    def wrapper(func):
        def inner(*args, **kwargs):
            for retry in range(0,times+1):
                result = func(*args, **kwargs)
                if result:
                    return result
                if retry != times:
                    print("Повторное подключение через {} сек".format(delay))
                time.sleep(delay)
        return inner

    return wrapper
    
@retry(times=3, delay=5)
def send_show_command(device, show_command):
    print("Подключаюсь к", device["host"])
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(show_command)
        return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        return None


if __name__ == "__main__":
    output = send_show_command(device_params, "sh clock")
    print(output)