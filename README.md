# PS1Lint

PS1Lint is a tool for finding flaws in PS1 strings. While the shell is forgiving, a poorly formatted PS1 can cause line wrapping issues.

## Usage

There are two ways to use PS1Lint.

1. Use the setup.py to install the module to your machine.

        python3 setup.py install

2. Pass the module a quoted PS1 argument.

        python3 ps1lint.py "\[\e[0;32m\]\u@\[\e[0;36m\]\h:\[\e[0;35m\] "

## PS1 Overview 

See [here](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html) for a list of valid prompt variables.

### Colors

A color sequence affects everything after its declaration.
It must be escaped with \[ ... \] so that lines wrap properly.

Below are valid color sequences:
    \[\e[0m\] (a text reset--the same as \[\033[0m\])
    \[\e[1;43m\]
    \[\e[32m\]
    \[\e[4;32;44m\]
    \[\e[44;0;34m\]
    \[\e[34;4m\]

Color Codes [1]
        Text attributes         Foreground colors   Background colors
        0 All attributes off    30 Black            40 Black
        1 Bold oni              31 Red              41 Red
        4 Underscore            32 Green            42 Green
        5 Blink on              33 Yellow           43 Yellow
        7 Reverse video on      34 Blue             44 Blue
        8 Concealed on          35 Magenta          45 Magenta
                                36 Cyan             46 Cyan
                                37 White            47 White

## Resources 

* [PS1 overview](http://www.ibm.com/developerworks/linux/library/l-tip-prompt/)
* [List of prompt variables](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html)
* [Color codes and cursor movement seqeunces](http://ascii-table.com/ansi-escape-sequences.php)

Places to find new PS1s:
* [archlinux](https://bbs.archlinux.org/viewtopic.php?id=50885)
* [reddit](http://www.reddit.com/r/programming/comments/697cu/bash_users_what_do_you_have_for_your_ps1/)
* [stackoverflow](http://stackoverflow.com/questions/103857/what-is-your-favorite-bash-prompt)
