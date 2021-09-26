# setup?
from typing import List
"""
From Python 3.9 (PEP 585) onwards tuple, list and various other classes are now generic types.
Using these rather than their typing counterpart is now preferred.
From Python 3.9 you can now just do:

def f(points: tuple[float, float]):
    return map(do_stuff, points)
    
"""
import datetime
# constantes?

# fonctions globales?

class Round:
    """
    définit la classe Round, qui permet:
    d'enregistrer automatiquement le début du tour (date et heure)
    d'enregistrer automatiquement la fin du tour (date et heure)
    """
    def __init__(self, c_round_number, c_matchs_list, c_start_datetime, c_end_datetime):
        self.round_number = c_round_number
        self.matchs_list = c_matchs_list
        self.start_datetime = c_start_datetime
        self.end_datetime = c_end_datetime




class Match:
    """
    définit la classe Match, qui permet:
    d'enregistrer les parties jouées et les scores
    """
    def __init__(self, joueur_x, score_joueur_x, joueur_y, score_joueur_y):
        self.joueur_x = joueur_x
        self.score_joueur_x = score_joueur_x
        self.joueur_y = joueur_y
        self.score_joueur_y = score_joueur_y

    def record_score(self, score_x, score_y):
        """ permet de saisir les scores des 2 joueurs du match à la fin de la partie et les ajoute aux listes"""




if __name__ == "__main__":
    pass
