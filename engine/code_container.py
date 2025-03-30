"""

Handles RestrictedPython and bytecode counting

"""

import marshal
from os import listdir
from os.path import isfile, join
import pickle
import re
from RestrictedPython import compile_restricted
from instrument import Instrument

class CodeContainer:
    def __init__(self, code):
        self.code = code

    @classmethod
    def create_from_directory_dict(cls, d, instrument=True):
        code = {}
        for file_name in d:
            module_name = file_name[:-3]
            compiled = compile_restricted(cls.preprocess(d[file_name]), file_name, 'exec') # TODO: Add preprocessing if we need to filter imports
            if instrument:
                code[module_name] = Instrument.instrument(compiled) # Instrument here
            else:
                code = compiled
        return cls(code)

    @classmethod
    def create_from_directory(cls, dir, instrument=True):
        files = [(f, join(dir, f)) for f in listdir(dir) if f[-3:] == '.py' and isfile(join(dir, f))]
        code = {}
        for file_name, location in files:
            with open(location) as f:
                code[file_name] = f.read()
        return cls.create_from_directory_dict(code, instrument)

    
    def to_bytes(self):
        packet = {}
        for key in self.code:
            packet[key] = marshal.dumps(self.code[key])

        return pickle.dumps(packet)

    @classmethod
    def from_bytes(cls, codebytes):
        packet = pickle.loads(codebytes)

        for key in packet:
            packet[key] = marshal.loads(packet[key])

        return cls(packet)

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.to_bytes())

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            return cls.from_bytes(cls.preprocess(f.read()))

    # TODO: Should be updated for my own imports (Not used atm)
    @classmethod
    def preprocess(cls, content):
        """
        Strips battlecode25.stubs imports from the code.

        It removes lines containing one of the following imports:
        - from battlecode25.stubs import *
        - from battlecode25.stubs import a, b, c

        The regular expression that is used also supports non-standard whitespace styles like the following:
        - from battlecode25.stubs import a,b,c
        - from  battlecode25.stubs  import  a,  b,  c

        Go to https://regex101.com/r/bhAqFE/6 to test the regular expression with custom input.
        """

        pattern = r'^([ \t]*)from([ \t]+)stubs([ \t]+)import([ \t]+)(\*|([a-zA-Z_]+([ \t]*),([ \t]*))*[a-zA-Z_]+)([ \t]*)$'

        # Replace all stub imports
        while True:
            match = re.search(pattern, content, re.MULTILINE)

            if match is None:
                break

            # Remove the match from the content
            start = match.start()
            end = match.end()
            content = content[0:start] + content[end:]

        return content

    def __getitem__(self, key):
        return self.code[key]

    def __contains__(self, key):
        return key in self.code