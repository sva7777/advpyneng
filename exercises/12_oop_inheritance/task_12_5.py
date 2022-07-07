# -*- coding: utf-8 -*-
"""
Задание 12.5

Создать примесь InheritanceMixin с двумя методами:

* subclasses - отображает дочерние классы
* superclasses - отображает родительские классы

Методы должны отрабатывать и при вызове через класс и при вызове
через экземпляр:
In [2]: A.subclasses()
Out[2]: [__main__.B, __main__.D]

In [3]: A.superclasses()
Out[3]: [__main__.A, __main__.InheritanceMixin, object]

In [4]: a.subclasses()
Out[4]: [__main__.B, __main__.D]

In [5]: a.superclasses()
Out[5]: [__main__.A, __main__.InheritanceMixin, object]

В задании заготовлена иерархия классов, надо сделать так, чтобы у всех
этих классов повились методы subclasses и superclasses.
Определение классов можно менять.
"""

class InheritanceMixin:
        
    def subclasses(self= None):
        return InheritanceMixin.__subclasses__()
        
    def superclasses(self = None):
        return InheritanceMixin.mro()


class A(InheritanceMixin):
    pass


class B(A):
    pass


class C(InheritanceMixin):
    pass


class D(A, C):
    pass

if __name__ == "__main__":
    print(A.subclasses())
    print(A.superclasses())
    a = A()
    print(a.subclasses())
    print(a.superclasses())