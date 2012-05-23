#!/usr/local/bin/python3

validPS1 = open('validPS1s.txt', mode='rt', encoding='utf=8')



def main():
	for ps1 in validPS1.readlines():
		print(ps1, end='')

if __name__ == "__main__": main()
	
