## PS1Lint

PS1Lint is a tool for finding flaws in PS1 strings. While the shell is forgiving, a poorly formatted PS1 can cause line wrapping issues.

### Usage

There are two ways to use PS1Lint.

1. Use the setup.py to install the module to your machine.
    python3 setup.py install

2. Pass the module a quoted PS1 argument.
    python3 ps1lint.py "\[\e[0;32m\]\u@\[\e[0;36m\]\h:\[\e[0;35m\] "
