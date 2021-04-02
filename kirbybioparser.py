'''
A python file to parse `kirbybio` files
'''

import os
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
        raise FileNotFoundError("This .kirbybio file does not exist")
    returnValue = KirbyBio()

    content = open(filename, 'r').read().splitlines()
    returnValue.filename = filename
    returnValue.fileContents = '\n'.join(content)

    # check if required data is there
    if "\\NAME\\" not in content:
        raise NoName("{file} has not \\NAME\\ property.".format(file=filename))
    if "\\BIO\\" not in content:
        raise NoBio("{file} has no \\BIO\\ property.".format(file=filename))
    if "\\FIRSTAPPEAR\\" not in content:
        raise NoAppearance("{file} has no \\FIRSTAPPEAR\\ property.".format(file=filename))

    # quote is optional
    if "\\QUOTE\\" in content:
        quoteInd = content.index("\\QUOTE\\")

        returnValue.quote = content[quoteInd+1]
    
    # bio
    bioInd = content.index("\\BIO\\")

    bioContents = ""
    inDoubleBackslash = False
    backSlashContent = ""
    for parseBio in content[bioInd+1]:
        if parseBio == "\\":
            inDoubleBackslash = not inDoubleBackslash
            if not inDoubleBackslash:
                backSlashContent = ""
            continue
        if not inDoubleBackslash:
            bioContents += parseBio
        else:
            backSlashContent += parseBio
        if backSlashContent == "NLN":
            bioContents += "\n"

        returnValue.bio = bioContents

    # name
    nameInd = content.index("\\NAME\\")
    returnValue.name = content[nameInd+1]

    # first appear
    firstAppear = content.index("\\FIRSTAPPEAR\\")
    returnValue.firstappear = content[firstAppear+1]

    # type
    if "\\TYPE\\" in content:
        ctype = content.index("\\TYPE\\")
        returnValue.char_type = [int(x) for x in content[ctype+1]]
    

    # get folder
    folder = filename.split("/")[-2]
    returnValue.folder = folder
    return returnValue


def dump(bio:KirbyBio, filename):
    '''Will completely overwrite the existing one'''

    with open(filename, 'w') as dump:
        if bio.bio != "":
            dump.write("\\BIO\\\n")
            dump.write(bio.bio + "\n")
        
        if bio.quote != "":
            dump.write("\\QUOTE\\\n")

            bioFormatted = bio.quote.replace("\\NLN\\", '\n')
            dump.write(bioFormatted)

# testing
if __name__ == "__main__":

    print(load("./characters/Template/bio.kirbybio"))
