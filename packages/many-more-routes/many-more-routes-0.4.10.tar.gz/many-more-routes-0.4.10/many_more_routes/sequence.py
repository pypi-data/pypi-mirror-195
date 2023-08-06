from functools import wraps
import re
from typing import Any, Callable, Generator, Optional, TypeGuard



def mark_as_obsolete(hint: Optional[str] = '') -> Callable:
    def outer(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            print(f'Obsolete: Fuction "{__name__}.{func.__name__}" is will be removed in future versions ({hint})')
            return func(*args, **kwargs)
        
        return inner
    
    return outer
    

def to_str(value: int) -> str:
    ''' Converts a given integer to the corresponding string value '''
        
    a = chr(((value // 10000) // 26) % 26 + 65)
    b = chr((value // 10000) % 26 + 65)
    c = str(value % 10000).zfill(4)
    
    return a + b + c


def to_int(value: str) -> int:
    ''' Converts a given string to the corresponding integer value '''
    a = (ord(value[0]) - 65) * 260000
    b = (ord(value[1]) - 65) * 10000
    c = int(value[2:])

    return a + b + c
    

def is_valid_str(value: Any) -> TypeGuard[str]:
    ''' Checks if a given string is a valid sequence number '''
    return True if re.match("^[A-Z]{2}[0-9]{4}$", str(value)) and isinstance(value, str) else False


def is_valid_int(value: Any) -> TypeGuard[int]:
    ''' Checks if a given integer is a valid sequence number '''
    try:
        return value >= 0 and value < 6760000

    except TypeError:
        return False


@mark_as_obsolete('Use to_int and a range instead')
def increment(sequenceNumber: Optional[str] = None) -> str:
    '''Taked a route sequence number and incriments by one.
    >>> increment(None)
    'AA0001'
    >>> increment('AA0001')
    'AA0002'
    >>> increment('AA9999')
    'AB0001'
    >>> increment('ZZ9999')
    'AA0001'
    '''
    if sequenceNumber:
        _validate_seed(sequenceNumber)

    return _next(sequenceNumber)

@mark_as_obsolete('Use to_int and a range instead')
def generator(sequenceNumber: Optional[str] = None, n: Optional[int] = None) -> Generator:
    '''Returns a sequence generator. If n is not given it will loop infinitely'''
    if sequenceNumber:
        _validate_seed(sequenceNumber)

    return _generator(sequenceNumber, n)

def _validate_seed(sequenceNumber: str) -> None:
    '''Validate the input of a seed'''
    if len(sequenceNumber) != 6:
        raise ValueError('The sequence number has to be exatly 6 chars long')
    elif not sequenceNumber[:2].isalpha():
        raise ValueError('The first to chars of the sequence number has to be alpha numeric')
    elif not sequenceNumber[2:].isdigit():
        raise ValueError('The last four chars of the sequence number has to be numeric')

@mark_as_obsolete(hint='Use is_int_valid or is_str_valid instead')
def is_sequenceNumber_valid(sequenceNumber: str):
    ''' Returns True if seed is valid, else False. Can be used in a functional way
    to determine if a sequence number is valid or not, or to filter out route names that follows
    an different route name scheme in combination with the standard python filter function '''
    try:
        _validate_seed(sequenceNumber=sequenceNumber)
        return True

    except ValueError:
        return False

    except TypeError:
        return False

def _generator(sequenceNumber: Optional[str] = None, n: Optional[int] = None) -> Generator:
    '''Returns a sequence generator. If n is not given it will loop infinitely'''
    if sequenceNumber:
        yield sequenceNumber

    else:
        sequenceNumber = 'AA0001'

    if n:
        for _ in range(n - 1):
            sequenceNumber = _next(sequenceNumber)
            yield sequenceNumber

    else:
        while True:
            sequenceNumber = _next(sequenceNumber)
            yield sequenceNumber
        
def _next(sequenceNumber: Optional[str] = None) -> str:
    '''Taked a route sequence number and incriments by one.'''
    if sequenceNumber:
        alpha = sequenceNumber[:2]
        digit = sequenceNumber[2:]

        newDigit = _incrementDigit(digit)
        newAlpha = _incrementAlpha(alpha) if newDigit == increment()[2:] else alpha

        return newAlpha + newDigit

    else:
        return 'AA0001'

def _incrementAlpha(alpha: str) -> str:
    '''Takes a upper char string and increments as it's a number sequence.
    
    >>> incrementAlpha('AA')
    'AB'
    >>> incrementAlpha('ZZ')
    'AA'   
    '''
    assert any(map(lambda x: x.isalpha(), alpha))

    alphaArray = list(reversed(alpha))

    for n, char in enumerate(alphaArray):
        alphaArray[n] = chr((ord(char.upper())+1 - 65) % 26 + 65)

        if not char == 'Z':
            break

    return ''.join(reversed(alphaArray))

def _incrementDigit(alpha: str) -> str:
    ''' Takes a digit as string type and returns as equal length number as string.
        Number is reset to 1 when max number is reached.    
     '''
    assert any(map(lambda x: x.isdigit(), alpha))

    if all(map(lambda x: x  == '9', alpha)):
        return f'1'.zfill(len(alpha))

    else:
        return f'{int(alpha) + 1}'.zfill(len(alpha))


if __name__ == '__main__':
    import doctest
    doctest.testmod()