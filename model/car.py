import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, 
    CAR_BRAKE_FORCE, CAR_MAX_REVERSE, CAR_REVERSE_ACCELERATION
)


class Car:
    """Voiture : position, vitesse, orientation et image.

    Attributes:
        x, y: Position du centre en pixels.
        speed: Vitesse actuelle (négative en marche arrière).
        angle: Orientation en degrés.
        sprite: Image de base, avant rotation.
    """

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """Augmente la vitesse de CAR_ACCELERATION."""

        self.speed += CAR_ACCELERATION

    def brake(self) -> None:
        """Freine si la voiture avance, sinon enclenche la marche arrière.

        La vitesse est bloquée à 0 pendant un freinage et à
        -CAR_MAX_REVERSE_SPEED en marche arrière.
        """
        if self.speed >0 :
            self.speed=max(0,self.speed-CAR_BRAKE_FORCE)
        else:
            self.speed=max(-CAR_MAX_REVERSE, self.speed-CAR_REVERSE_ACCELERATION)

    def update_position(self) -> None:
        self.y += self.speed

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
