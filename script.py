from random import randrange
import sys
import time
import requests
import mysql.connector
import json

connection_params = {
	'host': 'mysql-casino-py.alwaysdata.net',
	'user': 'casino-py',
	'password': 'ipssi2022',
	'database': 'casino-py_admin'
}

amount = 10
bet = 0
pseudo = ""
level = 1


def delprint(text, delay_time=0.00):
	for character in text:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(delay_time)
	print("")


def getUser(pseudo):
	try :
		with mysql.connector.connect(**connection_params) as db:
			with db.cursor() as c:
				c.execute("SELECT * FROM user WHERE name_user = '" + pseudo + "'")
				user = c.fetchone()
				print(user)
				if(user is None):
					print("Aucun utilisateur trouvé")
				return user
	except mysql.connector.Error as err:
		print("Something went wrong: {}".format(err))

def createUser(pseudo):
	with mysql.connector.connect(**connection_params) as db:
		with db.cursor() as c:
			c.execute(
				"INSERT INTO user (name_user, amount) VALUES (%s, %s)", (pseudo, amount))
			db.commit()

def update(key, value):
	with mysql.connector.connect(**connection_params) as db:
		with db.cursor() as c:
			c.execute("UPDATE user SET " + key + " = %s WHERE name_user = %s", (value, pseudo))
			db.commit()

def displayStats():
	user = getUser(pseudo)
	bets = json.loads(user[10])
	nb_play = len(bets)
	avg_bet = sum(bets) / nb_play
	print("Vous avez joué", nb_play, "fois")
	print("Votre plus grosse mise est de", user[7], "€")
	print("Votre plus petite mise est de", user[8], "€")
	print("Votre mise moyenne est de", avg_bet, "€")
	
		
pseudo = input("Je suis Python. Quel est votre pseudo ?")

if getUser(pseudo) is None:
	print('ici')
	createUser(pseudo)
else:
	user = getUser(pseudo)
	amount = user[4]
	level = user[2]
	displayStats()

print("Bonjour", pseudo, "vous avez", amount,
	  "€ .Très bien ! Installez vous SVP à la table de pari.")

if level > 1:
	print("Vous êtes au level", level)
	try:
		levelChoice = int(input("Vous pouvez choisir de rester au level actuel ou de choisir un niveau inférieur (ex : 1) : "))
		if levelChoice > 0 and levelChoice <= level:
			level = levelChoice
			update("actual_level", level)
		else:
			print("Vous n'avez pas choisi un level valide, vous restez au level", level)
	except ValueError:
		print("Vous n'avez pas choisi un level valide, vous restez au level", level)

delprint("""- Je viens de penser à un nombre entre 1 et 10. Devinez lequel ?

		- Att : vous avez le droit à trois essais !

		- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !

		- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !

		- Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !

		- Si vous ne le devinez pas au 3è coup, vous perdez votre mise et
		vous avez le droit :
			- de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu.
			- de quitter le jeu.

		- Dès que vous devinez mon nombre : vous avez le droit de quitter le jeu et de partir avec vos gains OU
		de continuer le jeu en passant au level supérieur.
""")

def play():
	global amount
	global bet
	global pseudo
	global level
	nb_try = 1
	max_try = 1 + level * 2
	nb_python = randrange(1, 2*level)
	multiplier = 2

	while True:
		try:
			bet = int(input("Le jeu commence, entrez votre mise : ?"))
		except ValueError:
			print("Vous devez entrer un nombre")
			continue

		if bet > amount:
			print("Vous ne pouvez miser que", amount, "€")
			continue
		if bet <= 0:
			print("Vous ne pouvez miser qu'un montant positif")
			continue
		else:
			amount = amount - bet
			update("amount", amount)
			break

	print("Vous avez misé", bet, "€", "il vous reste", amount, "€")

	user = getUser(pseudo)
	print(user)
	if(user[7] <= bet):
		update("highest_bet", bet)
	if(user[8] >= bet or user[8] == 0):
		update("lowest_bet", bet)

	if user[10] is None:
		data = []
		data.append(bet)
		data = json.dumps(data)
		update("bets", data)
	else:
		data = json.loads(user[10])
		data.append(bet)
		data = json.dumps(data)
		update("bets", data)

	while True:
		try:
			proposal = int(input("Alors mon nombre est : ?"))
		except ValueError:
			print("Vous devez entrer un nombre")
			continue

		if proposal == nb_python:
			print("Bravo ! Vous avez gagné !")
			earn = bet * multiplier
			user = getUser(pseudo)
			if(multiplier == 2):
				update("first_time", user[9] + 1)
			amount = amount + earn
			update("amount", amount)

			if (level != 3):
				level = level + 1
				user = getUser(pseudo)
				if(user[3] <= level):
					update("highest_level", level)
				update("actual_level", level)
				if(user[5] <= earn):
					update("highest_profit", earn)
				print("Statistiques du niveau précédent")
				print("Nombre de coups joués : ", nb_try)

			print("Vous avez gagné :", earn,
				  "€ vous êtes désormais au level", level, "avec ", amount, " €")

			choice = input("Voulez-vous continuer le jeu ? (o/n)")
			if choice == "o":
				play()
			else:
				print("Merci d'avoir joué !")
			break
		else:
			if nb_try < max_try:
				print("C'est faux ! Essayez encore !")
				if (proposal > nb_python):
					print("C'est moins ! Il vous reste",
						  max_try - nb_try, "essais")
				else:
					print("C'est plus ! Il vous reste",
						  max_try - nb_try, "essais")
				nb_try = nb_try + 1
				multiplier = multiplier / 2
				continue
			else:
				print("Vous avez perdu ! Mon nombre était", nb_python)
				print("Vous avez maintenant", amount, "€")
				if level != 1:
					level = level - 1
					update("actual_level", level)
				print("Vous êtes désormais au level", level)
				user = getUser(pseudo)
				if(user[6] <= bet):
					update("highest_loss", bet)
				choice = input("Voulez-vous continuer le jeu ? (o/n)")
				if choice == "o":
					play()
				else:
					print("Merci d'avoir joué !")
					sys.exit()
				break

play()

#float