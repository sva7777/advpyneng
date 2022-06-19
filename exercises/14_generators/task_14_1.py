# -*- coding: utf-8 -*-
"""
Задание 14.1

Создать генератор get_ip_from_cfg, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например: ('10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.

"""
import re

def get_line(filename):
    with open (filename) as f:
        while (True):
            line = f.readline()
            yield (line)


def get_ip_from_cfg(filename):
    gen = get_line(filename)
    re_comp = re.compile(r"\s+ip address (\S+) (\S+)")
    while (True):
        line = next(gen)
        if not line:
            break
        match_re = re.match(re_comp, line)
        if match_re:
            yield ( match_re.group(1), match_re.group(2))
        
    
    
gen= get_ip_from_cfg("/home/vasily/advpyneng/exercises/14_generators/config_r1.txt")

for item in gen:
    print(item)