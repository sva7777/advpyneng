# -*- coding: utf-8 -*-
"""
Задание 12.1a

Скопировать класс CiscoTelnet из задания 12.1 и добавить проверку на ошибки.

Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
* Invalid input detected, Incomplete command, Ambiguous command

Создать исключение ErrorInCommand, которое будет генерироваться при возникновении
ошибки на оборудовании.

Метод ожидает как аргумент команду и вывод команды. Если в выводе не обнаружена ошибка,
метод ничего не возвращает. Если в выводе найдена ошибка, метод генерирует исключение
ErrorInCommand с сообщением о том какая ошибка была обнаружена, на каком устройстве и в какой команде.

Добавить проверку на ошибки в методы send_show_command и send_config_commands.

Пример работы класса с ошибками:
In [1]: r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')

In [2]: r1.send_show_command('sh clck')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-e26d712f3ad3> in <module>
----> 1 r1.send_show_command('sh clck')
...
ErrorInCommand: При выполнении команды "sh clck" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

In [3]: r1.send_config_commands('loggg 7.7.7.7')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-3-ab4a1ce52554> in <module>
----> 1 r1.send_config_commands('loggg 7.7.7.7')
...
ErrorInCommand: При выполнении команды "loggg 7.7.7.7" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

Без ошибок:
In [4]: r1.send_show_command('sh clock')
Out[4]: 'sh clock\r\n*09:39:38.633 UTC Thu Oct 10 2019\r\nR1#'

In [5]: r1.send_config_commands('logging 7.7.7.7')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 7.7.7.7\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop77\r\nR1(config-if)#ip address 107.7.7.7 255.255.255.255\r\nR1(config-if)#end\r\nR1#'



Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.
R1(config)#logging
% Incomplete command.

R1(config)#sh i
% Ambiguous command:  "sh i"
"""

from base_telnet_class import TelnetBase
import re 


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class CiscoTelnet(TelnetBase):
    def __init__(self, ip, username, password, enable, disable_paging = True, encoding= "ascii"):
        super().__init__(ip, username, password, encoding)
        if enable:
            self._write_line("enable")
            self._read_until_regex("Password:") 
            self._telnet.write(enable.encode("utf-8") + b"\n")
            self._read_until_regex("#")
            
        if disable_paging:
            self._write_line("terminal length 0")
            self._read_until_regex("#")
    
    def _check_error_in_command(self, command, output):
        regex = "% (?P<err>.+)"
        
        message = (
            'При выполнении команды "{cmd}" на устройстве {device} '
            'возникла ошибка "{error}"'
        )
            
        error_in_cmd = re.search(regex, output)
        
        if error_in_cmd:
            raise ErrorInCommand(message.format(cmd= command, device=self.host, error= error_in_cmd.group("err")  ))

    
    def send_show_command(self, command):
        self._write_line(command)
        command_output = self._read_until_regex("#")
        self._check_error_in_command(command, command_output)
        return command_output
    
    def _enter_config_mode(self):
        self._write_line("conf t")
        return self._read_until_regex("(config)#")
        
    def _exit_config_mode(self):
        self._write_line("end")
        return self._read_until_regex("#")
        
    def _send_config_command(self, command):
        self._write_line(command)
        output = self._read_until_regex("#")
        self._check_error_in_command(command, output)
        return output
    
    def send_config_commands(self, commands):
        result = self._enter_config_mode()
        if type(commands) == str:
            commands= [commands]
        
        for command in commands:
            result = result + self._send_config_command(command)
        
        result = result + self._exit_config_mode()
        
        return result


# списки команд с ошибками и без:
config_commands_errors = ["logging 0255.255.1", "logging", "sh i"]
correct_config_commands = ["logging buffered 20010", "ip http server"]


if __name__ == "__main__":
    r1 = CiscoTelnet('10.210.255.2', 'cisco', 'cisco', 'cisco')
    r1.send_show_command('sh clck')
    r1.send_config_commands('loggg 7.7.7.7')