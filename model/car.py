import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_WHEELBASE,
    CAR_BRAKE_FORCE, CAR_REVERSE_ACCELERATION, CAR_MAX_STEERING_ANGLE, CAR_STEERING_RATE, CAR_STEERING_RECENTER_RATE
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
        start_x = start_col * TILE_SIZE + TILE_SIZE // 2
        start_y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.sprite = self.build_sprite()
        self.position = pygame.math.Vector2(start_x, start_y)
        self.velocity = pygame.math.Vector2() #px/s
        self.orientation:float = 0.0
        self.steering_angle:float = 0.0
        self.is_drifting:bool = False
        self.acceleration:float = 0.0 #px/s^2
        self.steering_input:int = 0 #-1:droite, 0:rien, +1:gauche

    def accelerate(self) -> None:
        """Augmente la vitesse de CAR_ACCELERATION."""

        self.acceleration = CAR_ACCELERATION

    def brake(self) -> None:
        """Freine si la voiture avance, sinon enclenche la marche arrière.

        La vitesse est bloquée à 0 pendant un freinage et à
        -CAR_MAX_REVERSE_SPEED en marche arrière.
        """
        forward = pygame.math.Vector2(1,0).rotate(-self.orientation)
        if self.velocity.dot(forward) > 0:
            self.acceleration = -CAR_BRAKE_FORCE
        else:
            self.acceleration = -CAR_REVERSE_ACCELERATION

    def update(self, dt:float) -> None:
        if self.steering_input != 0:
            self.steering_angle = max(-CAR_MAX_STEERING_ANGLE, min(self.steering_angle+self.steering_input*CAR_STEERING_RATE*dt,CAR_MAX_STEERING_ANGLE))
        else:
            step = CAR_STEERING_RECENTER_RATE*dt
            if abs(self.steering_angle)<=step:
                self.steering_angle = 0
            elif self.steering_angle >0:
                self.steering_angle -= step
            elif self.steering_angle < 0:
                self.steering_angle += step
        forward = pygame.math.Vector2(1,0).rotate(-self.orientation)
        v_long=self.velocity.dot(forward)
        self.orientation += math.degrees((v_long / CAR_WHEELBASE)*math.tan(math.radians(self.steering_angle)))*dt
        forward_new = pygame.math.Vector2(1,0).rotate(-self.orientation)
        self.velocity += forward_new*self.acceleration*dt
        v_long_new = self.velocity.dot(forward_new)
        self.velocity = forward_new*v_long_new #provisoir : sans derapage(supprimer apres)
        self.position += self.velocity*dt
        self.acceleration = 0
        self.steering_input = 0

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, self.orientation)
        rect = rotated.get_rect(center=(int(self.position.x), int(self.position.y)))
        return rotated, rect

    def steer_right(self) -> None:
        self.steering_input = -1
        
    def steer_left(self) -> None:
        self.steering_input = 1
        
    