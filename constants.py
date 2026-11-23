WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

DT=1/FPS

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 180.0
CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_WHEELBASE = 50
CAR_BRAKE_FORCE = 360.0
CAR_REVERSE_ACCELERATION = 180.0
CAR_MAX_REVERSE = 120.0
CAR_MAX_STEERING_ANGLE = 30.0
CAR_STEERING_RATE = 120.0 #degres/s(braquage complet en 0,25s)
CAR_STEERING_RECENTER_RATE = 90.0 #degres/s(retour droit en 0,33s)
CAR_AIR_DRAG = 0.6 #coeff des frottements de l'air
CAR_STOP_THRESHOLD = 1.0 #seuil d'arret de la voiture


class GameState:
    MENU = "menu"
    RACING = "racing"
    CIRCUIT_SELECT="circuit_select"

# --- Circuits ---
CIRCUITS=[
    {"name":"Circuit 1", "start_col":7, "start_row":1},
    {"name":"Circuit 2", "start_col":3, "start_row":5}
]

# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
