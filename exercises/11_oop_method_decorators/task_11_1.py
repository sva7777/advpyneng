# -*- coding: utf-8 -*-
"""
Задание 11.1

Скопировать класс IPv4Network из задания 9.1.
Переделать класс таким образом, чтобы запись значения в переменную hosts
была запрещена.


Пример создания экземпляра класса:
In [1]: net1 = IPv4Network('8.8.4.0/29')

In [2]: net1.hosts
Out[2]: ('8.8.4.1', '8.8.4.2', '8.8.4.3', '8.8.4.4', '8.8.4.5', '8.8.4.6')

Запись переменной:

In [6]: net1.hosts = 'test'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-6-c98e898835e1> in <module>
----> 1 net1.hosts = 'test'

AttributeError: can't set attribute

"""
import ipaddress

class IPv4Network:
    
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
        
    