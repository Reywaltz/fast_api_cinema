from dataclasses import dataclass

@dataclass
class A:
    a: int


@dataclass
class B(A):
    b: int

@dataclass
class C(A):
    c: int

def outer_def(abstract_class: A):
    def inner_def(a):
        return A(a)
    return inner_def


test = outer_def(A)
print(test(5))

