# PS1Lint

PS1Lint is a tool for finding flaws in PS1 strings. While the shell is forgiving, a poorly formatted PS1 can cause line wrapping issues.

## Usage

There are two ways to use PS1Lint.

1. Use the setup.py to install the module to your machine.

        python3 setup.py install

2. Pass the module a quoted PS1 argument.

        python3 ps1lint.py "\[\e[0;32m\]\u@\[\e[0;36m\]\h:\[\e[0;35m\] "

## PS1 Overview 

### Prompt Variables

See [here](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html) for a list of prompt variables.

### Colors

A color sequence affects everything after its declaration.
It must be escaped with `\[ ... \]` so that lines wrap properly.

Below are valid color sequences.

        \[\e[0m\] (a text reset--the same as \[\033[0m\])
        \[\e[1;43m\]
        \[\e[32m\]
        \[\e[4;32;44m\]
        \[\e[44;0;34m\]
        \[\e[34;4m\]

Color Codes [1]

        Text Attributes         Foreground Colors   Background Colors
        0 All Attributes Off    30 Black            40 Black
        1 Bold On               31 Red              41 Red
        4 Underscore On         32 Green            42 Green
        5 Blink On              33 Yellow           43 Yellow
        7 Reverse Video On      34 Blue             44 Blue
        8 Concealed On          35 Magenta          45 Magenta
                                36 Cyan             46 Cyan
                                37 White            47 White

### Cursor Movement

Cursor movement sequences must be escaped like color seqeunces.

Cursor Movement Seqeunces [1]

        \[\e[<Line>;<Column>H\]         Cursor Position
        \[\e[<Line>;<Column>f\]        
        \[\e[<Value>A\]                 Cursor Up
        \[\e[<Value>B\]                 Cursor Down
        \[\e[<Value>C\]                 Cursor Forward
        \[\e[<Value>D\]                 Cursor Backward
        \[\e[s\]                        Save Cursor Position
        \[\e[u\]                        Restore Cursor Position
        \[\e[2J\]                       Erase Display
        \[\e[K\]                        Erase Line
        \[\e[<Value>;...;<Value>m\]     Set Graphics Mode

### Shell Code and Variables

Shell code must be wrapped by either `` ` ... ` `` or `\$( ... )`.

## Resources 

* [PS1 overview](http://www.ibm.com/developerworks/linux/library/l-tip-prompt/)
* [List of prompt variables](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html)
* [Color codes and cursor movement seqeunces](http://ascii-table.com/ansi-escape-sequences.php)

Places to find new PS1s:
* [archlinux](https://bbs.archlinux.org/viewtopic.php?id=50885)
* [reddit](http://www.reddit.com/r/programming/comments/697cu/bash_users_what_do_you_have_for_your_ps1/)
* [stackoverflow](http://stackoverflow.com/questions/103857/what-is-your-favorite-bash-prompt)
