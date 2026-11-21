import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState, CIRCUITS
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
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        elif model.state== GameState.CIRCUIT_SELECT:
            self._draw_circuit_select(model)
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
