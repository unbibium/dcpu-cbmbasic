dcpu-cbmbasic
=============

Port of Commodore 64 BASIC and KERNAL to the DCPU-16

When I started looking into 0x10c and DCPU-16 programming, I noticed
there were a few KERNALs but no BASIC interpreter.  I considered
writing my own, but I wasn't quite up to the challenge of making a
full-featured BASIC.  I'd probably lose interest after doing the
INPUT and PRINT commands or something.

I then considered looking at old 8-bit ports of BASIC.  I know a
fair bit of 6502 assembly, and have reverse engineered a couple of
Atari 2600 games in college.  So I started looking online for online
disassemblies of various BASICs.  As it turned out, no BASIC was
obviously the simplest, but CBM BASIC seemed to have the fewest
pitfalls.

As I progressed, I realized that if I could port the entire KERNAL
and BASIC, I could make a DCPU-16 machine that behaved as though
it were another CBM-manufactured machine, like some kind of 16-bit
Plus-4.

As much fun as it would be to pretend that a CBM-style kernal was
available in the 0x10c universe, there are a few things about the
hardware's design that make this direct port too awkward to be a
canonical product of an in-game corporation.  Everything about the
DCPU-16 and LEM-1802 design suggests an ASCII-based memory and
keyboard, while CBM machines use PETSCII to represent strings
internally, and a differently-ordered PETSCII to represent text
visible on the screen.  I've made this work with a custom font,
but it means that this won't work with any text-mode emulators,
if they exist.  

A substantial fraction of the features work, but it's not complete
yet.  Here's a mostly-complete list of things that will work
mostly like they do on the C64:

* Screen editing
* Program entry
* Immediate mode
* BASIC commands: GOTO, GOSUB, RETURN, PRINT, RUN, CLR, END, ON,
                  NEW, STOP, REM, IF, FOR, NEXT, DATA, READ, INPUT
* BASIC functions: ABS, SGN, LEN, INT, LEFT$, RIGHT$, CHR$()
* BASIC keyword abbreviations with shifted second letters
* The ? abbreviation for PRINT
* Expressions involving floating-point addition, subtraction,
  and multiplication to 32-bit accuracy.
* Floating point division to 16-bit accuracy, more for special
  cases like division by 5 or 3.
* Comparison operators, NOT, AND, and OR.
* String literals and concatenation.
* Allocating, setting, and retrieving string variables like A$
* Allocating, setting, and retrieving float variables like A

Just about anything else won't work, and may even crash the machine.
Here's what's missing, in the rough order of when I'm going to add it:
* the functions MID$, ASC, and VAL
* Arrays
* Program storage (LOAD, SAVE, VERIFY)
* Garbage collection
* File access (OPEN, CLOSE, GET, GET#, INPUT#, PRINT#, CMD)
* Exponents and logarithms (EXP, LOG, ^ operator)
* POKE and PEEK (I'll need to stabilize the memory map first)
* Trigonometry (SIN, COS, TAN, ATN)
* Special variables ST, TI, TI$

Additionally, the code needs to be optimized and cleaned up.
Many speed gains are possible, though it may never be as fast
as the original.  

This program was developed using the DCPU toolchain at
http://dcputoolcha.in/ -- mostly the command-line tools,
since the DT IDE crashes on my PC and won't compile on my Mac.
This program will run on any emulator that handles interrupts
properly, even 0x10co.de.

I've used the following online resources to make this work:

* Mapping the C64 by Sheldon Leemon, Compute! Publications 1984
   <http://unusedino.de/ec64/technical/project64/mapping_c64.html>
* C64 ROM disassembly "annotated" -- there were no useful labels
  but there were a few useful comments and the JMP and JSR statements
  were linked.  (I had to save it offline for the links to work though.)
  <http://www.ffd2.com/fridge/docs/c64-diss.html>
* Create Your Own Version of Microsoft BASIC for 6502
  This has some source code listings that explained things a little
  more thoroughly.
  <http://www.pagetable.com/?p=46>

DISCLAIMER:

If your spaceship has this kernal, you will have a bad problem and
you will not go to space today.  There's a good chance this project
will never be as bug-free as the original product, though it's
possible the program's components can be separated, depending on
how thoroughly useful it becomes.  The floating point routines can
probably be separated, and the BASIC can certainly be separated
from the KERNAL.

Another promising interpreter for the DCPU-16 is dcpu-admiral,
which aims to be more Python-like:
* <https://github.com/r4d2/dcpu-admiral>


