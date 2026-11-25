import pygame  # type: ignore[reportMissingImports]
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DT,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Contrôleur principal du jeu.
    Fait tourner la boucle principale, lit les entrées du clavier, les
    traduit en actions sur le modèle et demande à la vue de dessiner.
    """
    def __init__(self):
        """Crée la fenêtre, l'horloge, le modèle, 
        la vue et le gestionnaire d'entrées."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.SCALED,)
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """Lance la boucle principale.

        Chaque itération (une frame) traite les événements, met à jour le
        jeu, dessine l'écran.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Traite les événements pygame de la frame (fermeture, touche enfoncée)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Réagit à l'appui sur une touche selon l'état actuel du jeu.

        Args:
            key: Code de la touche pygame (par exemple pygame.K_RETURN).
        """
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECT:
            self.handle_circuit_select_key(key)
        elif state == GameState.RACING:
            self.handle_racing_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Gère les touches dans le menu : Entrée lance la course, Échap quitte.

        Args:
            key: Code de la touche pygame.
        """
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECT
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_circuit_select_key(self,key):
        if key==pygame.K_UP:
            self.model.select_previous_circuit()
        elif key == pygame.K_DOWN:
            self.model.select_next_circuit()
        elif key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state=GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.model.state=GameState.MENU

    def handle_racing_key(self,key) ->None:
        if key == pygame.K_ESCAPE:
            self.model.return_to_menu()   

    def update(self) -> None:
        """Met à jour le jeu pour une frame.

        Ne fait rien si la course n'est pas en cours. Sinon lit les entrées
        du joueur, les applique à la voiture, puis fait avancer le modèle.
        """
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car
        self.apply_input(car, p1_input)
        self.model.update(DT, None)

    def apply_input(self, car, player_input) -> None:
        """Traduit les actions du joueur en commandes sur la voiture."""
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        if player_input['steer_right']:
            car.steer_right()
        if player_input['steer_left']:
            car.steer_left()

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
