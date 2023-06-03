

import inspect

class Myclass():
    def __init__(self):
        self._first_caller_name = None
        self._first_caller_kwargs = None

    def calc_foo(self, a=None, b=None):

        """ repeated 3 line codes """
        this_func_kwargs = {key: value for key, value in locals().items() if key != 'self'}
        this_func_name = inspect.stack()[0][3]
        self._set_first_caller_attributes(this_func_name, this_func_kwargs)

        if a is None:
            a = 0
        if b is None:
            b = 0
        return a + b

    def calc_bar(self, a=None, b=None):

        """ repeated 3 line codes """
        this_func_kwargs = {key: value for key, value in locals().items() if key != 'self'}
        this_func_name = inspect.stack()[0][3]
        self._set_first_caller_attributes(this_func_name, this_func_kwargs)

        return self.calc_foo(a=a, b=b) * 10

    def _set_first_caller_attributes(self, func_name, func_kwargs):
        self._first_caller_name = func_name
        self._first_caller_kwargs = func_kwargs


instance = Myclass()
print(instance.calc_bar(2, 3))
print(instance._first_caller_kwargs)

instance2 = Myclass()
print(instance2.calc_bar(None, 3))
print(instance2._first_caller_kwargs)