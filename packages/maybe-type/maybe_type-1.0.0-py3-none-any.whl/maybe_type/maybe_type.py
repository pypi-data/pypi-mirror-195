from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Union

A = TypeVar('A')
B = TypeVar('B')

@dataclass(frozen=True)
class Maybe(Generic[A]):
    '''A type that represents a value that may or may not be present.'''

    value: Union[A, None]

    def map(self, f: Callable[[A], B]) -> 'Maybe[B]':
        '''Applies a function, that doesn't return a Maybe, to the value, if it is present.'''

        if self.value is None:
            return Maybe(None)
        return Maybe(f(self.value))

    def bind(self, f: Callable[[A], 'Maybe[B]']) -> 'Maybe[B]':
        '''Applies a function, that returns a Maybe, to the value, if it is present.'''

        if self.value is None:
            return Maybe(None)
        return f(self.value)
    
    def extract(self) -> A:
        '''Extracts the value, if it is present, otherwise raise an exception.'''
        if self.value is None:
            raise Exception('Nothing to extract')
        return self.value

    def __repr__(self):
        return f'Maybe({self.value})'
    
def with_maybe(f):
    '''A decorator to make a function return it's result wrapped in a Maybe.'''

    def wrapper(*args, **kwargs):
        return Maybe(f(*args, **kwargs))
    return wrapper