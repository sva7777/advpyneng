# -*- coding: utf-8 -*-
"""
Задание 1.2

Написать тесты для класса Network. Тесты должны проверять:

* переменные экземпляров network и addresses:
  * наличие переменной экземпляра
  * правильное значение

* метод __iter__:
  * метод есть
  * возвращает итератор
  * при итерации возвращаются IP-адреса и правильные IP-адреса (достаточно проверить 2 адреса)

* метод __len__:
  * проверка количества IP-адресов

* метод __getitem__:
  * проверить обращение по положительному, отрицательному индексу
  * проверить, что при обращении к не существующему индексу, генерируется исключение IndexError


Тесты написать в файле заданий. Разделить на тесты по своему усмотрению.

Ограничение: класс менять нельзя.
Для заданий этого раздела нет тестов для проверки тестов :)
"""
import ipaddress
import inspect


class Network:
    def __init__(self, network):
        self.network = network
        subnet = ipaddress.ip_network(self.network)
        self.addresses = tuple([str(ip) for ip in subnet.hosts()])

    def __iter__(self):
        return iter(self.addresses)

    def __len__(self):
        return len(self.addresses)

    def __getitem__(self, index):
        return self.addresses[index]


if __name__ == "__main__":
    # пример создания экземпляра
    net1 = Network('10.1.1.192/30')
    print(net1.addresses[-4])
    

def test_Network_variables_exist():
    net1 = Network("10.1.1.192/30")
    assert getattr(net1, "network", None) != None , "Атрибут network не найден"
    assert getattr(net1, "addresses", None) != None , "Атрибут addresses не найден"
    
def test_Network_variables_correct_values():
    net1 = Network("10.1.1.192/30")
    assert net1.network == "10.1.1.192/30"  , "Атрибут network содержит не корректное значение"
    assert net1.addresses == ('10.1.1.193', '10.1.1.194'), "Атрибут addresses содержит не корректное значение"


def test_Network_method_iter_exists():
    net1 = Network("10.1.1.192/30")
    
    assert getattr(net1, "__iter__", None) != None , "Метод __iter__ не найден"
    assert inspect.ismethod( getattr(net1, "__iter__")) , "__iter__ должен быть методом, а не переменной"
    

def test_Network_method_iter_works():
    net1 = Network("10.1.1.192/30")
    try:
        iterator = iter(net1)
    except TypeError as error:
        pytest.fail("Network не итерируемый объект\n", error)
    else:
        item1 = next(iterator)
        item2 = next(iterator)
        assert item1 == "10.1.1.193" , "Итератор вернул не корректное значение"
        assert item2 == "10.1.1.194" , "Итератор вернул не корректное значение"

def test_Network_method_len():
    net1 = Network("10.1.1.192/30")
    assert len(net1) == 2, "len возвратил не корректное значение"
    

def test_Network_method_getitem():
    net1 = Network("10.1.1.192/30")
    assert net1[0] == "10.1.1.193",  "не корректное значение при обращении по индексу"
    assert net1[1] == "10.1.1.194",  "не корректное значение при обращении по индексу"
    assert net1[-1] == "10.1.1.194",  "не корректное значение при обращении по индексу"
    assert net1[-2] == "10.1.1.193",  "не корректное значение при обращении по индексу"
    try:
        i = net1[2]
    except IndexError as error:
        pass
    else:
        pytest.fail("не сгенерировано исключение при обращение по не существующему индексу", error)