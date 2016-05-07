dcpu-cbmbasic
=============

Port of Commodore 64 BASIC and KERNAL to the DCPU-16.

To see it in action, watch the [YouTube demonstration][1].

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

Working features
----------------

* Screen editing
* PETSCII uppercase and lowercase character sets
* PETSCII control codes, and ways to type them on some keyboards:
   * Ctrl-1 through 8 and Ctrl-Shift-1 through 8 for colors
   * Ctrl-9 and Ctrl-0 for reverse on/off
   * Ctrl-= for HOME
   * Ctrl-+ for CLR
   * Ctrl-, for uppercase, Ctrl-. for lowercase.
   * Arrow keys
   * Ctrl-Letter works on 0x10co.de
* Immediate mode
* Program entry with line numbers
* BASIC commands: `GOTO`, `GOSUB`, `RETURN`, `PRINT`, `RUN`, `CLR`, `END`, `ON`, `NEW`,
                  `STOP`, `REM`, `IF`, `FOR`, `NEXT`, `DATA`, `READ`, `INPUT`, `GET`
* BASIC functions: `ABS`, `SGN`, `LEN`, `INT`, `LEFT$`, `RIGHT$`, `CHR$`, `ASC`, `EXP`,
                   `SIN`, `COS`, `LOG`, `SPC`, `MID$`, `STR$`
* BASIC keyword abbreviations with shifted second letters
* The `?` abbreviation for `PRINT`
* Expressions involving floating-point addition, subtraction,
  and multiplication to 32-bit accuracy.
* Floating point division to 16-bit accuracy, more for special
  cases like division by 5 or 3.
* Comparison operators for strings and variables, `NOT`, `AND`, and `OR`.
* String literals and concatenation.
* Allocating, setting, and retrieving all variable types:
  * String variables like `A$`
  * Float variables like `A`
  * Integer variables like `A%`
* Multi-dimensional arrays for all the above types
* Garbage collection
* Functions (`DEF FN`)

I've put some stub routines in unused commands for testing purposes:
* `LOAD` can be used to load a few small demo programs.  Use `LOAD`
  by itself to cycle through, or `LOAD"$"` for a directory.
  You can then use RUN to execute it, or LIST to see the source code.
* `VERIFY` will display a table that describes how program memory
  is currently being used.

Just about anything else won't work, and may even crash the machine.
Here's what's missing, in the rough order of when I'm going to add it:
* other functions (`VAL`, `POS`, `TAB`)
* Program storage (`LOAD`, `SAVE`, `VERIFY`)
* File access (`OPEN`, `CLOSE`, `GET`, `GET#`, `INPUT#`, `PRINT#`, `CMD`)
* 32-bit division, which will also fix the inaccurate power operator, `LOG`, and `EXP`.
* A stable memory map for `POKE`, `WAIT` and `PEEK` 
* More trigonometry (`TAN`, `ATN`)
* Special variables `ST`, `TI`, `TI$`
* a few DCPU-specific uses, like using `DIM` to allocate memory
  for the SPED-3.
* direct DCPU access with `SYS`, `USR()`

Additionally, the code needs to be optimized and cleaned up.
Many speed gains are possible, though it may never be as fast
as the original.  

This branch is an experiment to compile the program under
[paultech's assembler][6].

Resources
---------

* [Mapping the C64 by Sheldon Leemon][2], Compute! Publications 1984
* [C64 ROM disassembly "annotated"][3] -- there were no useful labels
  but there were a few useful comments and the JMP and JSR statements
  were linked.  (I had to save it offline for the links to work though.)
* [Create Your Own Version of Microsoft BASIC for 6502][4]
  This has some source code listings that explained things a little
  more thoroughly.  You'll see chunks of comments pasted from here
  in the source.
* ELIZA source code in BASIC:
  <http://everything2.com/title/ELIZA+source+code+in+BASIC>

DISCLAIMER
----------

If your spaceship has this kernal, you will have a bad problem and
you will not go to space today.  There's a good chance this project
will never be as bug-free as the original product, though it's
possible the program's components can be separated, depending on
how thoroughly useful it becomes.  The floating point routines can
probably be separated, and the BASIC can certainly be separated.
Screen I/O would probably be faster in an OS that wasn't trying
so hard to be a Commodore 64.

OTHER LINKS
-----------

Another promising interpreter for the DCPU-16 is [dcpu-admiral][5],
which aims to be more Python-like.

[1]: https://www.youtube.com/watch?v=om-JTv51JqI   "YouTube demonstration"
[2]: http://unusedino.de/ec64/technical/project64/mapping_c64.html
[3]: http://www.ffd2.com/fridge/docs/c64-diss.html "C64 ROM disassembly"
[4]: http://www.pagetable.com/?p=46
[5]: https://github.com/orlof/dcpu-admiral
[6]: https://github.com/paultech/DASM
