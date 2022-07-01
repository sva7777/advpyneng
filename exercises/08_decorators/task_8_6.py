# -*- coding: utf-8 -*-
"""
Задание 8.6

Создать декоратор total_order, который добавляет к классу методы:

* __ge__ - операция >=
* __ne__ - операция !=
* __le__ - операция <=
* __gt__ - операция >


Декоратор total_order полагается на то, что в классе уже определены методы:
* __eq__ - операция ==
* __lt__ - операция <

Если методы __eq__ и __lt__ не определены, сгенерировать исключение ValueError при декорации.

Проверить работу декоратора можно на примере класса IPAddress. Класс нельзя менять,
можно только декорировать.
Декоратор не должен использовать переменные класса/экземпляров IPAddress. Для работы методов
должны использоваться только существующие методы __eq__ и __lt__.
Декоратор должен работать и с любым другим классом у которого
есть методы __eq__ и __lt__.


Пример проверки методов с классом IPAddress после декорирования:
In [4]: ip1 = IPAddress('10.10.1.1')

In [5]: ip2 = IPAddress('10.2.1.1')

In [6]: ip1 < ip2
Out[6]: False

In [7]: ip1 > ip2
Out[7]: True

In [8]: ip1 >= ip2
Out[8]: True

In [9]: ip1 <= ip2
Out[9]: False

In [10]: ip1 == ip2
Out[10]: False

In [11]: ip1 != ip2
Out[11]: True

"""
import ipaddress




def total_order(cls):
    def __ge__(self, other):
        if self < other:
            return False
        else:
            return True
    def __ne__(self, other):
        if  (self == other):
            return False
        else:
            return True
    def __le__(self, other):
        if (self < other) or (self == other):
            return True
        else:
            return False
    def __gt__(self, other):
        if not (self <other) and not (self == other):
            return True
        else:
            return False
            
    #check existance of __eq__ and __lt__
    eq = getattr(cls, "__eq__", None)
    lt = getattr(cls, "__lt__", None)
    if (eq is None) or (lt is None):
        raise ValueError("нет атрибута __eq__ или __lt__")
    if (not callable(eq)) or (not callable(lt)):
        raise ValueError("нет метода __eq__ или __lt__")

    cls.__ge__= __ge__
    cls.__ne__= __ne__
    cls.__le__= __le__
    cls.__gt__= __gt__
    
    
    return cls

@total_order
class IPAddress:
    def __init__(self, ip):
        self._ip = int(ipaddress.ip_address(ip))
        self.ip = ip

    def __repr__(self):
        return "IPAddress('{}')".format(self.ip)

    def __eq__(self, other):
        return self._ip == other._ip

    def __lt__(self, other):
        return self._ip < other._ip

@total_order
class DoThing:
    pass
    
if __name__ == "__main__":
    ip1 = IPAddress('10.10.1.1')
    ip2 = IPAddress('10.2.1.1')
    print(ip1 < ip2)
    print(ip1 > ip2)
    print(ip1 >= ip2)
    print(ip1 <= ip2)
    print(ip1 == ip2)
    print(ip1 != ip2)