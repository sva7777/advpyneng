# -*- coding: utf-8 -*-
"""
Задание 12.2

Скопировать класс IPv4Network из задания 11.1 и изменить его таким
образом, чтобы класс IPv4Network наследовал абстрактный класс Sequence из collections.abc.
Создать все необходимые абстрактные методы для работы IPv4Network как Sequence.

Проверить, что работают все методы характерные для последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__, index, count

Пример создания экземпляра класса:

In [1]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [2]: len(net1)
Out[2]: 6

In [3]: net1[0]
Out[3]: '8.8.4.1'

In [4]: '8.8.4.1' in net1
Out[4]: True

In [5]: '8.8.4.10' in net1
Out[5]: False

In [6]: net1.count('8.8.4.1')
Out[6]: 1

In [7]: net1.index('8.8.4.1')
Out[7]: 0

In [8]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6


"""


import ipaddress
from collections.abc import Sequence


class IPv4Network(Sequence):
    
    #ToDo gw сделать ключевым
    def __init__(self, ip_mask, gw = None):
        self.__network = ipaddress.ip_network(ip_mask)
        
        if gw:
            gw_check = ipaddress.ip_address(gw)
            
        self.gw = gw
        
        
        self.broadcast = format(self.__network.broadcast_address)
        
        if gw and (not gw_check in self.__network):
            raise ValueError("gw is not in network")
        

        self.__allocated = set()
        self.__unassigned = set()
        
        for host in self.__network.hosts():
            self.__unassigned.add(format(host))
        
        if gw:
            self.allocate_ip(gw)
       
    
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
        
    @property
    def network(self):
        return format (self.__network)

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
    
    def __getitem__(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        ret = res[key]
        if type(ret) is str:
            return ret
        else:
            return tuple(ret)
            
    def __len__(self):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return len(res)
        
    def count(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return res.count(key)

    def index(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return res.index(key)

        
if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    print( len(net1)  )
    print( net1[0]  )
    print( '8.8.4.1' in net1 )
    print( '8.8.4.10' in net1 )
    print( net1.count('8.8.4.1') )
    print( net1.index('8.8.4.1') )
    for ip in net1:
        print(ip)