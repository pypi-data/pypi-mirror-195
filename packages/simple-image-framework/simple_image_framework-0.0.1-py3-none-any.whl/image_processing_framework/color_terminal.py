import sys 

def __inner_print( content : str, prefix : str = '' ): 
    if type(content) is not str: 
        raise TypeError('content must be a string') 
    if type(prefix) is not str: 
        raise TypeError('prefix must be a string') 
    print ( f'{prefix} {content}\x1b[0m', file = sys.stderr ) 

def debug( content : str ): 
    __inner_print(content, '\x1b[32;1m[-]') 

def info( content : str ): 
    __inner_print(content, '\x1b[34;1m[+]') 

def warn( content : str ): 
    __inner_print(content, '\x1b[33;1m[?]') 

def error( content : str ): 
    __inner_print(content, '\x1b[31;1m[!]') 