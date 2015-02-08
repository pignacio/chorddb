chorddb
=======

A guitar tablature parser

![chorddb in curses mode](./images/curses.png)

##Usage

```
chorddb parse <filename>           # Terminal mode
chorddb parse <filename> --curses  # Curses mode
```

###Additional options

```
-i/--instrument: choose instrument to parse tabs for. Should be one of
                 guitar, loog, ukelele
-t/--transpose: transpose the tablature the given number of steps
-c/--capo: simulates a capo on the instrument
```

