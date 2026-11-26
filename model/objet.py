import random
from constants import OBJET_POIDS
def choix_objet():
    liste_objets=list(OBJET_POIDS.keys())
    liste_poids=list(OBJET_POIDS.values())
    a=random.choices(liste_objets,liste_poids)
    return a[0]

class Objet:
    def __init__(self):
        self.objet=choix_objet()

    def utiliser(self,joueur):
        pass

