# -*- coding: utf-8 -*-
"""
Задание 14.1b

Создать генератор get_intf_ip_from_files, который ожидает как аргумент
произвольное количество файлов с конфигурацией устройств и возвращает интерфейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать словарь
для каждого файла на каждой итерации:

* ключ - hostname (надо получить из конфигурационного файла из строки hostname ...)
* значение словарь, в котором:
    * ключ - имя интерфейса
    * значение - кортеж с IP-адресом и маской

Например: {'r7': {'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
                  'FastEthernet0/2': ('10.0.2.2', '255.255.255.0')}}

Проверить работу генератора на примере конфигураций config_r1.txt и config_r2.txt.

Пример результатов:
In [2]: for d in get_intf_ip_from_files("config_r1.txt"):
   ...:     pprint(d)
   ...:
{'PE_r1': {'Ethernet0/0': ('10.0.13.1', '255.255.255.0'),
           'Ethernet0/2': ('10.0.19.1', '255.255.255.0'),
           'Loopback0': ('10.1.1.1', '255.255.255.255')}}

In [3]: for d in get_intf_ip_from_files("config_r1.txt", "config_r2.txt"):
   ...:     pprint(d)
   ...:
{'PE_r1': {'Ethernet0/0': ('10.0.13.1', '255.255.255.0'),
           'Ethernet0/2': ('10.0.19.1', '255.255.255.0'),
           'Loopback0': ('10.1.1.1', '255.255.255.255')}}
{'PE_r2': {'Ethernet0/0': ('10.0.23.2', '255.255.255.0'),
           'Ethernet0/1': ('10.255.2.2', '255.255.255.0'),
           'Ethernet0/2': ('10.0.29.2', '255.255.255.0'),
           'Loopback0': ('10.2.2.2', '255.255.255.255')}}

"""
from pprint import pprint 
import re



def get_intf_ip(filename):
    
    re_string = r"interface (\S+)\n"\
              r"( .*\n)*"\
              r" ip address (\S+) (\S+)|hostname (\S+)"
    re_comp = re.compile(re_string)
    
    with open(filename) as f:
        for m in re.finditer(re_comp, f.read()):
            if m.group(5):
                switch_name = m.group(5)
            else:
                yield (switch_name, m.group(1), m.group(3), m.group(4) )


def get_intf_ip_from_files(*filenames):
    for filename in filenames:
        res = dict()
        
        
        
        gen = get_intf_ip(filename)
        res_inner = dict()
        
        for switch_name, int_f, ip, mask in gen:
            res_inner [int_f] = (ip, mask)
            sw_name= switch_name
        
        res[sw_name] = res_inner
        yield res


if __name__ == '__main__':
    gen = get_intf_ip_from_files("/home/vasily/advpyneng/exercises/14_generators/config_r1.txt", "/home/vasily/advpyneng/exercises/14_generators/config_r2.txt")

    for m in gen:
        pprint(m)
