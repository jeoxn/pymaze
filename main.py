import pygame
import random

class Maze:
    def __init__(self, width:int=10, height:int=10, cell_size:int=20) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.maze = [[{'top': True, 'bottom': True, 'left': True, 'right': True} for _ in range(width)] for _ in range(height)]
        self.stack = [(0, 0)]
        self.visited = [(0, 0)]
        self.maze[0][0]['top'] = False  # Entrance
        self.generate_maze()

    def get_maze(self) -> list:
        return self.maze

    def get_neighbors(self, x:int, y:int) -> list:
        neighbors = []
        if x > 0:
            neighbors.append((x-1, y))
        if y > 0:
            neighbors.append((x, y-1))
        if x < self.width - 1:
            neighbors.append((x+1, y))
        if y < self.height - 1:
            neighbors.append((x, y+1))
        return random.sample(neighbors, len(neighbors))

    def remove_wall(self, current:tuple, next:tuple) -> None:
        cx, cy = current
        nx, ny = next
        if nx == cx + 1:  # next is to the right of current
            self.maze[cy][cx]['right'] = False
            self.maze[ny][nx]['left'] = False
        elif nx == cx - 1:  # next is to the left of current
            self.maze[cy][cx]['left'] = False
            self.maze[ny][nx]['right'] = False
        elif ny == cy + 1:  # next is below current
            self.maze[cy][cx]['bottom'] = False
            self.maze[ny][nx]['top'] = False
        elif ny == cy - 1:  # next is above current
            self.maze[cy][cx]['top'] = False
            self.maze[ny][nx]['bottom'] = False

    def generate_maze(self) -> None:
        self.maze = [[{'top': True, 'bottom': True, 'left': True, 'right': True} for _ in range(self.width)] for _ in range(self.height)]
        self.stack = [(0, 0)]
        self.visited = [(0, 0)]
        self.maze[0][0]['top'] = False  # Entrance
        
        while self.stack:
            x, y = self.stack[-1]
            neighbors = self.get_neighbors(x, y)
            found = False
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    self.stack.append(neighbor)
                    self.remove_wall((x, y), neighbor)
                    found = True
                    break
            if not found:
                self.stack.pop()

    def draw_maze(self, screen: pygame.Surface) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]
                top_left = (x * self.cell_size, y * self.cell_size)
                top_right = ((x + 1) * self.cell_size, y * self.cell_size)
                bottom_left = (x * self.cell_size, (y + 1) * self.cell_size)
                bottom_right = ((x + 1) * self.cell_size, (y + 1) * self.cell_size)

                if cell['top']:
                    pygame.draw.line(screen, (255, 255, 255), top_left, top_right)
                if cell['bottom']:
                    pygame.draw.line(screen, (255, 255, 255), bottom_left, bottom_right)
                if cell['left']:
                    pygame.draw.line(screen, (255, 255, 255), top_left, bottom_left)
                if cell['right']:
                    pygame.draw.line(screen, (255, 255, 255), top_right, bottom_right)

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (rect[0] + 10, rect[1] + 10))

def main():
    pygame.init()
    cell_size = 25
    width, height = 25, 25
    screen_width, screen_height = width * cell_size, height * cell_size + 50
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Generator")

    maze = Maze(width, height, cell_size)
    button_rect = pygame.Rect(10, screen_height - 40, 100, 30)
    player_pos = [0, 0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    maze.generate_maze()
                    player_pos = [0, 0]
            elif event.type == pygame.KEYDOWN:
                x, y = player_pos
                if event.key == pygame.K_UP and y > 0 and not maze.maze[y][x]['top']:
                    player_pos = [x, y - 1]
                elif event.key == pygame.K_DOWN and y < height - 1 and not maze.maze[y][x]['bottom']:
                    player_pos = [x, y + 1]
                elif event.key == pygame.K_LEFT and x > 0 and not maze.maze[y][x]['left']:
                    player_pos = [x - 1, y]
                elif event.key == pygame.K_RIGHT and x < width - 1 and not maze.maze[y][x]['right']:
                    player_pos = [x + 1, y]
                if player_pos == [width - 1, height - 1]:
                    maze.generate_maze()
                    player_pos = [0, 0]

        screen.fill((0, 0, 0))
        maze.draw_maze(screen)
        pygame.draw.circle(screen, (0, 0, 255), (player_pos[0] * cell_size + cell_size // 2 + 1, player_pos[1] * cell_size + cell_size // 2 + 1), cell_size // 2 - 4)
        draw_button(screen, "Shuffle", button_rect, (0, 128, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
