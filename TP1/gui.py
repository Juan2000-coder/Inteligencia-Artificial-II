import pygame
import sys


class Interfaz:
    def __init__(self):
        self.WIDTH = None
        self.HEIGHT = None
        self.COLS = None
        self.ROWS = None
        self.CELL_SIZE = (20, 20)

        self.UNIT_MATRIX = [
            ["0", "0", "0", "0"],
            ["0", "1", "1", "0"],
            ["0", "1", "1", "0"],
            ["0", "1", "1", "0"],
            ["0", "1", "1", "0"],
            ["0", "0", "0", "0"]
        ]


        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)


    def draw_grid(self, screen, rows, cols):
        # Dibujar cuadrícula
        for x in range(0, rows, self.CELL_SIZE[0]):
            pygame.draw.line(screen, self.GRAY, (x, 0), (x, rows))
        for y in range(0, cols, self.CELL_SIZE[1]):
            pygame.draw.line(screen, self.GRAY, (0, y), (cols, y))


    def draw_start_and_end(self,screen, start, end):
        # Dibujar punto de inicio y fin si existen
        if start is not None:
            pygame.draw.rect(screen, self.GREEN, (start[0] * self.CELL_SIZE[0], start[1] * self.CELL_SIZE[1], self.CELL_SIZE[0], self.CELL_SIZE[1]))
        if end is not None:
            pygame.draw.rect(screen, self.RED, (end[0] * self.CELL_SIZE[0], end[1] * self.CELL_SIZE[1], self.CELL_SIZE[0], self.CELL_SIZE[1]))


    def print_matrix(self, start, end):
        # Crear matriz
        matrix = []
        for y in range(self.ROWS):
            row = []
            for x in range(self.COLS):
                if (x, y) == start:
                    row.append("S")
                elif (x, y) == end:
                    row.append("E")
                else:
                    row.append("0")
            matrix.append(row)
        
        return matrix


    def multiply_matrix(self, matrix, rows, cols, units_x, units_y):
        # Multiplicar la matriz básica por la cantidad de unidades en filas y columnas
        multiplied_matrix = []
        for _ in range(units_y):
            for row in matrix:
                multiplied_matrix.append(row * units_x)
        
        return multiplied_matrix

    def draw_basic_unit(self, screen, x, y):
        # Dibujar una unidad básica en la posición (x, y) del tablero
        for j in range(len(self.UNIT_MATRIX)):
            for i in range(len(self.UNIT_MATRIX[0])):
                color = self.BLACK if self.UNIT_MATRIX[j][i] == "1" else self.WHITE
                pygame.draw.rect(screen, color, ((x + i) * self.CELL_SIZE[0], (y + j) * self.CELL_SIZE[1], self.CELL_SIZE[0], self.CELL_SIZE[1]))

    def draw_board(self, screen, units_x, units_y):
        # Dibujar el tablero completo
        for j in range(units_y):
            for i in range(units_x):
                self.draw_basic_unit(screen, i * len(self.UNIT_MATRIX[0]), j * len(self.UNIT_MATRIX[0]))


    def main(self):
        units_x = None
        units_y = None
        running = True
        start = None
        end = None
        selected = None

        while units_x is None or units_x < 1:
            try:
                units_x = int(input("Ingrese la cantidad de unidades de estanterías en columnas: "))
            except ValueError:
                print("Ingrese un número válido.")

        while units_y is None or units_y < 1:
            try:
                units_y = int(input("Ingrese la cantidad de unidades de estanterías en filas: "))
            except ValueError:
                print("Ingrese un número válido.")

        self.ROWS = units_y * len(self.UNIT_MATRIX)
        self.COLS = units_x * len(self.UNIT_MATRIX[0])
        self.WIDTH = self.COLS * self.CELL_SIZE[0]
        self.HEIGHT = self.ROWS * self.CELL_SIZE[1]

        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Selecciona punto de partida y llegada")
        clock = pygame.time.Clock()


        while running:
            screen.fill(self.WHITE)
            self.draw_board(screen, units_x, units_y)
            self.draw_grid(screen, self.ROWS, self.COLS)
            self.draw_start_and_end(screen, start, end)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Obtener la celda seleccionada por el usuario
                    mouse_pos = pygame.mouse.get_pos()
                    cell_x = mouse_pos[0] // self.CELL_SIZE[0]
                    cell_y = mouse_pos[1] // self.CELL_SIZE[1]
                    selected = (cell_x, cell_y)
                    if not start:
                        start = selected
                    elif selected != start and selected != end:
                        end = selected
                        self.draw_start_and_end(screen, start, end)

            pygame.display.flip()
            clock.tick(60)

            if end is not None:
                pygame.time.delay(1000)
                break

        pygame.quit()
        matrix = self.print_matrix(start, end)
        filas, columnas = len(matrix), len(matrix[0])
        multiplied_matrix = self.multiply_matrix(self.UNIT_MATRIX, filas, columnas, units_x, units_y)
        return multiplied_matrix, (start, end)


if __name__ == "__main__":
    matrix, points = Interfaz().main()
    print("Matriz:")
    for row in matrix:
        print(" ".join(row))
    print("Puntos de inicio y llegada:", points)
    sys.exit()
