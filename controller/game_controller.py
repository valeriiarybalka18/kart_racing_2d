
import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Contrôleur principal du jeu."""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """Lance la boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Traite les événements Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Redirige les touches selon l'état actuel du jeu."""
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.MODE_SELECT:
            self.handle_mode_select(key)

        elif state == GameState.CAR_SELECT:
            self.handle_car_select_key(key)

        elif state == GameState.CIRCUIT_SELECT:
            self.handle_circuit_select_key(key)

        elif state == GameState.RACING:
            self.handle_racing_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Gère les touches du menu principal."""
        if key == pygame.K_RETURN:
            self.model.state = GameState.MODE_SELECT

        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_mode_select(self, key: int) -> None:
        """Gère la sélection du nombre de joueurs."""
        if key == pygame.K_UP:
            self.model.select_next_player_count()

        elif key == pygame.K_DOWN:
            self.model.select_previous_player_count()

        elif key == pygame.K_RETURN:
            self.model.state = GameState.CAR_SELECT

        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU
        

    def handle_car_select_key(self, key: int) -> None:
        if key == pygame.K_LEFT:
            self.model.select_previous_car(0)
        elif key == pygame.K_RIGHT:
            self.model.select_next_car(0)
        elif self.model.nb_players == 2 and key == pygame.K_d:
            self.model.select_previous_car(1)
        elif self.model.nb_players == 2 and key == pygame.K_q:
            self.model.select_next_car(1)
        elif key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECT
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MODE_SELECT

    def handle_circuit_select_key(self, key: int) -> None:
        """Gère la sélection du circuit."""
        if key == pygame.K_UP:
            self.model.select_previous_circuit()

        elif key == pygame.K_DOWN:
            self.model.select_next_circuit()

        elif key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING

        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def handle_racing_key(self, key: int) -> None:
        """Gère les touches pendant la course."""
        if key == pygame.K_ESCAPE:
            self.model.return_to_menu()

    def update(self) -> None:
        """Met à jour le jeu pendant la course."""
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car

        self.apply_input(car, p1_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """Applique les commandes du joueur à sa voiture."""
        if player_input['accelerate']:
            car.accelerate()

        if player_input['brake']:
            car.brake()

    def render(self) -> None:
        """Demande à la vue de dessiner le jeu."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Ferme le jeu."""
        self.running = False
        pygame.quit()
        sys.exit()
