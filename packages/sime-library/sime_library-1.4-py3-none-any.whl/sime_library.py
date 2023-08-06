import time
from colorama import Fore
import ctypes
import pyshorteners
import random
import time
class SimeLibraryError(Exception):
    pass


def sleep(t: float) -> None:
    try:
        time.sleep(t)
    except Exception:
        raise SimeLibraryError("Error occurred during sleep")


def color(color_name: str) -> str:
    try:
        return getattr(Fore, color_name.upper())
    except AttributeError:
        raise SimeLibraryError(f"{color_name} is not a valid color name")


def set_window_title(title: str) -> None:
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except Exception:
        raise SimeLibraryError("Error occurred during setting window title")


def spaces(n: int) -> None:
    try:
        for i in range(n):
            print()
    except Exception:
        raise SimeLibraryError("Error occurred during adding spaces")

def shorten_url(url: str) -> str:
    try:
        s = pyshorteners.Shortener()
        return str(s.tinyurl.short(url))
    except Exception:
        raise SimeLibraryError("Error occurred during shortening URL")
def generatePass(length: int) -> int:
    krack = [x for x in range(33, 127)]
    word = ""
    for x in range(length):
        charter = random.choice(krack)
        word += charter
    return word
def tempConv(from_temp: str, to_temp: str, temp: float) -> float:
    if from_temp == "c" and to_temp == "f":
        return temp * 9/5 + 32
    elif from_temp == "f" and to_temp == "c":
        return (temp - 32) * 5/9
    else:
        raise SimeLibraryError("These settings are not supported by the library.")
def checkPassword(password: str) -> bool:
    lenght = False
    letters = False
    numbers = False
    if len(password) >= 8:
        lenght = True
    for x in password:
        if x.isalpha():
            letters = True
        elif x.isdigit():
            numbers = True
    if lenght and letters and numbers:
        return True
    else:
        return False