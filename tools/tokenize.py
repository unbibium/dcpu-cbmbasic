#!/opt/local/bin/python3.2
#
# Tokenize a text file into a BASIC file.
#
# There is stub code here for compiling to a Commodore 64
# BASIC file, and ro a binary DCPU BASIC file, but from the
# command line you can only create a listing for dtasm.
#
# see the other script files for how this is integrated
# into DCPU-BASIC Alpha's LOAD statement.

import sys, os
import re
from struct import *

"""text tokenizer"""

maxline=70

colordict = {
    '0': 0x90, '1': 0x05, '2': 0x1c, '3': 0x9f, 
    '4': 0x9c, '5': 0x1E, '6': 0x1F, '7': 0x9E,
    '8': 0x81, '9': 0x95, 'A': 0x96, 'B': 0x97, 
    'C': 0x98, 'D': 0x99, 'E': 0x9a, 'F': 0x9b,
    'I': 0x12, 'J': 0x92, 'Z': 147,
    'U': 0x91, 'V': 0x11, 'L': 0x9D, 'K': 0x1d,
}

keydict = {
    0x80: 'END',
    0x81: 'FOR',
    0x82: 'NEXT',
    0x83: 'DATA',
    0x84: 'INPUTN',
    0x85: 'INPUT',
    0x86: 'DIM',
    0x87: 'READ',
    0x88: 'LET',
    0x89: 'GOTO',
    0x8a: 'RUN',
    0x8b: 'IF',
    0x8c: 'RESTORE',
    0x8d: 'GOSUB',
    0x8e: 'RETURN',
    0x8f: 'REM',
    0x90: 'STOP',
    0x91: 'ON',
    0x92: 'WAIT',
    0x93: 'LOAD',
    0x94: 'SAVE',
    0x95: 'VERIFY',
    0x96: 'DEF',
    0x97: 'POKE',
    0x98: 'PRINT#',
    0x99: 'PRINT',
    0x9A: 'CONT',
    0x9B: 'LIST',
    0x9C: 'CLR',
    0x9D: 'CMD',
    0x9E: 'SYS',
    0x9f: 'OPEN',
    0xa0: 'CLOSE',
    0xa1: 'GET',
    0xa2: 'NEW',
    0xa3: 'TAB(',
    0xa4: 'TO',
    0xa5: 'FN',
    0xa6: 'SPC(',
    0xa7: 'THEN',
    0xa8: 'NOT',
    0xa9: 'STEP',
    0xaa: '+',
    0xab: '-',
    0xac: '*',
    0xad: '/',
    0xae: '^',
    0xaf: 'AND',
    0xb0: 'OR',
    0xb1: '>',
    0xb2: '=',
    0xb3: '<',
    0xb4: 'SGN',
    0xb5: 'INT',
    0xb6: 'ABS',
    0xb7: 'USR',
    0xb8: 'FRE',
    0xb9: 'POS',
    0xba: 'SQR',
    0xbb: 'RND',
    0xbc: 'LOG',
    0xbd: 'EXP',
    0xbe: 'COS',
    0xbf: 'SIN',
    0xc0: 'TAN',
    0xc1: 'ATN',
    0xc2: 'PEEK',
    0xc3: 'LEN',
    0xc4: 'STR$',
    0xc5: 'VAL',
    0xc6: 'ASC',
    0xc7: 'CHR$',
    0xc8: 'LEFT$',
    0xc9: 'RIGHT$',
    0xca: 'MID$',
    0xcb: 'GO',
}

keywords = list(keydict.items())
keywords.sort()

def qplop(bline):
    "render a line of program text"
    s = []
    for b in bline:
        if b<128 or quotemode:
            if b == 34:
                quotemode = not quotemode
            s.append(chr(b))
    return "".join(s)

def tokenize(line):
    "tokenize a line of program text"
    b = list()
    # TODO: break line into bytes
    datamode = comment = quotemode = False
    while len(line):
        if quotemode and line[:1] == '~':
            try:
                line = chr(colordict[line[1:2].upper()]) + line[2:]
            except:
                line = chr(255)
        if line[:1] == '"':  #quotes
            quotemode = not quotemode
        if line[:1] == ':' and not quotemode: 
            datamode = False
        if quotemode or comment or datamode:
            b.append(ord(line[:1]))
            line = line[1:]
            continue
        if line[:1] == '?':
            b.append(0x99)
            line = line[1:]
            continue
        for token, keyword in keywords:
            if line[:len(keyword)] == keyword:
                b.append(token)
                line = line[len(keyword):]
                if keyword == 'REM':
                    comment=True
                elif keyword == 'DATA':
                    datamode = True
                break
        else:
            b.append(ord(line[:1]))
            line = line[1:]
    return b

class PRG:
    "program object"

    line_re = re.compile(r'^\s*(\d+)\s*(.*)$')

    def __init__(self, program, filename="DEMO"):
        self.label = os.path.split(filename)[-1].split('.')[0].upper()
        print(self.label)
        if not hasattr(self, 'origin'):
            self.origin = 0x0801
        self.ln_struct = Struct(self.__class__.structs['line_number'])
        self.ch_struct = Struct(self.__class__.structs['text_character'])
        self.lines = {}
        if type(program) is str:
            self.load_text(program)
        else:
            raise TypeError

    def load_text(self, text):
        if type(text) is not str:
            raise TypeError
        for line in text.split("\n"):
            parsed_line = self.parse_text(line)
            if parsed_line:
                self.add_line(*parsed_line)

    def add_line(self, lnum, statements):
        if lnum > 63999:
            raise ValueError("invalid line number")
        self.lines[lnum] = statements

    def parse_text(self, line):
        m = PRG.line_re.match(line)
        if m:
            lnum, statements = (m.groups())
            return (int(lnum), tokenize(statements))
        else:
            return None

    def write_line(self, f, loc, lnum, line):
        linesize = self.ln_struct.size * 2 + self.ch_struct.size * (len(line)+1)
        linesize /= self.__class__.wordsize
        f.write(self.ln_struct.pack(loc+linesize))
        f.write(self.ln_struct.pack(lnum))
        for b in line:
            f.write(self.ch_struct.pack(b))
        f.write(self.ch_struct.pack(0))
        return loc + linesize

    def write_to(self, f):
        line_numbers = list(self.lines.keys())
        line_numbers.sort()
        loc = self.origin
        self._write_preamble(f)
        for lnum in line_numbers:
            loc = self.write_line(f, loc, lnum, self.lines[lnum])
        self._write_eof(f)

    def _write_preamble(self, f):
        return 0
    
    def _write_eof(self, f):
        f.write(self.ln_struct.pack(0))

class CBM_PRG(PRG):
    def _write_preamble(self, f):
        f.write(bytes((1,8)))
        return 2

    wordsize = 1
    structs = {
        'line_number': '<H',
        'text_character': 'B'
    }

class DCPU_PRG(PRG):
    def __init__(self, p, **kw):
        self.origin = 0
        super(DCPU_PRG, self).__init__(p, **kw)


    wordsize = 2
    structs = {
        'line_number': '>H',
        'text_character': '>H'
    }

class DCPU_DAT(DCPU_PRG):
    def _write_preamble(self, f):
        f.write((':%s\n' % self.label).encode('us-ascii'))
        f.write('; DCPU-BASIC binary listing\n;\n'.encode('us-ascii'))

    def _write_eof(self, f):
        f.write((' DAT 0\n:%s_END\n DAT 0\n DAT "%s", 0\n' % (self.label, self.label)).encode('us-ascii'))

    def write_line(self, fo, loc, lnum, line):
        linesize = self.ln_struct.size * 2 + self.ch_struct.size * (len(line)+1)
        linesize /= self.__class__.wordsize
        s = " DAT BASICMEM+%d, %d\n" % (loc+linesize, lnum)
        fo.write(s.encode('us-ascii'))
        s = ''
        for b in line+[0]:
                if len(s) == 0:
                    s = ' DAT '
                #if b>0xfff0:
                #    s += "%d," % (b-65536)
                if b>31 and b<127 and b not in (34,92,58):
                    if s[-2:] == '",':
                        s = s[:-2] + '%c",' % b
                    else:
                        s += '"%c",' % b
                elif b<64:
                    s += "%d," % b
                else:
                    s += "0x%x," % b
                if len(s) > maxline:
                    fo.write((s[:-1] + '\n').encode('us-ascii'));
                    s=""
        fo.write((s[:-1] + '\n').encode('us-ascii'));
        
        return loc + linesize

def convert(source, dest, fromclass=DCPU_DAT):
        with open(source,'r') as f:
            p = fromclass(f.read(), filename=source)
        with open(dest,'wb') as fo:
            p.write_to(fo)

    
# stand-alone instructions
if __name__=='__main__':
    if len(sys.argv) < 2:
        print( "usage: ", sys.argv[0], " infile [outfile]")
    elif len(sys.argv) == 2:
        convert(sys.argv[1], sys.argv[1]+'.dprg')
    elif len(sys.argv) == 3:
        convert(sys.argv[1], sys.argv[2])
    else:
        print("error")


#autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class,with coutwords=return,pass
#tabstop=4
#shiftwidth=4
#expandtab
#autoindent
#softtabstop=4

