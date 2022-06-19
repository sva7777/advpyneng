# -*- coding: utf-8 -*-
"""
Задание 14.1a

Создать генератор get_intf_ip, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все интерфейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - имя интерфейса
* второй элемент кортежа - IP-адрес
* третий элемент кортежа - маска

Например: ('FastEthernet', '10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.
"""
import re


def get_intf_ip(filename):
    
    re_string = r"interface (\S+)\n"\
              r"( .*\n)*"\
              r" ip address (\S+) (\S+)"
    re_comp = re.compile(re_string)
    
    with open(filename) as f:
        for m in re.finditer(re_comp, f.read()):
            yield (m.group(1), m.group(3), m.group(4) )

        
    
 
if __name__ == '__main__':
    gen= get_intf_ip("/home/vasily/advpyneng/exercises/14_generators/config_r1.txt")
    for item in gen:
        print(item)