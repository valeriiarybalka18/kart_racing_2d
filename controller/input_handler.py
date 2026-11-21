import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "brake",
}


class InputHandler:
    """Lit l'état du clavier et le convertit en actions du jeu.

    Le lien touche → action est défini par le dictionnaire MAPPING.
    """
    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        """Retourne les actions actuellement demandées.

        Returns:
            Dictionnaire {nom_action: bool} où True signifie que la touche
            associée est maintenue à cet instant.
        """
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
