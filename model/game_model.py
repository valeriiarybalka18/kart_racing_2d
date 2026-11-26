from constants import GameState, GRID_ROWS, GRID_COLS, CIRCUITS, FLOOR_TYPE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.terrain import Terrain


class GameModel:
    """Modèle global : état du jeu, circuit et voiture.

    Ne dépend ni du clavier ni de l'affichage.
    """

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.selected_circuit:int=0 #Indice dans CIRCUITS

    def select_next_circuit(self) -> None:
        self.selected_circuit=(self.selected_circuit+1)%len(CIRCUITS)

    def select_previous_circuit(self) -> None:
        self.selected_circuit=(self.selected_circuit-1)%len(CIRCUITS)

    def load_circuit(self) -> None:
        info=CIRCUITS[self.selected_circuit]
        terrains={lettre:Terrain(mot) for lettre,mot in FLOOR_TYPE.items()}
        grid = [ ]
        liste=[]
        for row_idx in range(GRID_ROWS):
            for col_idx in range(GRID_COLS):
                ltr=info["layout"][row_idx][col_idx]
                liste.append(RoadTile(col=col_idx, row=row_idx,terrain=terrains[ltr]))
            grid.append(liste)
            liste=[]
        self.circuit = Circuit(grid=grid)
        self.spawn_car(info["start_col"], info["start_row"])

    def spawn_car(self, start_col:int, start_row:int) -> None:
        self.car = Car(start_col, start_row)

    def update(self, dt:float) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        pos_x=self.car.position.x
        pos_y=self.car.position.y
        tile=self.circuit.get_tile_at_pixel(pos_x, pos_y)
        if tile is None or tile.terrain.is_void:
            self.car.teleport(self.car.start_postion, self.car.start_orientation)
            return
        self.car.update(dt, tile.terrain)

    def return_to_menu(self) -> None:
        self.state=GameState.MENU
        self.circuit=None
        self.car=None