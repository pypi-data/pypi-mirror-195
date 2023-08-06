from xybase.converter import Converter


class B:
    age: int


class A:
    name: str
    b: B


if __name__ == '__main__':
    c = Converter('__main__')
    a: A = c.convert({'name': 'x', 'b': {'age': 1}}, A)
    print(a.b.age)
