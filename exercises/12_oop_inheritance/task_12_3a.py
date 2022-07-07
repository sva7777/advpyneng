# -*- coding: utf-8 -*-
"""
Задание 12.3a

Скопировать класс Topology из задания 12.3.
В этом задании две части (подробнее ниже):
1. удаление дублирующих соединений при создании экземпляра
2. добавить возможность работать со значениями как с ключами

1 часть задания: При создании экземпляра класса, как аргумент теперь
передается словарь, который может содержать дублирующиеся соединения.
Дублем считается ситуация, когда в словаре есть такие пары:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1') и ('SW1', 'Eth0/1'): ('R1', 'Eth0/0')

Обе пары описывают то же самое соединение в сети (дубль) и для описания топологии
достаточно оставить только одну пару ключ значение.
При создании экземпляра класса надо обрабатывать исходный словарь и удалять одно из
дублирующих соединений - при удалении дублей надо оставить ту пару, где key < value.

Ключом должно быть меньший кортеж, а значением больший. Из таких двух пар:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1') и ('SW1', 'Eth0/1'): ('R1', 'Eth0/0')

должна остаться первая
('R1', 'Eth0/0'): ('SW1', 'Eth0/1').

Итоговый словарь без дублей надо записать в переменную экземлпяра topology.

2 часть задания: Дополнить класс Topology таким образом, чтобы методы __getitem__,
__setitem__, __delitem__, могли работать с соединением и в том случае,
когда вместо ключа, передается значение из словаря.

Пример создания экземпляра класса:
In [1]: t1 = Topology(example1)

После создания экземлпяра, в topology словарь без дублей
In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка 2 части задания:

получение элемента (по ключу получаем значение):
In [3]: t1[('R1', 'Eth0/0')]
Out[3]: ('SW1', 'Eth0/1')

получение элемента (по значению получаем ключ):
In [4]: t1[('SW1', 'Eth0/2')]
Out[4]: ('R2', 'Eth0/0')

Перезапись/запись элемента:
In [5]: t1[('R1', 'Eth0/0')] = ('SW1', 'Eth0/12')

In [6]: t1.topology
Out[6]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [7]: t1[('R6', 'Eth0/0')] = ('SW1', 'Eth0/17')

In [8]: t1.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17')}

In [9]: t1[('SW1', 'Eth0/21')] = ('R7', 'Eth0/0')

In [10]: t1.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17'),
 ('R7', 'Eth0/0'): ('SW1', 'Eth0/21')}

Удаление (по ключу):
In [11]: del t1[('R7', 'Eth0/0')]

In [12]: t1.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17')}

Удаление (по значению):
In [13]: del t1[('SW1', 'Eth0/17')]

In [14]: t1.topology
Out[14]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Итерация:
In [15]: for item in t1:
    ...:     print(item)
    ...:
('R1', 'Eth0/0')
('R2', 'Eth0/0')
('R2', 'Eth0/1')
('R3', 'Eth0/0')
('R3', 'Eth0/1')
('R3', 'Eth0/2')

Длина:
In [16]: len(t1)
Out[16]: 6

"""

example1 = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R4", "Eth0/0"): ("R3", "Eth0/1"),
    ("R5", "Eth0/0"): ("R3", "Eth0/2"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

example2 = {("R1", "Eth0/4"): ("R7", "Eth0/0"), ("R1", "Eth0/6"): ("R9", "Eth0/0")}



from collections.abc import MutableMapping
from pprint import pprint

class Topology(MutableMapping):
    
    @staticmethod
    def _normalize_topology(topology):
        
        
        #
        res = dict()
        for l1_left, l1_rigth in topology.items():
            if  l1_rigth in res.keys():
                # нужно решить какой оставить
                if l1_left < res[l1_rigth]:
                    pass
                else:
                    del res[l1_rigth]
                    res[l1_left]=l1_rigth
            else:
                res[l1_left]=l1_rigth
        return res

    
    def __init__(self, topology):
        if type(topology) != dict :
            raise ValueError("передан не словарь")
        self.__topology = Topology._normalize_topology(topology)
    
    @property
    def topology(self):
        return self.__topology
    
    def __getitem__(self, item):
        if item in self.__topology:
            return self.__topology[item]
        else:
            for key, value in self.__topology.items():
                if item == value:
                    return key
        
    def __setitem__(self, key, value):
        self.__topology[key]= value
        self.__topology = Topology._normalize_topology(self.__topology)
        
    def __delitem__(self, item):
        to_del = None
        if item in self.__topology:
            del self.__topology[item]
        else:
            for key, value in self.__topology.items():
                if item == value:
                    del self.__topology[key]
                    break
            
        
    def __iter__(self):
        return iter(self.__topology)
        
    def __len__(self):
        return len(self.__topology)


example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
        }


if __name__ == "__main__":
    #t1 = Topology(example1)
    #pprint(t1.topology)
    
    top = Topology(example)
    if top[("R1", "Eth0/0")] == ("SW1", "Eth0/1") :
        pprint("Hello1")
    else:
        pprint("Hello2")
    