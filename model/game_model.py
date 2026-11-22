from constants import GameState, GRID_ROWS, GRID_COLS, CIRCUITS, CARS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """Modèle global : état du jeu, circuit et voiture.

    Ne dépend ni du clavier ni de l'affichage.
    """

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.selected_circuit:int=0 #Indice dans CIRCUITS
        self.nb_players = 1
        self.player_cars=[0,0]

    def select_next_player_count(self):
        self.nb_players = (self.nb_players % 2) + 1

    def select_previous_player_count(self):
        self.nb_players = (self.nb_players - 2) % 2 + 1


    def select_next_car(self, player: int) -> None:
        self.player_cars[player] = (self.player_cars[player] + 1) % len(CARS)

    def select_previous_car(self, player: int) -> None:
        self.player_cars[player] = (self.player_cars[player] - 1) % len(CARS)


    def select_next_circuit(self) -> None:
        self.selected_circuit=(self.selected_circuit+1)%len(CIRCUITS)

    def select_previous_circuit(self) -> None:
        self.selected_circuit=(self.selected_circuit-1)%len(CIRCUITS)

    def load_circuit(self) -> None:
        info = CIRCUITS[self.selected_circuit]
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        color = CARS[self.player_cars[0]]["color"]    # <-- cette ligne manque
        self.spawn_car(info["start_col"], info["start_row"], color)

    def spawn_car(self, start_col:int, start_row:int, color : tuple) -> None:
        self.car = Car(start_col, start_row,color)

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()

    def return_to_menu(self) -> None:
        self.state=GameState.MENU
        self.circuit=None
        self.car=None
