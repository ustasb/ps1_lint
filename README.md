# PS1Lint

PS1Lint is a tool for finding flaws in PS1 strings. While the shell is forgiving, a poorly formatted PS1 can cause line wrapping issues.

## Usage

There are two ways to use PS1Lint.

1. Use the setup.py to install the module to your machine.

        python3 setup.py install

2. Pass the module a quoted PS1 argument.

        python3 ps1lint.py "\[\e[0;32m\]\u@\[\e[0;36m\]\h:\[\e[0;35m\] "

## Resources 

* [PS1 overview](http://www.ibm.com/developerworks/linux/library/l-tip-prompt/)
* [List of prompt variables](http://www.gnu.org/software/bash/manual/html_node/Printing-a-Prompt.html)
* [Color codes and cursor movement seqeunces](http://ascii-table.com/ansi-escape-sequences.php)

Places to find new PS1s (be sure to validate them first!):
* [archlinux](https://bbs.archlinux.org/viewtopic.php?id=50885)
* [reddit](http://www.reddit.com/r/programming/comments/697cu/bash_users_what_do_you_have_for_your_ps1/)
* [stackoverflow](http://stackoverflow.com/questions/103857/what-is-your-favorite-bash-prompt)
