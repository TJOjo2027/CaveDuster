# LIBRARIES
import pygame
import sys
import os
import random
from mine_grid import MineGrid

# CONSTANTS
CELL_SIZE = 40
NUM_ROWS = 12
NUM_COLS = 20
HUD_HEIGHT = 60
SIDEBAR_WIDTH = 220
GRID_WIDTH = NUM_COLS * CELL_SIZE
WINDOW_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = HUD_HEIGHT + NUM_ROWS * CELL_SIZE
FPS = 60
MUSIC_FOLDER = r"C:\Users\tojo\Desktop\Cave_Duster\CaveDuster\game_music"

# COLORS
COLOR_BG = (30,  30,  30)
COLOR_HUD = (20,  20,  20)
COLOR_COVERED = (80,  80,  80)
COLOR_UNCOVERED = (45,  45,  45)
COLOR_CURSOR = (80, 120,  80)
COLOR_MINE = (180,  40,  40)
COLOR_FLAG = (220, 160,   0)
COLOR_GRID_LINE = (100, 100, 100)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220,  80,  80)
COLOR_SIDEBAR = (25,  25,  35)
COLOR_BTN = (55,  55,  75)
COLOR_BTN_HOVER = (75,  75, 105)
COLOR_ACCENT = (80, 160, 220)

WEIGHT_COLORS = {
    1: (100, 149, 237),
    2: (80,  180,  80),
    3: (220,  80,  80),
    4: (100,  60, 180),
    5: (180,  60,  60),
    6: (60,  180, 180),
    7: (220,  60, 220),
    8: (160, 160, 160),
}

# GAME INIT
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

screen  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("CaveDuster")
clock   = pygame.time.Clock()
font    = pygame.font.SysFont("comicsansms", 22, bold=True)
font_sm = pygame.font.SysFont("comicsansms", 13)
font_xs = pygame.font.SysFont("comicsansms", 11)

joystick = None
if (pygame.joystick.get_count() > 0):
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# MUSIC PLAYER SETTINGS (playing songs from Mac DeMarco's One Wayne G)
def load_playlist(folder):
    if not os.path.isdir(folder):
        return []
    ext = ".mp3"
    tracks = sorted(
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(ext)
    )
    return tracks

playlist = load_playlist(MUSIC_FOLDER)
track_index = 0
music_paused = False
shuffle_on = False
volume = 0.5 # music ranges from volume levels 0.0 to 1.0
pygame.mixer.music.set_volume(volume)

def play_track(index):
    global track_index, music_paused
    if (not playlist):
        return
    track_index  = index % len(playlist)
    music_paused = False
    pygame.mixer.music.load(playlist[track_index])
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

shuffle_queue = []

def rebuild_shuffle_queue():
    indices = list(range(len(playlist)))
    if (track_index in indices):
        indices.remove(track_index)
    random.shuffle(indices)
    return indices

def next_track():
    global shuffle_queue
    if (shuffle_on and len(playlist) > 1):
        if not shuffle_queue:
            shuffle_queue = rebuild_shuffle_queue()
        play_track(shuffle_queue.pop())
    else:
        play_track(track_index + 1)

def prev_track():
    play_track(track_index - 1)

def toggle_shuffle():
    global shuffle_on, shuffle_queue
    shuffle_on = not shuffle_on
    shuffle_queue = rebuild_shuffle_queue() if shuffle_on else []

def toggle_pause():
    global music_paused
    if not playlist:
        return
    if music_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    music_paused = not music_paused

def set_volume(new_vol):
    global volume
    volume = max(0.0, min(1.0, new_vol))
    pygame.mixer.music.set_volume(volume)

# Auto-advance when a track finishes
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

if playlist:
    play_track(0)

# GAME STATES
def new_game():
    grid = MineGrid(NUM_ROWS, NUM_COLS)
    flagged = [[False] * NUM_COLS for _ in range(NUM_ROWS)]
    start_ticks = pygame.time.get_ticks()
    game_over = False
    won = False
    first_click = True # to ensure mines aren't placed until first click
    return grid, flagged, start_ticks, game_over, won, first_click

grid, flagged, start_ticks, game_over, won, first_click = new_game()
cursor_row = 0
cursor_col = 0

# HELPER FUNCTIONS
def pixel_to_cell(x, y):
    col = x // CELL_SIZE
    row = (y - HUD_HEIGHT) // CELL_SIZE
    return row, col

def count_mines():
    total = sum(grid.getCell(r, c).isMine for r in range(NUM_ROWS) for c in range(NUM_COLS))
    flags = sum(flagged[r][c] for r in range(NUM_ROWS) for c in range(NUM_COLS))
    return total - flags

def check_win():
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if not grid.getCell(r, c).isMine and grid.getCell(r, c).isCovered:
                return False
    return True

def reveal(row, col):
    global game_over, won, first_click
    if game_over or not (0 <= row < NUM_ROWS and 0 <= col < NUM_COLS):
        return
    if first_click:
        grid.initializeMines(row, col)  # place mines now, skipping this cell
        first_click = False
    cell = grid.getCell(row, col)
    if not cell.isCovered or flagged[row][col]:
        return
    cell.isCovered = False
    if cell.isMine:
        game_over = True
        return
    if cell.weight == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                reveal(row + dr, col + dc)
    if check_win():
        won = True
        game_over = True

def toggle_flag(row, col):
    if game_over or not grid.getCell(row, col).isCovered:
        return
    flagged[row][col] = not flagged[row][col]

# SIDEBAR
SB_X = GRID_WIDTH + 10          # left edge of sidebar content
SB_W = SIDEBAR_WIDTH - 20       # usable width

def make_btn(y, h=32):
    return pygame.Rect(SB_X, y, SB_W, h)

BTN_PREV    = make_btn(HUD_HEIGHT + 20)
BTN_PLAY    = make_btn(HUD_HEIGHT + 62)
BTN_NEXT    = make_btn(HUD_HEIGHT + 104)
BTN_SHUFFLE = make_btn(HUD_HEIGHT + 146)
BTN_VOL_UP  = make_btn(HUD_HEIGHT + 210, 28)
BTN_VOL_DN  = make_btn(HUD_HEIGHT + 246, 28)

def draw_button(rect, label, hover=False):
    color = COLOR_BTN_HOVER if hover else COLOR_BTN
    pygame.draw.rect(screen, color, rect, border_radius=6)
    surf = font_sm.render(label, True, COLOR_WHITE)
    r    = surf.get_rect(center=rect.center)
    screen.blit(surf, r)

def truncate(text, max_chars):
    return text if len(text) <= max_chars else text[:max_chars - 1] + "…"

# DRAWING FUNCTIONS
def draw_hud(elapsed_seconds):
    pygame.draw.rect(screen, COLOR_HUD, (0, 0, WINDOW_WIDTH, HUD_HEIGHT))
    screen.blit(font.render(f"Mines: {count_mines()}", True, COLOR_WHITE), (20, 18))
    screen.blit(font.render(f"Time: {elapsed_seconds}s", True, COLOR_WHITE), (GRID_WIDTH - 180, 18))
    if game_over:
        msg   = "YOU WIN!  R to restart" if won else "GAME OVER  R to restart"
        color = (80, 220, 80) if won else COLOR_RED
        surf  = font.render(msg, True, color)
        screen.blit(surf, surf.get_rect(center=(GRID_WIDTH // 2, HUD_HEIGHT // 2)))

def draw_grid():
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            cell = grid.getCell(r, c)
            rect = pygame.Rect(c * CELL_SIZE, HUD_HEIGHT + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if r == cursor_row and c == cursor_col and not game_over:
                bg = COLOR_CURSOR
            elif cell.isCovered:
                bg = COLOR_COVERED
            elif cell.isMine:
                bg = COLOR_MINE
            else:
                bg = COLOR_UNCOVERED
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, COLOR_GRID_LINE, rect, 1)
            if flagged[r][c] and cell.isCovered:
                s = font.render("F", True, COLOR_FLAG)
                screen.blit(s, s.get_rect(center=rect.center))
            elif not cell.isCovered:
                if cell.isMine:
                    s = font.render("*", True, COLOR_WHITE)
                    screen.blit(s, s.get_rect(center=rect.center))
                elif cell.weight > 0:
                    s = font.render(str(cell.weight), True, WEIGHT_COLORS.get(cell.weight, COLOR_WHITE))
                    screen.blit(s, s.get_rect(center=rect.center))

def draw_sidebar(mouse_pos):
    # background
    pygame.draw.rect(screen, COLOR_SIDEBAR, (GRID_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, COLOR_BTN, (GRID_WIDTH, 0), (GRID_WIDTH, WINDOW_HEIGHT), 2)

    # title
    screen.blit(font_sm.render("♪ NOW PLAYING", True, COLOR_ACCENT), (SB_X, HUD_HEIGHT - 30))

    # track name (truncated to fit)
    if playlist:
        name = os.path.splitext(os.path.basename(playlist[track_index]))[0]
        screen.blit(font_xs.render(truncate(name, 22), True, COLOR_WHITE), (SB_X, HUD_HEIGHT - 12))
        idx_str = f"{track_index + 1} / {len(playlist)}"
    else:
        screen.blit(font_xs.render("No tracks found", True, COLOR_RED), (SB_X, HUD_HEIGHT - 12))
        idx_str = "0 / 0"

    screen.blit(font_xs.render(idx_str, True, (160, 160, 160)), (SB_X, HUD_HEIGHT + 4))

    # buttons
    play_label = "Pause" if (pygame.mixer.music.get_busy() and not music_paused) else "Play"
    draw_button(BTN_PREV,   "Previous Song",  BTN_PREV.collidepoint(mouse_pos))
    draw_button(BTN_PLAY,   play_label,  BTN_PLAY.collidepoint(mouse_pos))
    draw_button(BTN_NEXT,   "Next Song",  BTN_NEXT.collidepoint(mouse_pos))

    # shuffle
    shuf_color = COLOR_ACCENT if shuffle_on else COLOR_WHITE
    shuf_label = "Shuffle ON" if shuffle_on else "Shuffle OFF"
    pygame.draw.rect(screen, COLOR_BTN_HOVER if BTN_SHUFFLE.collidepoint(mouse_pos) else COLOR_BTN, BTN_SHUFFLE, border_radius=6)
    shuf_surf = font_sm.render(shuf_label, True, shuf_color)
    screen.blit(shuf_surf, shuf_surf.get_rect(center=BTN_SHUFFLE.center))

    # volume
    screen.blit(font_sm.render(f"Vol: {int(volume * 100)}%", True, COLOR_WHITE), (SB_X, HUD_HEIGHT + 186))
    draw_button(BTN_VOL_UP, "Vol +", BTN_VOL_UP.collidepoint(mouse_pos))
    draw_button(BTN_VOL_DN, "Vol -", BTN_VOL_DN.collidepoint(mouse_pos))

    # volume bar
    bar_rect = pygame.Rect(SB_X, HUD_HEIGHT + 272, SB_W, 8)
    pygame.draw.rect(screen, COLOR_BTN, bar_rect, border_radius=4)
    filled = pygame.Rect(SB_X, HUD_HEIGHT + 272, int(SB_W * volume), 8)
    pygame.draw.rect(screen, COLOR_ACCENT, filled, border_radius=4)

# MAIN GAME LOOP
running = True
while running:
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    mouse_pos = pygame.mouse.get_pos()

    # keep cursor synced to mouse when hovering over the grid
    mx, my = mouse_pos
    if my > HUD_HEIGHT and mx < GRID_WIDTH:
        hover_row, hover_col = pixel_to_cell(mx, my)
        if 0 <= hover_row < NUM_ROWS and 0 <= hover_col < NUM_COLS:
            cursor_row, cursor_col = hover_row, hover_col

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == MUSIC_END:
            next_track()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                grid, flagged, start_ticks, game_over, won, first_click = new_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # sidebar buttons
            if mx >= GRID_WIDTH:
                if BTN_PREV.collidepoint(mx, my):
                    prev_track()
                elif BTN_PLAY.collidepoint(mx, my):
                    toggle_pause()
                elif BTN_NEXT.collidepoint(mx, my):
                    next_track()
                elif BTN_SHUFFLE.collidepoint(mx, my):
                    toggle_shuffle()
                elif BTN_VOL_UP.collidepoint(mx, my):
                    set_volume(volume + 0.1)
                elif BTN_VOL_DN.collidepoint(mx, my):
                    set_volume(volume - 0.1)

            # grid clicks
            elif my > HUD_HEIGHT:
                row, col = pixel_to_cell(mx, my)
                if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
                    reveal(row, col)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = event.pos
            if my > HUD_HEIGHT and mx < GRID_WIDTH:
                row, col = pixel_to_cell(mx, my)
                if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
                    toggle_flag(row, col)

        if event.type == pygame.JOYBUTTONDOWN:
            print(f"[Controller] Button {event.button} pressed")
            if event.button == 0:
                reveal(cursor_row, cursor_col)
            elif event.button == 1:
                toggle_flag(cursor_row, cursor_col)
            elif event.button == 7:
                grid, flagged, start_ticks, game_over, won, first_click = new_game()

        if event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            cursor_col = max(0, min(NUM_COLS - 1, cursor_col + hat_x))
            cursor_row = max(0, min(NUM_ROWS - 1, cursor_row - hat_y))

    # IN-LOOP DRAWING
    screen.fill(COLOR_BG)
    draw_grid()
    draw_hud(elapsed_seconds)
    draw_sidebar(mouse_pos)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()