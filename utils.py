import random
import json
from re import I

bullet_char = "\u2022"

def generate_ascii_values():
    return [chr(num) for num in range(1, 256)]

# ----------------------------------- #
ascii_values = generate_ascii_values()
# ----------------------------------- #

def str_replace(st:str,index:int,char:str) -> str:
    """
    Takes a string and replaces the character present at index with given char
    and returns the modified string.

    :param st: str : string to be modified
    :param index: int: index at which replacement is to be done
    :param char: str : a character which should be replaced
    :return: str : modified string
    """
    lstr = list(st)
    lstr[index] = char
    return "".join(lstr)

def randint(a,b) -> int:
    return random.randint(a,b)

def random_KeyGen(keylen:int) -> list[int]:
    return random.sample(range(255),keylen)

def ciph(text: str, key: list) -> str:
    """
    Takes text and key, encrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : encrypted text
    """
    ciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) + key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - ((ascii_index * -1)%len(ascii_values))
        ciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return ciphered_text


def deciph(text: str, key: list) -> str:
    """
    Takes text and key, decrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : decrypted text
    """
    deciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) - key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - ((ascii_index * -1)%len(ascii_values))
        deciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return deciphered_text

def get_key(strval:str) -> list[int]:
    """
    takes string, tries to decode using json, converts to list
    checks if all the elements in the list are integers or not, if not, then tries to convert the characters to integer using ord().
    if it fails to so.. then entire string will be taken as string key, and each character of this string will be converted to integer and returns as list

    :param strval: str
    :return: list[int]
    """
    k = []
    try:
        k = json.loads(strval)
        if type(k) != type(list()):
            raise json.decoder.JSONDecodeError("not int","",0)
        elif any(type(x) != type(int()) for x in k):
            raise json.decoder.JSONDecodeError("not int","",0)
    except json.decoder.JSONDecodeError:
        k = [ord(x) for x in strval]
    return k

def to_even(n):
    """
    Takes an integer n, and returns the closest even value from n
    
    return: int - closest even number
    """
    if n%2==0:
        return n
    else:
        return n-1

def find_in(lst:list,val):
    """
    Finds the given value in list and returns the index of first occurrence of value
    """
    for i,item in enumerate(lst):
        if item == val:
            return i
    return -1