import pygame
class Terrain:
    """definir nos differents types de terrains"""
    def __init__(self,sol:str):
        self.sol=sol

    def determination_grip(self):#pour determiner le frottement en drift
        if self.sol == "Asphalte":
            return 1.4
        elif self.sol == "Herbe":
            return 0.9
        elif self.sol == "Terre":
            return 0.5
        elif self.sol == "Glace":
            return 0.05
        elif self.sol=="Vide":
            return 0
        else:
            raise ValueError(f"y'a une erreur dans le nom de sol a {self.sol}")
    def determination_traction(self):#pour determiner la traction en general
        if self.sol == "Asphalte":
            return 1
        elif self.sol == "Herbe":
            return 0.7
        elif self.sol == "Terre":
            return 0.7
        elif self.sol == "Glace":
            return 0.3
        elif self.sol=="Vide":
            return 0
        else:
            raise ValueError(f"y'a une erreur dans le nom de sol a {self.sol}")
    def determination_seuil(self):#pour determiner le seuil de decrochage
        if self.sol == "Asphalte":
            return 1
        elif self.sol == "Herbe":
            return 0.7
        elif self.sol == "Terre":
            return 0.5
        elif self.sol == "Glace":
            return 0.1
        elif self.sol=="Vide":
            return 0
        else:
            raise ValueError(f"y'a une erreur dans le nom de sol a {self.sol}")
    def est_vide(self):
        return (self.sol=="Vide")
