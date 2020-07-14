import abc
from typing import Iterable
from collections import namedtuple


class ModelMeta(type):

    def __init__(cls, name, bases, attrs):
        print(cls, name, bases, attrs, "__init__")
        super().__init__(name, bases, attrs)
        cls.x = None

    def __new__(mcs, name, bases, attrs):
        print(mcs, name, bases, attrs, "__new__")
        annotations = attrs["__annotations__"]
        for k, v in annotations.items():
            pass
        print(annotations["x"])
        a = "2"
        print(isinstance(a, annotations["x"]))
        return super().__new__(mcs, name, bases, attrs)


class Filed(object):

    def __init__(self, name, value, type_):
        self.name = name
        self.type_ = type_
        self.value = value


class Test(metaclass=ModelMeta):
    x: int
    # table_name = "test"
    # filed_list = ["uid", "name", "gender"]
    # data_model = namedtuple(table_name, field_names=filed_list)

    def __init__(self, *fields, **kwargs):
        # if fields:
        #     self.data = self.data_model(*fields)
        pass

    def __call__(self, *args, **kwargs):
        print(args, kwargs)


# print(Test.__annotations__)
#
b = Test(1, 2, 3)
# print(b)
# print(b.data.uid)
# b(1, 2, 3)
print(b.x)
b.x = 10
print(b.x, Test.x)
