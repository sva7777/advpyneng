# -*- coding: utf-8 -*-
'''
Задание 10.1

Скопировать класс IPv4Network из задания 9.1 и добавить ему все методы,
которые необходимы для реализации протокола последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__
* index, count - должны работать аналогично методам в списках и кортежах

И оба метода, которые отвечают за строковое представление экземпляров
класса IPv4Network.

Существующие методы и атрибуты (из задания 9.1) можно менять, при необходимости.

Пример создания экземпляра класса:

In [2]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [3]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6

In [4]: net1[2]
Out[4]: '8.8.4.3'

In [5]: net1[-1]
Out[5]: '8.8.4.6'

In [6]: net1[1:4]
Out[6]: ('8.8.4.2', '8.8.4.3', '8.8.4.4')

In [7]: '8.8.4.4' in net1
Out[7]: True

In [8]: net1.index('8.8.4.4')
Out[8]: 3

In [9]: net1.count('8.8.4.4')
Out[9]: 1

In [10]: len(net1)
Out[10]: 6

Строковое представление:

In [13]: net1
Out[13]: IPv4Network(8.8.4.0/29)

In [14]: str(net1)
Out[14]: 'IPv4Network 8.8.4.0/29'

'''


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
       
    def __iter__(self):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return iter(res)
    
    def __getitem__(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        ret = res[key]
        if type(ret) is str:
            return ret
        else:
            return tuple(ret)
    
        
    def index(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return res.index(key)
        
    def count(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return res.count(key)

    def __len__(self):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        return len(res)
        
    def __str__(self):
        return "IPv4Network "+str(self.__network)
    
    def __repr__(self):
        return "IPv4Network("+str(self.__network)+")"
        
    def __contains__(self, key):
        res = list ()
        for host in self.__network.hosts():
            res.append( format(host))
        for item in res:
            if item == key:
                return True
        return False
        
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
        
    

if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    for ip in net1:
        print(ip)

    print(net1[2])
    print(net1[-1])
    print(net1[1:4])
    print ('8.8.4.4' in net1)
    print(net1.index('8.8.4.4'))
    print(net1.count('8.8.4.4') )
    print(len(net1))
    print(net1)
    print(str(net1))
