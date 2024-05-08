import pygame
import sys
from queue import Queue

command_queue = Queue()

class Ship:
    def __init__(self, name, ship_status, position, facing, speed):
        self.name = name
        self.ship_status = ship_status
        self.position = position
        self.facing = facing
        self.speed = speed
        self.rect = pygame.Rect(position[0], position[1], 20, 20)

    def move(self, direction, game_instance):
        new_position = self.position
        if direction == 'UP':
            new_position = (self.position[0], self.position[1] - self.speed)
        elif direction == 'DOWN':
            new_position = (self.position[0], self.position[1] + self.speed)
        elif direction == 'LEFT':
            new_position = (self.position[0] - self.speed, self.position[1])
        elif direction == 'RIGHT':
            new_position = (self.position[0] + self.speed, self.position[1])

        if game_instance.is_valid_move(self, new_position):
            self.position = new_position
            self.rect.update(self.position[0], self.position[1], 20, 20)

class Game:
    def __init__(self):
        self.ships = {}
        self.initialize_pygame()
        self.create_ships()

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def create_ships(self):
        ship1 = Ship("Enterprise", "active", (400, 300), "NORTH", 10)
        ship2 = Ship("Voyager", "active", (200, 150), "SOUTH", 10)
        self.add_ship(ship1)
        self.add_ship(ship2)

    def add_ship(self, ship):
        self.ships[ship.name] = ship

    def is_valid_move(self, ship, new_position):
        test_rect = pygame.Rect(new_position[0], new_position[1], 20, 20)
        for other_ship in self.ships.values():
            if other_ship != ship and other_ship.rect.colliderect(test_rect):
                return False
        return True

    def run(self):
        while True:
            self.handle_commands()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((10, 10, 40))
            for ship in self.ships.values():
                pygame.draw.rect(self.screen, (0, 255, 0) if ship.name == "Enterprise" else (255, 0, 0), ship.rect)
            pygame.display.flip()
            self.clock.tick(60)

    def handle_commands(self):
        while not command_queue.empty():
            ship_name, command = command_queue.get()
            ship = self.ships.get(ship_name)
            if ship:
                ship.move(command, self)
