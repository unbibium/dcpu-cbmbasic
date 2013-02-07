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
obviously the simplest.  I thought that Woz's Integer BASIC would
be a prime candidate, since I wouldn't have to muck around with
floating point math.  But I wasn't as familiar with it as I was
with the Atari 8-bit BASIC, or with Commodore 64 BASIC V2.  I also
knew that there was a Unix port of CBM BASIC, so it was possible
to decouple the BASIC interpreter from the KERNAL, or so I imagined.
Besides, Atari BASIC was slow.  So, I looked up the CBM BASIC
disassembly and got started.

I soon discovered that since the BASIC was included in the machine's
ROM, it wasn't as decoupled from teh KERNAL as I'd hoped.  But then
I decided that a BASIC interpreter, in and of itself, wasn't anything
anyone would bother looking at for very long.  If I could port the
entire KERNAL and BASIC, I could make a DCPU-16 machine that behaved
as though it were another CBM-manufactured machine, like some kind
of 16-bit Plus-4.

As much fun as it would be to pretend that a CBM-style kernal was
available in the 0x10c universe, there are a few things about the
hardware's design that make this direct port too awkward to be a
canonical product of an in-game corporation.  Everything about the
DCPU-16 and LEM-1802 design suggests an ASCII-based memory and
keyboard, while CBM machines use PETSCII to represent strings
internally, and a differently-ordered PETSCII to represent text
visible on the screen.  

Currently, this program will display the startup message, set up
BASIC memory, and allow keyboard input.  Behind the scenes, I have
much of the floating point math package working, since it turned
out to be necessary to print the "38911 BASIC BYTES FREE" message.
It's also using the C64 font's character layout, and the C64 palette.
There's a lot of untested BASIC code floating around in there too.

It does not actually execute any BASIC commands, and there are
some bugs that make the screen editor not quite useful anyway.

If your spaceship has this kernal, you will have a bad problem and
you will not go to space today.  There's a good chance this project
will never be as bug-free as the original product, though I'm
happy enough with how the floating point routines turned out, that
I think it may be possible to isolate and test them thoroughly,
and release them in a form useful to other DCPU-16 programmers.

If you want a reliable BASIC interpreter for your DCPU-16, a better
place to start might be to port another BASIC implementation to one
of the more venerable kernals, such as one of these:
http://www.ittybittycomputers.com/IttyBitty/TinyBasic/

