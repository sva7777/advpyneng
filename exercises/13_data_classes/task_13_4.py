# -*- coding: utf-8 -*-
"""
Задание 13.4

Скопировать и переделать класс IPv4Network из задания 9.1
с использованием dataclass. У каждого экземпляра класса
IPv4Network должны быть такие переменные:

* network - строка вида "10.1.1.0/29"
* broadcast - строка вида "10.1.1.7"
* gw - None или строка вида "10.1.1.1"
* hosts - кортеж со всеми IP-адресами указанной сети
  пример для net1 ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6')
* allocated - множество IP-адресов, которые назначены на какие-то устройства в сети
* unassigned - множество со свободными IP-адресами

И такие методы:

* allocate_ip - ожидает как аргумент один IP-адрес. Если адрес входит в сеть экземпляра
  и еще не выделен, метод добавляет адрес в множество allocated (и удаляет из unassigned).
  Если адрес не из сети экземпляра, генерируется исключение ValueError. Если адрес уже
  находится в allocated, генерируется ValueError.
* free_ip - делает обратную операцию по сравнению с allocate_ip, аналогично работает с
  множествами allocated и unassigned. И генерирует ValueError при попытке освободить адрес,
  который и так свободен

Для реализации функционала класса можно использовать модуль ipaddress.

Пример создания экземпляра класса:

In [1]: from task_13_4 import IPv4Network

In [2]: net1 = IPv4Network('10.1.1.0/29')

In [3]: net1
Out[3]: IPv4Network(network='10.1.1.0/29', hosts=('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6'))

In [4]: net1.network
Out[4]: '10.1.1.0/29'

In [5]: net1.broadcast
Out[5]: '10.1.1.7'

In [6]: net1.gw

In [7]: net1.allocated
Out[7]: set()

In [8]: net1.unassigned
Out[8]: {'10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6'}

In [9]: net1.hosts
Out[9]: ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6')

In [10]: net1 = IPv4Network('10.1.1.0/29', gw='10.1.1.1')

In [11]: net1.allocated
Out[11]: {'10.1.1.1'}

In [12]: net1.allocate_ip('10.1.1.3')

In [13]: net1.allocate_ip('10.1.1.6')

In [14]: net1.allocated
Out[14]: {'10.1.1.1', '10.1.1.3', '10.1.1.6'}

In [15]: net1.unassigned
Out[15]: {'10.1.1.2', '10.1.1.4', '10.1.1.5'}

"""

import ipaddress
from dataclasses import dataclass, field
import dataclasses


_original_create_fn = dataclasses._create_fn

def _new_create_fn(name, args, body, **kwargs):
    args_str = ', '.join(args)
    body_str = '\n'.join('  ' + l for l in body)
    print(f'def {name}({args_str}):\n{body_str}\n')
    return _original_create_fn(name, args, body, **kwargs)

dataclasses._create_fn = _new_create_fn



@dataclass
class IPv4Network:
    network : str
    
    def __init__(self, network, gw = None):
        self.__network = ipaddress.ip_network(network)
        
        self.network = network
        self.gw = gw
        
        if gw:
            gw_check = ipaddress.ip_address(gw)
            
        self.broadcast = format(self.__network.broadcast_address)
        
        if self.gw and (not gw_check in self.__network):
            raise ValueError("gw is not in network")
        

        self.__allocated = set()
        self.__unassigned = set()
        
        for host in self.__network.hosts():
            self.__unassigned.add(format(host))
        
        if gw:
            self.allocate_ip(gw)

    
    def __repr__(self):
        return "IPv4Network(network='{}',, hosts={}".format(self.network, self.hosts)
        
    
    @property
    def hosts(self):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return tuple(res)
        
    @property
    def allocated(self):
        return self.__allocated
    
    @property
    def unassigned(self):
        return self.__unassigned
        
    def allocate_ip(self, ip):
        ip_address = ipaddress.ip_address(ip)
        if not ip_address in self.__network:
            raise ValueError("Адрес не входит в данную сеть")
        if ip in self.allocated: 
            raise ValueError("Адрес уже выделен")
        
        self.__allocated.add(ip)
        self.__unassigned.remove(ip)
        
    def free_ip(self, ip):
        ip_address = ipaddress.ip_address(ip)
        if not (ip  in self.__allocated):
            raise ValueError("Данный адрес не был выделен")
            
        self.__allocated.remove(ip)
        self.__unassigned.add(ip)


if __name__ == "__main__":
    net1 = IPv4Network('10.1.1.0/29')
    print(net1)
    print(net1.network)
    print(net1.broadcast)
    print(net1.gw)
    print(net1.allocated)
    print(net1.unassigned)
    print(net1.hosts)
    net1 = IPv4Network('10.1.1.0/29', gw='10.1.1.1')
    print(net1)
    print(net1.allocated)
    net1.allocate_ip('10.1.1.3')
    net1.allocate_ip('10.1.1.6')
    print(net1.allocated)
    print(net1.unassigned)
    
    
    
    