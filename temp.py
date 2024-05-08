import pygame
import sys

class Ship:
    def __init__(self, name, ship_status, position, facing, speed):
        self.name = name
        self.ship_status = ship_status
        self.position = position  # Grid coordinates (x, y)
        self.facing = facing
        self.speed = speed
        self.rect = pygame.Rect(position[0], position[1], 20, 20)

    def move(self, direction, is_valid_move):
        new_position = self.position
        if direction == 'UP':
            new_position = (self.position[0], self.position[1] - self.speed)
        elif direction == 'DOWN':
            new_position = (self.position[0], self.position[1] + self.speed)
        elif direction == 'LEFT':
            new_position = (self.position[0] - self.speed, self.position[1])
        elif direction == 'RIGHT':
            new_position = (self.position[0] + self.speed, self.position[1])

        if is_valid_move(self, new_position):
            self.position = new_position
            self.rect.update(self.position[0], self.position[1], 20, 20)


class Game:
    def __init__(self):
        self.ships = {}

    def add_ship(self, ship):
        self.ships[ship.name] = ship

    def get_ship_info(self, name):
        return self.ships.get(name, None)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Creating two ships
ship1 = Ship("Enterprise", "active", (400, 300), "NORTH", 10)
ship2 = Ship("Voyager", "active", (200, 150), "SOUTH", 10)

game = Game()
game.add_ship(ship1)
game.add_ship(ship2)

def is_valid_move(ship, new_position):
        test_rect = pygame.Rect(new_position[0], new_position[1], 20, 20)
        for other_ship in game.ships.values():
            if other_ship != ship and other_ship.rect.colliderect(test_rect):
                return False
        return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship1.move('UP', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key == pygame.K_DOWN:
                ship1.move('DOWN', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key == pygame.K_LEFT:
                ship1.move('LEFT', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key == pygame.K_RIGHT:
                ship1.move('RIGHT', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key == pygame.K_w:
                ship2.move('UP', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key is pygame.K_s:
                ship2.move('DOWN', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key is pygame.K_a:
                ship2.move('LEFT', lambda ship, pos: is_valid_move(ship, pos))
            elif event.key is pygame.K_d:
                ship2.move('RIGHT', lambda ship, pos: is_valid_move(ship, pos))
            

    screen.fill((10, 10, 40))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(ship1.position[0], ship1.position[1], 20, 20))  # Draw ship1
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(ship2.position[0], ship2.position[1], 20, 20))  # Draw ship2
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second
