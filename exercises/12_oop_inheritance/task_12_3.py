# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать класс Topology, который представляет топологию сети.
Класс Topology должен наследовать абстрактный класс MutableMapping
и для всех абстрактных методов класса MutableMapping должна быть
написана рабочая реализация в классе Topology.

Проверить, что после реализации абстрактных методов, работают также
такие методы: keys, items, values, get, pop, popitem, clear, update, setdefault.

При создании экземпляра класса, как аргумент передается словарь, который описывает топологию.
В каждом экземпляре должна быть создана переменная topology, в которой
содержится словарь топологии.

Пример создания экземпляра класса:
In [1]: t1 = Topology(example1)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка реализации абстрактных методов:

получение элемента:
In [3]: t1[('R1', 'Eth0/0')]
Out[3]: ('SW1', 'Eth0/1')


Перезапись/добавление элемента:
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


Удаление:
In [11]: del t1[('R6', 'Eth0/0')]

In [12]: t1.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Итерация:
In [13]: for item in t1:
    ...:     print(item)
    ...:
('R1', 'Eth0/0')
('R2', 'Eth0/0')
('R2', 'Eth0/1')
('R3', 'Eth0/0')
('R3', 'Eth0/1')
('R3', 'Eth0/2')

Длина:
In [14]: len(t1)
Out[14]: 6

После реализации абстрактных методов, должны работать таким методы:

In [1]: t1.topology
Out[1]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

keys, values, items:
In [2]: t1.keys()
Out[2]: KeysView(<__main__.Topology object at 0xb562f82c>)

In [3]: t1.values()
Out[3]: ValuesView(<__main__.Topology object at 0xb562f82c>)

Метод get:
In [4]: t1.get(('R2', 'Eth0/0'))
Out[4]: ('SW1', 'Eth0/2')

In [6]: print(t1.get(('R2', 'Eth0/4')))
None

Метод pop:
In [8]: t1.pop(('R2', 'Eth0/0'))
Out[8]: ('SW1', 'Eth0/2')

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Метод update:
In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [11]: t1.update(t2)

In [13]: t1.topology
Out[13]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Метод clear:
In [14]: t1.clear()

In [15]: t1.topology
Out[15]: {}

"""

example1 = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R4", "Eth0/0"): ("R3", "Eth0/1"),
    ("R5", "Eth0/0"): ("R3", "Eth0/2"),
}

example2 = {("R1", "Eth0/4"): ("R7", "Eth0/0"), ("R1", "Eth0/6"): ("R9", "Eth0/0")}

from collections.abc import MutableMapping

class Topology(MutableMapping):
    def __init__(self, topology):
        if type(topology) != dict :
            raise ValueError("передан не словарь")
        self.__topology = topology
    
    @property
    def topology(self):
        return self.__topology
    
    def __getitem__(self, key):
        if key in self.__topology:
            return self.__topology[key]
        else:
            return None
        
    def __setitem__(self, key, value):
        self.__topology[key]= value
        
    def __delitem__(self, key):
        if key in self.__topology:
            del self.__topology[key]
        
    def __iter__(self):
        return iter(self.__topology)
        
    def __len__(self):
        return len(self.__topology)
        

if __name__ == "__main__":
    t1 = Topology(example1)
    print(t1.topology)
    print(t1[('R1', 'Eth0/0')])
    t1[('R1', 'Eth0/0')] = ('SW1', 'Eth0/12')
    print(t1.topology)
    t1[('R6', 'Eth0/0')] = ('SW1', 'Eth0/17')
    print(t1.topology)
    del t1[('R6', 'Eth0/0')]
    print(t1.topology)
    for item in t1:
        print(item)
    print(len(t1))
    print(t1.topology)
    print(t1.keys()) 
    print(t1.values())
    print(t1.get(('R2', 'Eth0/0')))
    print(t1.get(('R2', 'Eth0/4')))
    print(t1.pop(('R2', 'Eth0/0')))
    print(t1.topology)
    t2 = Topology(example2)
    print(t2.topology)
    t1.update(t2)
    print(t1.topology)
    t1.clear()
    print(t1.topology)
    