from random import randrange

amount = 10
bet = 0
pseudo = ""
level = 1

pseudo = input("Je suis Python. Quel est votre pseudo ?")

print("Bonjour", pseudo, "vous avez", amount,
      "€ .Très bien ! Installez vous SVP à la table de pari.")

print("""- Je viens de penser à un nombre entre 1 et 10. Devinez lequel ?

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
        bet = int(input("Le jeu commence, entrez votre mise : ?"))
        if bet > amount:
            print("Vous ne pouvez miser que", amount, "€")
            continue
        else:
            amount = amount - bet
            break

    print("Vous avez misé", bet, "€", "il vous reste", amount, "€")

    while True:
        proposal = int(input("Alors mon nombre est : ?"))
        if proposal == nb_python:
            print("Bravo ! Vous avez gagné !")
            earn = bet * multiplier
            amount = amount + earn
            if (level != 3):
                level = level + 1
            print("Vous avez gagné :", earn, "€ vous êtes désormais au level", level, "avec ", amount, " €")

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
                print("Vous êtes désormais au level", level)
                choice = input("Voulez-vous continuer le jeu ? (o/n)")
                if choice == "o":
                    play()
                else:
                    print("Merci d'avoir joué !")
                break


play()
