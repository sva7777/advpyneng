# -*- coding: utf-8 -*-
"""
Задание 2.1

Написать аннотацию для всех методов класса IPv4Network:
аннотация должна описывать параметры и возвращаемое значение.

Проверить код с помощью mypy, если возникли какие-то ошибки, исправить их.

"""
import ipaddress
from typing import List, Iterator


class IPv4Network:
    def __init__(self, network : str) -> None:
        self.network = network
        address, mask = network.split("/")
        self.network_address = address
        self.mask = int(mask)
        self.bin_mask = "1" * self.mask + "0" * (32 - self.mask)

    def hosts(self) -> List[str]:
        net = ipaddress.ip_network(self.network)
        return [str(ip) for ip in net.hosts()]

    def __repr__(self) -> str:
        return f"Network('{self.network}')"

    def __len__(self) -> int:
        return len(self.hosts())

    def __iter__(self) -> Iterator[str]:
        return iter(self.hosts())


if __name__ == "__main__":
    net1 = IPv4Network("10.1.1.0/28")
    all_hosts = net1.hosts()
    print(all_hosts)
