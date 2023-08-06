import builtins, typing, types
import inspect


class A:
    damn = "Damn"
    def __init__(self):
        self.pog = "Pog"
        self.dupa = "XD"
        self.something()
        self.yo = "TOO"

    def something(self):
        pass

class B(A):
    pass

class C(A):
    pass

class D(C):
    def check_type_compatibility(self, type_a, type_b, check_flipped=True):
        if type_a == 0 and type_b != 1:
            return True
        if check_flipped:
            if type_a == type_b:
                return True
            if isinstance(type_a, type) and isinstance(type_b, type):
                return False
            if self.check_type_compatibility(type_b, type_a, False):
                return True
        if typing.get_origin(type_a) == typing.Union or typing.get_origin(type_a) == types.UnionType:
            for arg in typing.get_args(type_a):
                if self.check_type_compatibility(arg, type_b):
                    return True
        if typing.get_origin(type_a) == tuple:
            if hasattr(type_b, '__iter__') and len(typing.get_args(type_a)) == len(type_b):
                return True
        if typing.get_origin(type_a) == list:
            required_elements_type = typing.get_args(type_a)
            if len(required_elements_type) == 1:
                required_elements_type = required_elements_type[0]
                if isinstance(type_b, tuple) or isinstance(type_b, list):
                    for element in type_b:
                        if element != required_elements_type:
                            break
                    else:
                        return True
                if type_b == tuple or typing.get_origin(type_b) == tuple:
                    for arg in typing.get_args(type_b):
                        if arg != required_elements_type:
                            break
                    else:
                        return True
        return False


if __name__ == "__main__":
    print(4.0.__eq__((2, 5)))


    # print(typing.get_origin(typing.Union[int, typing.Tuple[int, int]]))
    # print(typing.get_args(int | float))
    # print(typing.get_args(typing.Tuple[int, float]))
    # print(typing.get_origin())
    # print(isinstance(typing.Tuple[int, int], type))


    # if hasattr(dupa, "__code__"):
    #     print(dupa.__code__.co_varnames)

    # print(builtins.object)
    #
    #
    #
    # from editor.core.utils import parse_signatures
    #
    # # torch.add = "pog"
    # test = D()
    #
    # test.new_attribute = "value"
    #
    # setattr(test, "add", lambda: "hmm")
    #
    #
    # print(test.new_attribute)

    # print(parse_signatures(pygame.Vector2.__doc__, pygame.Vector2))

    # print(isinstance(eval("x"), type))

    # print(eval(str(pygame.Vector2).split('\'')[1]))

    # pygame.Vector2()

    # print(int.__invert__(2))