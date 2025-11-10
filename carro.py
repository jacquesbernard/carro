import os
import random
import time
import msvcrt  # Pour Windows (permet de lire les touches sans appuyer sur Entrée)

# Dimensions du jeu
HAUTEUR = 20
LARGEUR = 15

# Symboles du jeu
VIDE = " "
JOUEUR = "▲"
ENNEMI = "V"
BORDE = "|"

# Position initiale du joueur (au centre en bas)
pos_joueur = [HAUTEUR - 2, LARGEUR // 2]

# Liste d'ennemis (positions)
ennemis = []
score = 0
vitesse = 0.15  # temps entre deux rafraîchissements


def nettoyer_ecran():
    """Efface le terminal (Windows ou Linux)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher(grille):
    """Affiche la matrice du jeu"""
    for ligne in grille:
        print("".join(ligne))
    print(f"\nScore : {score}")


def creer_grille():
    """Crée une grille vide avec les bordures de la piste"""
    grille = []
    for i in range(HAUTEUR):
        ligne = []
        for j in range(LARGEUR):
            if j == 0 or j == LARGEUR - 1:
                ligne.append(BORDE)
            else:
                ligne.append(VIDE)
        grille.append(ligne)
    return grille


def ajouter_ennemi():
    """Ajoute un ennemi en haut de la piste à une position aléatoire"""
    x = 1  # première ligne jouable
    y = random.randint(1, LARGEUR - 2)
    ennemis.append([x, y])


def deplacer_ennemis():
    """Fait descendre les ennemis"""
    global ennemis
    for e in ennemis:
        e[0] += 1
    # Supprime ceux qui sortent de l’écran
    ennemis = [e for e in ennemis if e[0] < HAUTEUR - 1]


def maj_grille():
    """Met à jour le contenu de la grille"""
    grille = creer_grille()

    # Placer le joueur
    grille[pos_joueur[0]][pos_joueur[1]] = JOUEUR

    # Placer les ennemis
    for e in ennemis:
        if 0 <= e[0] < HAUTEUR and 0 <= e[1] < LARGEUR:
            grille[e[0]][e[1]] = ENNEMI
    return grille


def verifier_collision():
    """Vérifie si un ennemi touche le joueur"""
    for e in ennemis:
        if e[0] == pos_joueur[0] and e[1] == pos_joueur[1]:
            return True
    return False


def lire_touche():
    """Lit une touche sans bloquer le programme"""
    if msvcrt.kbhit():
        return msvcrt.getch().decode('utf-8').lower()
    return None


def main():
    global score, vitesse

    # Boucle principale
    iterations = 0
    while True:
        nettoyer_ecran()

        # Ajout d’un ennemi aléatoirement
        if iterations % 8 == 0:
            ajouter_ennemi()

        # Déplacement des ennemis
        deplacer_ennemis()

        # Déplacement du joueur
        touche = lire_touche()
        if touche == 'a' and pos_joueur[1] > 1:
            pos_joueur[1] -= 1
        elif touche == 'd' and pos_joueur[1] < LARGEUR - 2:
            pos_joueur[1] += 1
        elif touche == '\x1b':  # Touche ÉCHAP
            print("Jeu terminé par le joueur.")
            break

        # Mise à jour du score
        score += 1

        # Affichage
        grille = maj_grille()
        afficher(grille)

        # Vérifie la collision
        if verifier_collision():
            print("\n💥 Collision ! Fin du jeu 💥")
            break

        time.sleep(vitesse)
        iterations += 1


if __name__ == "__main__":
    main()

