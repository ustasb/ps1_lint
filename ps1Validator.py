#!/usr/local/bin/python3

import re

# Colors listing from: https://wiki.archlinux.org/index.php/Color_Bash_Prompt
validColors = {
	'colorOff':		r'\e[0m',

	# Normal
	'black':		r'\e[0;30m',
	'red':			r'\e[0;31m',
	'green':		r'\e[0;32m',
	'yellow':		r'\e[0;33m',
	'blue':			r'\e[0;34m',
	'purple':		r'\e[0;35m',
	'cyan':			r'\e[0;36m',
	'white':		r'\e[0;37m',

	# Bold
	'BBlack':		r'\e[1;30m',
	'BRed':			r'\e[1;31m',
	'BGreen':		r'\e[1;32m',
	'BYellow':		r'\e[1;33m',
	'BBlue':		r'\e[1;34m',
	'BPurple':		r'\e[1;35m',
	'BCyan':		r'\e[1;36m',
	'BWhite':		r'\e[1;37m',

	# Underline
	'UBlack':		r'\e[4;30m',
	'URed':			r'\e[4;31m',
	'UGreen':		r'\e[4;32m',
	'UYellow':		r'\e[4;33m',
	'UBlue':		r'\e[4;34m',
	'UPurple':		r'\e[4;35m',
	'UCyan':		r'\e[4;36m',
	'UWhite':		r'\e[4;37m',

	# Background
	'BgBlack':		r'\e[40m',
	'BgRed':		r'\e[41m',
	'BgGreen':		r'\e[42m',
	'BgYellow':		r'\e[43m',
	'BgBlue':		r'\e[44m',
	'BgPurple':		r'\e[45m',
	'BgCyan':		r'\e[46m',
	'BgWhite':		r'\e[47m',

	# High Intensity
	'IBlack':		r'\e[0;90m',
	'IRed':			r'\e[0;91m',
	'IGreen':		r'\e[0;92m',
	'IYellow':		r'\e[0;93m',
	'IBlue':		r'\e[0;94m',
	'IPurple':		r'\e[0;95m',
	'ICyan':		r'\e[0;96m',
	'IWhite':		r'\e[0;97m',

	# Bold High Intensity
	'BIBlack':		r'\e[1;90m',
	'BIRed':		r'\e[1;91m',
	'BIGreen':		r'\e[1;92m',
	'BIYellow':		r'\e[1;93m',
	'BIBlue':		r'\e[1;94m',
	'BIPurple':		r'\e[1;95m',
	'BICyan':		r'\e[1;96m',
	'BIWhite':		r'\e[1;97m',

	# High Intensity Backgrounds
	'BgIBlack':		r'\e[0;100m',
	'BgIRed':		r'\e[0;101m',
	'BgIGreen':		r'\e[0;102m',
	'BgIYellow':	r'\e[0;103m',
	'BgIBlue':		r'\e[0;104m',
	'BgIPurple':	r'\e[10;95m',
	'BgICyan':		r'\e[0;106m',
	'BgIWhite':		r'\e[0;107m' 
}

colorRE = re.compile(r'\\e\[\d{,2};?\d{,3}m')

# Prompt Variables from: 
promptVars = {
	'bell':				r'\a',
	'date':				r'\d',
	#'strftime':			r'D{format}',
	'escape':			r'\e',
	'hostnameMin':		r'\h',
	'hostnameFull':		r'\H',
	'jobs':				r'\j',
	'deviceName':		r'\l',
	'newline':			r'\n',
	'carriageReturn':	r'\r',
	'shellName':		r'\s',
	'time24HH:MM:SS':	r'\t',
	'time12HH:MM:SS':	r'\T',
	'time12AMPM':		r'\@',
	'time24HH:MM':		r'\A',
	'username':			r'\u',
	'bashVersion':		r'\v',
	'bashRelease':		r'\V',
	'cwd':				r'\w',
	'basename$PWD':		r'\W',
	'historyNumber':	r'\!',
	'commandNumber':	r'\#',
	'effUID':			r'\$'
	#'octalValChr':		r'nnn',
	#'backslash':		r'\\',
}

def logIssue(ps1, pos, msg, err=True):
	print(ps1)
	print('{}^\n{}: {}'.format('-' * (pos - 1),'Error' if err else 'Warning', msg))
	if err:
		raise SystemExit(0)
	
def validateVar(ps1):
	for val in promptVars.values():
		if val == ps1[0:2]:
			print('Matched {}'.format(val))
			return 2 

	logIssue(ps1, 2, '{} is an invalid prompt variable'.format(ps1[0:2]))

def validateColor(ps1):
	return re.match(colorRE, ps1).group(0)

def validateEscape(ps1):
	l = len(ps1)
	i = 0

	while i < l:
		if ps1[i:i + 2] == r'\e':
			colorStr = validateColor(ps1[i:]) 
			i += len(colorStr)
			if ps1[i:i + 2] == r'\]':
				print('Matched {}'.format(ps1[:i + 2]))
				# Return the length of the escaped expression
				return i + 2
		else:
			pass
		
		i += 1

def parsePS1(ps1):
	pos = 0
	l = len(ps1)

	while pos < l:
		if ps1[pos] == '\\':
			if ps1[pos + 1] == r'[':
				pos += validateEscape(ps1[pos:])
			else:
				pos += validateVar(ps1[pos:])		
			continue
		else:
			print('{} is a valid character'.format(ps1[pos]))

		pos += 1

	print('{} is a valid PS1'.format(ps1))
	
def main():
	testPS1 = r'[\z@\h \W]\$'
	testPS12 = r'\[\e[1;32m\][\u@\h \W]\$\[\e[0m\]'
	parsePS1(testPS1)
	parsePS1(testPS12)

if __name__ == "__main__": main()
