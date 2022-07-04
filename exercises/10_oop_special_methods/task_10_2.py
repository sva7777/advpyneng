# -*- coding: utf-8 -*-
'''
Задание 10.2

Скопировать класс PingNetwork из задания 9.2 и изменить его таким образом,
чтобы адреса пинговались не при вызове метода scan, а при вызове экземпляра.

Вся функциональность метода scan должна быть перенесена в метод, который отвечает
за вызов экземпляра.

Пример работы с классом PingNetwork. Сначала создаем сеть:
In [2]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [3]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

Затем создается экземпляр класса PingNetwork, сеть передается как аргумент:
In [6]: ping_net = PingNetwork(net1)

После этого экземпляр должен быть вызываемым объектом (callable):

In [7]: ping_net()
Out[7]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [8]: ping_net(include_unassigned=True)
Out[8]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

'''

import subprocess
import sys
sys.path.insert(1, '/home/vasily/advpyneng/exercises/09_oop_basics')
from task_9_1 import IPv4Network 
from concurrent.futures import ThreadPoolExecutor


class PingNetwork:
    def __init__(self, ip_network):
        #if not (ip is IPv4Network):
        #    raise ValueError("Передан не экземпляр класса IPv4Network")
        self.__ipv4network = ip_network
    
    def __call__(self, workers = 5 , include_unassigned = False):
        return self.scan(workers, include_unassigned)
        
    def _ping(self, ip_address):
        reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8')
        if reply.returncode == 0:
            return True
        else:
            return False
    
    def scan(self, workers = 5 , include_unassigned = False):
        ok_ping = list()
        not_ping = list()
        
        ip_list = list()
        
        ip_list.extend(self.__ipv4network.allocated)
        if (include_unassigned):
            ip_list.extend(self.__ipv4network.unassigned)
        
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            result = executor.map(self._ping, ip_list)
            for ip, res  in zip(ip_list, result):
                if res:
                    ok_ping.append(ip)
                else:
                    not_ping.append(ip)
        return (ok_ping, not_ping)

if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    net1.allocate_ip('8.8.4.2')
    net1.allocate_ip('8.8.4.4')
    net1.allocate_ip('8.8.4.6')
    ping_net = PingNetwork(net1)
    print(ping_net())
    print(ping_net(include_unassigned=True))
    
    