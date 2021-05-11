'''
A python file to parse `kirbybio` files
Kirbybio files were complete garbage what was I thinking
'''

import os
import json
from enum import IntEnum

class KirbyBio:

    quote = None
    filename = None
    fileContents = None
    bio = None
    firstappear = None
    name = None
    char_type = None
    folder = None

    def __str__(self):
        f = f"{self.name}\n"
        if self.quote:
            f += f"\t> {self.quote}\n"
        if self.firstappear:
            f += f"\t(from {self.firstappear})\n"
        if self.char_type:
            types = ', '.join([CharacterType(x).name for x in self.char_type])
            f += f"\tStatus: {types}\n"
        
        f += f"BIO:\n{self.bio} "
        return f

class CharacterType(IntEnum):

    Enemy    = 0
    Helper   = 1
    Boss     = 2
    Miniboss = 3
    Ally     = 4

class KirbyBioParserException(Exception):
    pass

class NoBio(KirbyBioParserException):
    '''Gets raised when the specified file does not have a bio.'''

class NoName(KirbyBioParserException):
    '''Gets raised when the specified file does not contain a name.'''

class NoAppearance(KirbyBioParserException):
    '''Gets raised when the specified file does not have a specified first appearance.'''


def load(filename) -> KirbyBio:
    if not os.path.exists(filename):
        raise FileNotFoundError("This kirby bio file does not exist")
    returnValue = KirbyBio()

    content:dict = json.load(open(filename))

    returnValue.bio = content["_bio"]
    returnValue.firstappear = content["_firstAppear"]
    returnValue.name = content["_name"]

    if "_type" in  content.keys():
        if type(content["_type"]) == int:
            types = [content["_type"],]
        else:
            types = content["_type"]

        returnValue.char_type = types
    if "_quote" in content.keys():
        returnValue.quote = content["_quote"]

    return returnValue