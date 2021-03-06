# PS1Lint

- Initial release: 06/03/2012
- Author: [Brian Ustas](http://brianustas.com)

PS1Lint is a tool for finding flaws in Bash PS1 strings. While Bash is forgiving, a poorly formatted PS1 can cause line wrapping issues.

## Usage

There are two ways to use PS1Lint.

1. Use setup.py to install the module to your machine.

        python3 setup.py install

        # someFile.py
        import ps1Lint
        ps1Lint.parse(r'\u@\h\n\$ ')  # Returns a boolean.

2. Pass the module a single quoted (prevents shell expansion) PS1 argument.

        ps1Lint.py [-h] bashPS1

        # e.g.
        python3 ps1Lint.py '\[\e[0;32m\]\u@\[\e[0;36m\]\h:\[\e[0;35m\] '

## Quick PS1 Overview

### Prompt Variables

See [here](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html) for a list of prompt variables.

Note: \a and \r are not tolerated as they cause line wrapping issues.

### Colors

A color sequence affects everything after its declaration. It must be escaped with `\[ ... \]` so that lines wrap properly.

Below are valid escaped color sequences:

        \[\e[0m\]  # (a text reset--the same as \[\033[0m\])
        \[\e[1;43m\]
        \[\e[32m\]
        \[\e[4;32;44m\]
        \[\e[44;0;34m\]
        \[\e[34;4m\]

Color Codes [1]:

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

Cursor movement sequences must be escaped like color sequences.

Escaped Cursor Movement Sequences [1]:

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

### Shell Expansions

Shell code must be wrapped in either `` ` ... ` `` or `\$( ... )`.

        `echo thing | sed 's/thing/ding/'`
        \$(date +%H:%M)

Shell variables must be wrapped in `${ ... }` or solely prefixed with `$`.

        \[${blue}\]@\[${purple}\]
        \[$orange\]\u\[$blue\]\h

### Things to Avoid

Only color or cursor movement sequences should be put inside `\[ ... \]`. Do not do this as PS1Lint will complain:

        \[\n[$PWD]\] \n\[\033[1;34m\]\u  # Causes line wrapping issues.

Instead, change the PS1 to this:

        \n[$PWD] \n\[\033[1;34m\]\u

## Resources

* [PS1 overview](http://www.ibm.com/developerworks/linux/library/l-tip-prompt/)
* [\[1\] Cursor movement sequences and color codes](http://ascii-table.com/ansi-escape-sequences.php)

Looking for a new PS1?
* [archlinux](https://bbs.archlinux.org/viewtopic.php?id=50885)
* [reddit](http://www.reddit.com/r/programming/comments/697cu/bash_users_what_do_you_have_for_your_ps1/)
* [stackoverflow](http://stackoverflow.com/questions/103857/what-is-your-favorite-bash-prompt)
