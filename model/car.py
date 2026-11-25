import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_WHEELBASE, CAR_MAX_REVERSE, CAR_AIR_DRAG, CAR_STOP_THRESHOLD,
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

    @property
    def forward(self) -> pygame.math.Vector2 :
        return pygame.math.Vector2(1,0).rotate(-self.orientation)

    @property
    def longitudial_speed(self) -> float:
        return self.velocity.dot(self.forward)

    def brake(self) -> None:
        """Freine si la voiture avance, sinon enclenche la marche arrière.

        La vitesse est bloquée à 0 pendant un freinage et à
        -CAR_MAX_REVERSE_SPEED en marche arrière.
        """
        if self.longitudial_speed > 0:
            self.acceleration = -CAR_BRAKE_FORCE
        else:
            self.acceleration = -CAR_REVERSE_ACCELERATION

    def _update_steering(self, dt:float) ->None:
        """Met à jour l'angle de braquage ou le recentre vers 0."""
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

    def _update_orientation(self, dt:float) -> None:
        """Fait pivoter la voiture selon le modèle bicyclette."""
        self.orientation += math.degrees((self.longitudial_speed / CAR_WHEELBASE)*math.tan(math.radians(self.steering_angle)))*dt

    def _apply_forces(self, dt:float) ->None:
        """Applique l'accélération, le frottement de l'air et le seuil d'arrêt."""
        self.velocity += self.forward*self.acceleration*dt #ajout d'acceleration
        self.velocity -= CAR_AIR_DRAG*self.velocity*dt #frottement de l'air
        if self.velocity.length()<CAR_STOP_THRESHOLD:
            self.velocity=pygame.math.Vector2()

    def _apply_grip(self) -> None:
        """Aligne la vitesse sur l'axe avant (provisoire) et borne la marche arrière."""
        self.velocity = self.forward*max(-CAR_MAX_REVERSE,self.longitudial_speed)

    def _reset_inputs(self) -> None:
        """Réinitialise les intentions de commande pour la frame suivante."""
        self.acceleration = 0
        self.steering_input = 0

    def update(self, dt:float) -> None:
        """Met à jour la physique de la voiture sur un pas de temps.

        Enchaîne le braquage, la rotation, l'application des forces
        (moteur, freinage, frottements), l'adhérence et le déplacement,
        puis réinitialise les intentions de commande de la frame.

        Args:
            dt: Pas de temps écoulé depuis la frame précédente, en secondes.
        """
        self._update_steering(dt)
        self._update_orientation(dt)
        self._apply_forces(dt)
        self._apply_grip() #provisoire : sans derapage(supprimer apres)
        self.position += self.velocity*dt
        self._reset_inputs()

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
        
    def teleport(self, pos : pygame.math.Vector2, orientation =None) -> None:
        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2()
        self.acceleration = 0.0
        self.steering_input = 0.0
        self.steering_angle = 0.0
        self.is_drifting = False
        if orientation is not None:
            self.orientation = orientation

    def apply_boost(self, amount : float) -> None:
        self.velocity += self.forward*amount