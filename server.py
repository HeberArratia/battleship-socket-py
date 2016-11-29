import socket
import threading
from random import randint
import string
import sys

# Colores y estilos para salida de texto por pantalla
class bcolors:
	PINK = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

#Clase Board: Corresponde al juego en si, el tablero con sus barcos
class Board(object):
	#ingresamos cantidad de filas (r), columnas (c) y barcos en tablero (q)
	def __init__(self, r, c, q):
		#tablero de juego
		self.board = []
		#barcos en el tablero
		self.boats = []
		#iniciamos metodos necesarios
		self.loadBoard(r, c)
		self.fillBoats(q)

	# agrega filas y columnas al tablero
	def loadBoard(self, r, c):
		# lleno mi tablero con r:filas y c:columnas
		circle = u"\u25CB" 
		circle = circle.encode('utf-8')
		for x in range(r):
			self.board.append([circle] * c)

	# muestra el tablero
	def printBoard(self):
		# agregar numeros para cada columna
		headBoard =  "  "
		for x in range(len(self.board[0])):
			headBoard =  headBoard + str(x + 1) + " "

		#Obtener abecedario para lado del tablero
		abc = list(string.uppercase)
		count = 0;
		outp = ""
		# almacenamos el tablero completo
		for row in self.board:
		# eliminamos comillas y comas, concatena solo string con " ".join
		# agregamos tambien una letra por cada fila
			outp = outp + bcolors.OKGREEN + abc[count] + bcolors.PINK + " " + " ".join(row) + bcolors.ENDC + "\n"
			count = count + 1
		# retornamos el tablero
		return headBoard + "\n" + outp

	# Cargamos cada uno de los barcos (con random) en el tablero
	# parametro quan: cantidad de barcos a cargar en tablero
	def fillBoats(self, quan):
		# obtengo cantidad de filas y columnas del tablero
		nrow = len(self.board)
		ncol = len(self.board[0])
		# creo mi tabla de barcos del mismo tamano que el tablero
		for x in range(nrow):
			self.boats.append(["0"] * ncol)
		# generamos posiciones random
		# la cantidad de veces requerida por quan
		count = 0
		while (count < quan):
			ship_row = randint(0, nrow - 1)
			ship_col = randint(0, ncol - 1)
			# si no existe barco en esta posicion, se crea
			if self.boats[ship_row][ship_col] != "1":
				# los barcos se representan con un "1"
				self.boats[ship_row][ship_col] = "1"
				count = count + 1

	# muestra los barcos en el tablero
	def printBoats(self):
		for row in self.boats:
		# eliminamos comillas y comas, concatena solo string
			print " ".join(row)

	# metodo que permite jugar un turno
	def play(self, r, col):
		# convertir letra de fila a numero (para poder jugar)
		di = dict(zip(string.letters,[ord(c)%32 for c in string.letters]))
		r = di[str(r)] - 1
		col = col - 1 
		# si esta fuera del tablero 
		if ( r < 0 or r >= len(self.board) ) or ( col < 0 or col >= len(self.board[0]) ):
			return "Le has dado al oceano"
		# si dio en el mismo espacio anterior
		elif (self.boats[r][col] == "2"):
			return "Ya has pegado en este lugar"
		# si le dio a un barco
		elif (self.boats[r][col] == "1"):
			self.boats[r][col] = "2"
			tick = u"\u2713"
			tick = tick.encode('utf-8')
			self.board[r][col] = tick
			win = True
			# comprueba si existen "unos" (barcos en el tablero)
			# si no existen quiere decir los mato a todos
			for row in self.boats:
				for x in range(len(row)):
					if row[x] == "1":
						win = False
			# si gana retorna win
			if win:
				return "win"
			return "Muy bien, le diste :)"
		# si no le dio a nada
		else:
			self.boats[r][col] = "2"
			self.board[r][col] = "x"
			return "No le has dado :("

#Clase que lleva el juego entre los dos usuarios
# esto se hace en un hilo de juego que une dos jugadores
class Game(threading.Thread):  #hereda de threading
	# recibe los dos jugadores (usuarios)
	def __init__(self, p1, p2):
		threading.Thread.__init__(self)
		self.p1 = p1
		self.p2 = p2
		self.turn = 1

	# inicio de juego
	def run(self):

		print "\nhay dos usuarios, se ha creado un juego"
		# avisamos a player uno que ha ingresado al juego
		self.p1.sendMsg("yes")
		self.p1.setName(self.p1.getMsg())
		print "El player 1 ingreso el nombre de: " + self.p1.getName()
		# avisamos a player dos que ha ingresado al juego
		self.p2.sendMsg("yes")
		self.p2.setName(self.p2.getMsg())
		print "El player 2 ingreso el nombre de: " + self.p2.getName()
		# avisamos a ambos player que el juego ha comenzado
		self.p1.sendMsg(bcolors.OKGREEN + "COMIENZA EL JUEGO!!!" + bcolors.ENDC)
		self.p2.sendMsg(bcolors.OKGREEN + "COMIENZA EL JUEGO!!!" + bcolors.ENDC)
		print "Se han ingresado ambos nombres, comienza el juego"
		#comienza el juego por turnos
		while True:
			# juega el jugador uno (tiene su turno)
			if self.turn == 1:
				self.p1.sendMsg("turn")
				self.p2.sendMsg("noturn")
				nombre = self.p1.getName()
				# mostramos tableros de juegos a ambos jugadores
				# inidicanso tambien si es su turno de jugar o no
				self.p1.sendMsg(bcolors.BOLD + "+++++++++++\nEs tu turno\n+++++++++++\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard())
				self.p2.sendMsg(bcolors.BOLD + "++++++++++++\nTurno openente\n++++++++++++\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard())
				# obtenemos fila y columna ingresadas por player 1
				row = self.p1.getMsg()
				col = int(self.p1.getMsg())
				# se realiza el juego en el tablero del contricante (player 2)
				result = self.p2.board.play(row, col)
				if result == "win":
					self.p1.sendMsg("Ganastee!!")
					self.p2.sendMsg("Perdiste!!")
					# si ha ganado sale del ciclo o juego
					break
				else:
					# se envia el resultado del juego al jugador
					self.p1.sendMsg(result)
				# se cambia el turno
				self.turn = 2
			# juega el jugador dos (tiene su turno)
			elif self.turn == 2:
				self.p1.sendMsg("noturn")
				self.p2.sendMsg("turn")
				# mostramos tableros de juegos a ambos jugadores
				# inidicanso tambien si es su turno de jugar o no
				self.p2.sendMsg(bcolors.BOLD + "+++++++++++\nEs tu turno\n+++++++++++\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard())
				self.p1.sendMsg(bcolors.BOLD + "++++++++++++\nTurno openente\n++++++++++++\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard())
				# obtenemos fila y columna ingresadas por player 2
				row = self.p2.getMsg()
				col = int(self.p2.getMsg())
				# se realiza el juego en el tablero del contricante (player 1)
				result = self.p1.board.play(row, col)
				if result == "win":
					self.p2.sendMsg("Ganastee!!")
					self.p1.sendMsg("Perdiste!!")
					# si ha ganado sale del ciclo o juego
					break
				else:
					# se envia el resultado del juego al jugador
					self.p2.sendMsg(result)
				# se cambia el turno
				self.turn = 1
		# al terminar el juego cierro los socket de los juegos
		self.p1.closeSocket()
		self.p2.closeSocket()
		print "termino el juego"
	
#clase server
class Server():

	def __init__(self):
		#variables necesarias para crear socket
		# y para indicar el puerto y max cola
		self.host = "127.0.0.1"
		self.port = 9991
		self.maxcon = 1
		self.clients = []
		
	def start(self):
		# creamos socket
		self.s=socket.socket()
		#reserva el puerto
		self.s.bind((self.host, self.port))
		#el socket queda a la escucha de conexiones
		self.s.listen(self.maxcon)
		# creamos un ciclo, para que cada vez que llega un cliente,
		# crea un cliente y lo deriva a su propio socket
		while True:
			# si hay 2 clientes conectados al servidor crea un juego
			# y limpia la lista de clientes
			if len(self.clients) == 2:
				game = Game(self.clients[0], self.clients[1])
				game.start()
   				del self.clients[0]
   				del self.clients[0]
   			# si no hay dos usuarios, lo recibe el servidor, crea su socket y
   			# lo agrega a la lista de usuarios (clientes)
			else: 
				client = User(self.s.accept())
				self.clients.append(client)
				client.start()
			
# 3 4 8 - 2 2 2
#Clase user que tiene herencia de thread, que proviene de thereading
class User(threading.Thread): #hereda de threading

	def __init__(self, (sc, addr)):
		#llamo al constructor de la clase Thread
		threading.Thread.__init__(self)
		# socket pequeno dejando liberado socket principal
		self.sc = sc
		self.addr = addr
		self.name = ''
		self.board = Board(3,4,8)

	def run(self):
		print "cliente iniciado"

	# agregar nombre usuario
	def setName(self, n):
		self.name = n

	# obtener nombre usuario
	def getName(self):
		return self.name

	# obtener mensajes de los usuarios
	def getMsg(self):
		return self.sc.recv(1024)

	# cerrar socket del usuario
	def closeSocket(self):
		self.sc.close()

	# enviar mensajes al usuario
	def sendMsg(self, msg):
		self.sc.send(msg)

# "main de python"
if __name__ == "__main__":
	server = Server()
	server.start()