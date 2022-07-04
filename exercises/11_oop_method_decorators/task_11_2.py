# -*- coding: utf-8 -*-
"""
Задание 11.2

Скопировать класс PingNetwork из задания 9.2.
Один из методов класса зависит только от значения аргумента и не зависит
от значений переменных экземпляра или другого состояния объекта.

Сделать этот метод статическим и проверить работу метода.

"""

import subprocess
import sys
sys.path.insert(1, '/home/vasily/advpyneng/exercises/09_oop_basics')
from task_9_1 import IPv4Network 
from concurrent.futures import ThreadPoolExecutor


class PingNetwork:
    def __init__(self, ip):
        #if not (ip is IPv4Network):
        #    raise ValueError("Передан не экземпляр класса IPv4Network")
        self.__ipv4network = ip
    
    @staticmethod
    def _ping( ip_address):
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
            result = executor.map(_ping, ip_list)
            for ip, res  in zip(ip_list, result):
                if res:
                    ok_ping.append(ip)
                else:
                    not_ping.append(ip)
        return (ok_ping, not_ping)

if __name__ == "__main__":
    pass