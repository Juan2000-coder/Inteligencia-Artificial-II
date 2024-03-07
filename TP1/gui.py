import pygame
import sys

# Tamaño de la ventana
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Tamaño del tablero
ROWS = 10
COLS = 10

# Tamaño de las celdas
CELL_SIZE = WINDOW_WIDTH // COLS, WINDOW_HEIGHT // ROWS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def draw_grid(screen):
    # Dibujar cuadrícula
    for x in range(0, WINDOW_WIDTH, CELL_SIZE[0]):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE[1]):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_start_and_end(screen, start, end):
    # Dibujar punto de inicio y fin
    pygame.draw.rect(screen, GREEN, (start[0] * CELL_SIZE[0], start[1] * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]))
    if end is not None:
        pygame.draw.rect(screen, RED, (end[0] * CELL_SIZE[0], end[1] * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1]))

def print_matrix(start, end):
    # Crear matriz
    matrix = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            if (x, y) == start:
                row.append("S")
            elif (x, y) == end:
                row.append("E")
            else:
                row.append("-")
        matrix.append(row)
    
    return matrix

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Selecciona punto de partida y llegada")
    clock = pygame.time.Clock()

    start = None
    end = None
    selected = None

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(screen)
        if start:
            draw_start_and_end(screen, start, end)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener la celda seleccionada por el usuario
                mouse_pos = pygame.mouse.get_pos()
                cell_x = mouse_pos[0] // CELL_SIZE[0]
                cell_y = mouse_pos[1] // CELL_SIZE[1]
                selected = (cell_x, cell_y)
                if not start:
                    start = selected
                elif selected != start and selected != end:
                    end = selected
                    draw_start_and_end(screen, start, end)

        pygame.display.flip()
        clock.tick(60)

        if end is not None:
            pygame.time.delay(1000)
            break

    pygame.quit()
    matrix = print_matrix(start, end)
    return matrix, (start, end)

if __name__ == "__main__":
    matrix, points = main()
    print("Matriz:")
    for row in matrix:
        print(" ".join(row))
    print("Puntos de inicio y llegada:", points)
    sys.exit()
