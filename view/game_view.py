import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState, CIRCUITS, CARS 
)
from model.game_model import GameModel


class GameView:
    """Vue : dessine l'état du modèle avec pygame, sans le modifier."""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.MODE_SELECT:
            self._draw_mode_select(model)
        elif model.state == GameState.CAR_SELECT:
            self._draw_car_select(model)
        elif model.state == GameState.CIRCUIT_SELECT:
            self._draw_circuit_select(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_circuit_select(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2
        
        title_surf = self.font.render(
            "Selection du circuit", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))
        
        options = [("Circuit Debutant", GameState.RACING),
                    ("Circuit Avance", GameState.RACING),
                    ("Retour au Menu", None)]
        for i,circuit in enumerate(CIRCUITS):
            y=320+i*80
            selected=(i==model.selected_circuit)
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            border_color = COLOR_ACCENT if selected else COLOR_PANEL_BORDER
            border_width = 4 if selected else 2
            pygame.draw.rect(self.screen, border_color,
                            rect, border_width, border_radius=8)
            text_color=COLOR_ACCENT if selected else COLOR_TEXT
            text_surf = self.font.render(circuit["name"], True, text_color)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))



    def _draw_mode_select(self, model: GameModel) -> None:
        """Choix du nombre de joueurs (haut/bas pour changer, Entrée pour valider)."""
        cx = WINDOW_WIDTH // 2
        title_surf = self.font.render("Nombre de joueurs", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        labels = ["1 JOUEUR", "2 JOUEURS"]
        for i, label in enumerate(labels):
            y = 320 + i * 80
            selected = (i + 1 == model.nb_players)
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen,
                            COLOR_ACCENT if selected else COLOR_PANEL_BORDER,
                            rect, 4 if selected else 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if selected else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_car_select(self, model: GameModel) -> None:
        """Choix des voitures : un panneau par joueur."""
        cx = WINDOW_WIDTH // 2
        title_surf = self.font.render("Choix de la voiture", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 100)))

        if model.nb_players == 1:
            centers = [cx]
        else:
            centers = [WINDOW_WIDTH // 4, 3 * WINDOW_WIDTH // 4]
        controls = ["< >  (fleches)", "Q  D"]

        for player in range(model.nb_players):
            px = centers[player]
            car = CARS[model.player_cars[player]]

            # Panneau
            panel = pygame.Rect(px - 150, 200, 300, 320)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_ACCENT, panel, 3, border_radius=8)

            # Titre du joueur
            label = self.font.render(f"Joueur {player + 1}", True, COLOR_ACCENT)
            self.screen.blit(label, label.get_rect(center=(px, 235)))

            # Aperçu de la voiture (rectangle de sa couleur)
            preview = pygame.Rect(0, 0, 120, 70)
            preview.center = (px, 340)
            pygame.draw.rect(self.screen, car["color"], preview, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_TEXT, preview, 2, border_radius=10)

            # Flèches
            left = self.font.render("<", True, COLOR_TEXT)
            right = self.font.render(">", True, COLOR_TEXT)
            self.screen.blit(left, left.get_rect(center=(px - 110, 340)))
            self.screen.blit(right, right.get_rect(center=(px + 110, 340)))

            # Nom de la voiture
            name = self.font.render(car["name"], True, COLOR_TEXT)
            self.screen.blit(name, name.get_rect(center=(px, 420)))

            # Rappel des touches
            hint = self.font.render(controls[player], True, COLOR_PANEL_BORDER)
            self.screen.blit(hint, hint.get_rect(center=(px, 480)))

        enter = self.font.render("Entree : continuer   Echap : retour",
                                True, COLOR_TEXT)
        self.screen.blit(enter, enter.get_rect(center=(cx, WINDOW_HEIGHT - 60)))

    def _draw_menu(self, model: GameModel) -> None:
        """Dessine le menu principal (titre et boutons)."""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """Dessine la grille du circuit puis la voiture.

        Args:
            model: Modèle contenant le circuit et la voiture.
        """
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return
        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)
