import pygame
from constants import TILE_SIZE
from model.terrain import Terrain

class RoadTile:
    """Case de la grille du circuit.

    Attributes:
        col, row: Coordonnées de la case dans la grille.
        terrain:type de terrain sur lequel on roule
        sprite: Image mise en cache après le premier dessin.
    """

    def __init__(self, col: int, row: int,terrain:Terrain):
        self.col = col
        self.row = row
        self.terrain=terrain
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill((80, 80, 90))
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
