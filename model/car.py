import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_WHEELBASE, CAR_MAX_REVERSE, CAR_AIR_DRAG, CAR_STOP_THRESHOLD,
    CAR_BRAKE_FORCE, CAR_REVERSE_ACCELERATION, CAR_MAX_STEERING_ANGLE, CAR_STEERING_RATE, CAR_STEERING_RECENTER_RATE, A_LAT_MAX, DRIFT_FRICTION_SCALE,
    CAR_DRAG_FACTOR, DRIFT_EXIT_LATERAL_SPEED
)


class Car:
    """Voiture : état physique, commandes et image.

    Les commandes (accelerate, brake, steer_left, steer_right) posent des
    intentions ; update(dt, terrain) les consomme puis les remet à zéro.
    Angles en degrés (0° = vers la droite, positif = vers la gauche),
    vitesses en px/s, accélérations en px/s².

    Attributes:
        position: Centre de la voiture, en pixels.
        velocity: Vecteur vitesse, en px/s.
        orientation: Direction du nez, en degrés.
        steering_angle: Angle des roues avant, en degrés.
        is_drifting: True pendant un dérapage.
        acceleration: Intention d'accélération de la frame, en px/s².
        steering_input: Intention de direction (-1 droite, 0 rien, +1 gauche).
        start_position: Point de départ, utilisé pour les retours.
        start_orientation: Orientation de départ, en degrés.
        sprite: Image de base, avant rotation.
    """

    def __init__(self, start_col: int, start_row: int):
        """Place la voiture au centre de la case de départ, à l'arrêt.

        Args:
            start_col: Colonne de la case de départ.
            start_row: Ligne de la case de départ.
        """
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
        self.start_postion=pygame.math.Vector2(start_x, start_y)
        self.start_orientation=0.0

    def accelerate(self) -> None:
        """Demande d'accélérer pour la frame courante (intention)."""

        self.acceleration = CAR_ACCELERATION

    @property
    def forward(self) -> pygame.math.Vector2 :
        """Vecteur unitaire qui pointe vers l'avant de la voiture."""
        return pygame.math.Vector2(1,0).rotate(-self.orientation)

    @property
    def longitudinal_speed(self) -> float:
        """Vitesse projetée sur l'avant, en px/s (négative en marche arrière)."""

        return self.velocity.dot(self.forward)

    @property
    def lateral(self) -> pygame.math.Vector2:
        """Vecteur unitaire qui pointe vers la gauche de la voiture."""
        return pygame.math.Vector2(1,0).rotate(-self.orientation-90)

    @property
    def lateral_speed(self) -> float:
        """Vitesse de glissade projetée sur la gauche, en px/s.

        Positive si la voiture glisse vers sa gauche, négative vers sa droite.
        """
        return self.velocity.dot(self.lateral)

    def _update_drift_state(self, grip_threshold) :
        """Décide si la voiture dérape.

        Calcule la sollicitation latérale demandée par le virage, puis la
        compare au seuil d'adhérence du terrain. Le dérapage commence quand
        elle le dépasse et ne s'arrête que lorsqu'elle repasse sous le seuil
        et que la glissade est devenue faible.

        Args:
            grip_threshold: Seuil d'adhérence du terrain sous la voiture.
        """
        s = self.longitudinal_speed*self.longitudinal_speed*abs(math.tan(math.radians(self.steering_angle)))/(CAR_WHEELBASE*A_LAT_MAX)
        was_drifting=self.is_drifting
        if self.is_drifting:
            if s<grip_threshold and abs(self.lateral_speed)<DRIFT_EXIT_LATERAL_SPEED:
                self.is_drifting=False
        else:
            self.is_drifting=(s>grip_threshold)
        

    def brake(self) -> None:
        """Freine si la voiture avance, sinon enclenche la marche arrière.

        Ne modifie que l'intention d'accélération ; la vitesse en marche
        arrière est bornée plus tard par CAR_MAX_REVERSE.
        """
        if self.longitudinal_speed > 0:
            self.acceleration = -CAR_BRAKE_FORCE
        else:
            self.acceleration = -CAR_REVERSE_ACCELERATION

    def _update_steering(self, dt:float) ->None:
        """Met à jour l'angle de braquage, ou le recentre vers 0 sans commande.

        Args:
            dt: Pas de temps, en secondes.
        """
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
        """Fait pivoter la voiture selon le modèle bicyclette.

        La rotation dépend de la vitesse avant, de l'empattement et de
        l'angle de braquage.

        Args:
            dt: Pas de temps, en secondes.
        """
        self.orientation += math.degrees((self.longitudinal_speed / CAR_WHEELBASE)*math.tan(math.radians(self.steering_angle)))*dt

    def _apply_forces(self, dt:float, traction : float, drag_factor : float) ->None:
        """Applique la poussée du moteur, la traînée et le seuil d'arrêt.

        Args:
            dt: Pas de temps, en secondes.
            traction: Part de la poussée transmise au sol par le terrain.
            drag_factor: Multiplicateur de traînée propre au terrain.
        """
        self.velocity += self.forward*self.acceleration*dt*traction #ajout d'acceleration en fonction du terrain
        self.velocity -= (CAR_AIR_DRAG*drag_factor)*self.velocity*dt #frottement de l'air
        if self.acceleration==0 and self.velocity.length()<CAR_STOP_THRESHOLD:
            self.velocity=pygame.math.Vector2()

    def _apply_grip(self, dt:float, drift_friction) -> None:
        """Gère l'adhérence : supprime ou amortit la vitesse latérale.

        Sans dérapage, la vitesse est alignée sur l'avant (marche arrière
        bornée). En dérapage, la vitesse latérale est conservée et décroît
        selon le frottement de dérapage du terrain.

        Args:
            dt: Pas de temps, en secondes.
            drift_friction: Frottement de dérapage du terrain.
        """
        if not self.is_drifting :
            self.velocity = self.forward*max(-CAR_MAX_REVERSE,self.longitudinal_speed)
            return
        avant = max(-CAR_MAX_REVERSE, self.longitudinal_speed)
        cote = self.lateral_speed
        cote -= drift_friction*DRIFT_FRICTION_SCALE*cote*dt
        self.velocity = self.forward*avant+self.lateral*cote

    def _reset_inputs(self) -> None:
        """Réinitialise les intentions de commande pour la frame suivante."""
        self.acceleration = 0
        self.steering_input = 0

    def update(self, dt:float, terrain) -> None:
        """Fait avancer la physique de la voiture d'un pas de temps.

    Enchaîne braquage, rotation, état de dérapage, forces, adhérence et
    déplacement, puis réinitialise les commandes. Sur un terrain vide, la
    voiture n'est pas mise à jour.

    Args:
        dt: Pas de temps, en secondes.
        terrain: Terrain sous la voiture (traction, grip_threshold,
            drift_friction, is_void, sol), ou None pour un terrain neutre.
    """
        if terrain is None:
            traction = 1.0
            drag_factor = 1.0
            grip_threshold = 1.0
            drift_friction = 1.4
            is_void = False
        else :
            traction = terrain.traction
            drag_factor = CAR_DRAG_FACTOR.get(terrain.sol,1.0)
            grip_threshold=terrain.grip_threshold
            drift_friction = terrain.drift_friction
            is_void = terrain.is_void

        if is_void :
            self._reset_inputs()
            return
        self._update_steering(dt)
        self._update_orientation(dt)
        self._update_drift_state(grip_threshold)
        self._apply_forces(dt, traction, drag_factor)
        self._apply_grip(dt, drift_friction) 
        self.position += self.velocity*dt
        self._reset_inputs()

    def build_sprite(self) -> pygame.Surface:
        """Crée l'image de base de la voiture.

    Returns:
        Surface rectangulaire de la taille CAR_WIDTH x CAR_HEIGHT.
    """
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Renvoie l'image tournée selon l'orientation, avec son rectangle.

    Returns:
        Le couple (image tournée, rectangle centré sur la position).
    """
        rotated = pygame.transform.rotate(self.sprite, self.orientation)
        rect = rotated.get_rect(center=(int(self.position.x), int(self.position.y)))
        return rotated, rect

    def steer_right(self) -> None:
        """Demande de tourner à droite pour la frame courante (intention)."""
        self.steering_input = -1
        
    def steer_left(self) -> None:
        """Demande de tourner à gauche pour la frame courante (intention)."""
        self.steering_input = 1
        
    def teleport(self, pos : pygame.math.Vector2, orientation : float | None =None) -> None:
        """Replace la voiture et arrête tout mouvement.

    Remet à zéro la vitesse, l'accélération, la direction et le dérapage.

    Args:
        pos: Nouvelle position, en pixels.
        orientation: Nouvelle orientation en degrés, ou None pour la garder.
    """

        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2()
        self.acceleration = 0.0
        self.steering_input = 0
        self.steering_angle = 0.0
        self.is_drifting = False
        if orientation is not None:
            self.orientation = orientation

    def apply_boost(self, amount : float) -> None:
        """Ajoute une impulsion de vitesse dans le sens du nez.

    Args:
        amount: Vitesse ajoutée, en px/s.
    """
        self.velocity += self.forward*amount