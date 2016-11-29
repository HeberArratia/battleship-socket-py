import socket
import time

class bcolors:
	PINK = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

s = socket.socket()
s.connect(('127.0.0.1',9991))

#pedimos al usuario que ingrese un dato
print bcolors.YELLOW + "esperando que ingrese un contrincante..." + bcolors.ENDC
# permite jugar
while True:
	if s.recv(1024) == "yes":
		print bcolors.OKGREEN + "Listo para jugar" + bcolors.ENDC
		msg = bcolors.OKGREEN + "Escribe aqui tu nombre > " + bcolors.ENDC
		name = raw_input(msg)
		# enviamos los datos al servidor
		s.send(name)
		print bcolors.YELLOW + "esperando nombre de contrincante..." + bcolors.ENDC
		break
time.sleep(1)
print s.recv(1024)
while True:
	isturn = s.recv(1024)
	time.sleep(1)
	if  isturn == "turn":
		print s.recv(1024)
		guess_row = raw_input("Ingresa un letra: ")
		guess_col = raw_input("Ingresa un numero: ")
		s.send(guess_row)
		s.send(guess_col)
		result = s.recv(1024)
		if result == "Ganastee!!":
			print bcolors.OKGREEN + result + bcolors.ENDC
			break
		else:
			print bcolors.PINK + result + bcolors.ENDC
	elif isturn == "Perdiste!!":
		print bcolors.RED + "Perdiste!!" + bcolors.ENDC
		break
	else:
		result = s.recv(1024)
		if result == "Ganastee!!":
			print bcolors.OKGREEN + result + bcolors.ENDC
			break
		else:
			print result 
s.close()

