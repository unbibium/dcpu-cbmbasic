dcpu-cbmbasic
=============

Port of Commodore 64 BASIC and KERNAL to the DCPU-16

When I started looking into 0x10c and DCPU-16 programming, I noticed there were a few
KERNALs but no BASIC interpreter.  I considered writing my own, but I wasn't quite up
to the challenge of making a full-featured BASIC.  I'd probably lose interest after
doing the INPUT and PRINT commands or something.

I then considered looking at old 8-bit ports of BASIC.  I know a fair bit of 6502
assembly, and have reverse engineered a couple of Atari 2600 games in college.  So
I started looking online for online disassemblies of various BASICs.  As it turned out,
no BASIC was obviously the simplest.  I thought that Woz's Integer BASIC would be a
prime candidate, since I wouldn't have to muck around with floating point math.  But I 
wasn't as familiar with it as I was with the Atari 8-bit BASIC, or with Commodore 64 
BASIC V2.  I also knew that there was a Unix port of CBM BASIC, so it was possible
to decouple the BASIC interpreter from the KERNAL, or so I imagined.  Besides, Atari
BASIC was slow.  So, I looked up the CBM BASIC disassembly and got started.

I soon discovered that since the BASIC was included in the machine's ROM, it wasn't
as decoupled from teh KERNAL as I'd hoped.  But then I decided that a BASIC interpreter,
in and of itself, wasn't anything anyone would bother looking at for very long.  If I
could port the entire KERNAL and BASIC, I could make a DCPU-16 machine that behaved as
though it were another CBM-manufactured machine, like some kind of 16-bit Plus-4.

If your spaceship has this kernal, you will have a bad problem and you will not go to
space today.

Currently, this program will display the startup message, set up BASIC memory, and 
blink the cursor.  Behind the scenes, I have much of the floating point math package
working, since it turned out to be necessary to print the "38911 BASIC BYTES FREE"
message.  It's also using the C64 font's character layout.

I intend to port everything except the I/O.  Then I might add just enough I/O to make
it possible to save to disk.
