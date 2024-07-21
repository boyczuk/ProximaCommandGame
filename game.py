import pygame
import sys
from queue import Queue
import math
import time

command_queue = Queue()

class Ship:
    def __init__(self, name, team, position, facing, speed):
        self.name = name
        self.team = team
        self.position = list(position)
        self.facing = facing  # Facing direction in degrees (0 = East, 90 = North, 180 = West, 270 = South)
        self.speed = speed  # Current speed (0 = Stop, 1 = Partial, 2 = Full)
        self.max_speed = 2  # Maximum speed, adjusted to be slower
        self.health = 5
        self.shields_up = False  # Indicates if shields are raised
        self.shield_raised_time = 0  # Timestamp when shields were raised
        self.shield_cooldown = False  # Indicates if shields are in cooldown
        self.rect = pygame.Rect(position[0], position[1], 20, 20)
        self.selected = False  # Indicates if the ship is selected

    def move(self, screen_width, screen_height):
        if self.speed > 0:
            rad = math.radians(self.facing)
            dx = self.max_speed * self.speed * math.cos(rad) / 5
            dy = -self.max_speed * math.sin(rad) * self.speed / 5  # Negative because Pygame's y-axis is inverted
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy

            # Boundary check
            if 0 <= new_x <= screen_width - 20 and 0 <= new_y <= screen_height - 20:
                self.position[0] = new_x
                self.position[1] = new_y
                self.rect.update(self.position[0], self.position[1], 20, 20)

    def distance_to(self, other_ship):
        return math.sqrt((self.position[0] - other_ship.position[0]) ** 2 + (self.position[1] - other_ship.position[1]) ** 2)

    def decrease_health(self):
        if self.shields_up:
            print(f"{self.name} was hit but shields absorbed the damage!")
        else:
            self.health -= 1
            print(f"{self.name} has been hit! Health: {self.health}")

    def change_direction(self, angle):
        self.facing = (self.facing + angle) % 360

    def toggle_shields(self):
        current_time = time.time()
        if not self.shield_cooldown:
            if not self.shields_up:
                self.shields_up = True
                self.shield_raised_time = current_time
                self.shield_cooldown = True  # Start cooldown
            else:
                self.shields_up = False

    def update_shields(self):
        current_time = time.time()
        if self.shields_up and current_time - self.shield_raised_time >= 3:  # Shields last for 3 seconds
            self.shields_up = False
        if self.shield_cooldown and not self.shields_up:
            if current_time - self.shield_raised_time >= 8:  # Cooldown period of 5 seconds after shields go down
                self.shield_cooldown = False

    def draw(self, screen):
        # Draw the ship rectangle
        color = (0, 255, 0) if self.team == "green" else (0, 0, 255)
        pygame.draw.rect(screen, color, self.rect)

        # Draw the facing triangle
        rad = math.radians(self.facing)
        tip = (self.position[0] + 10 * math.cos(rad), self.position[1] - 10 * math.sin(rad))
        left = (self.position[0] + 5 * math.cos(rad + 2.5), self.position[1] - 5 * math.sin(rad + 2.5))
        right = (self.position[0] + 5 * math.cos(rad - 2.5), self.position[1] - 5 * math.sin(rad - 2.5))
        pygame.draw.polygon(screen, (255, 255, 0), [tip, left, right])

        # Draw selection circle if selected
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 25, 2)

        # Draw shields if raised
        if self.shields_up:
            pygame.draw.circle(screen, (0, 0, 255), self.rect.center, 25, 2)

class Game:
    def __init__(self):
        self.ships = {}
        self.screen_width = 400
        self.screen_height = 300
        self.initialize_pygame()
        self.create_ships()
        self.selected_target = None

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Smaller map
        self.clock = pygame.time.Clock()

    def create_ships(self):
        ship1 = Ship("Enterprise", "green", (100, 50), 90, 0)  # Facing north, speed stopped
        ship2 = Ship("Voyager", "green", (100, 75), 270, 0)     # Facing south, speed stopped
        ship3 = Ship("Voq'leth", "blue", (200, 150), 90, 0) 
        ship4 = Ship("Negh'Var", "blue", (200, 100), 270, 0) 
        self.add_ship(ship1)
        self.add_ship(ship2)
        self.add_ship(ship3)
        self.add_ship(ship4)

    def add_ship(self, ship):
        self.ships[ship.name] = ship

    def is_valid_move(self, ship, new_position):
        test_rect = pygame.Rect(new_position[0], new_position[1], 20, 20)
        for other_ship in self.ships.values():
            if other_ship != ship and other_ship.rect.colliderect(test_rect):
                return False
        return True

    def get_targetable_enemies(self, player_ship_name, radius):
        targetable_enemies = []
        player_ship = self.ships[player_ship_name]
        for ship_name, ship in self.ships.items():
            if ship_name != player_ship_name and player_ship.distance_to(ship) <= radius:
                targetable_enemies.append(ship_name)
        return targetable_enemies

    def run(self):
        while True:
            self.handle_commands()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((10, 10, 40))
            for ship in self.ships.values():
                ship.move(self.screen_width, self.screen_height)  # Move the ship based on its speed and direction
                ship.update_shields()  # Update shields status
                ship.draw(self.screen)  # Draw the ship with its facing direction
                self.display_health(ship)
            pygame.display.flip()
            self.clock.tick(60)

    def handle_commands(self):
        while not command_queue.empty():
            ship_name, command = command_queue.get()
            ship = self.ships.get(ship_name)
            if ship:
                if command.startswith("FIRE"):
                    _, target_name = command.split()
                    self.fire_weapon(ship, target_name)
                elif command in ("STOP", "PARTIAL", "FULL"):
                    self.adjust_speed(ship, command)
                elif command in ("LEFT", "RIGHT"):
                    self.change_direction(ship, command)
                elif command == "TOGGLE_SHIELDS":
                    ship.toggle_shields()
                elif command.startswith("SELECT"):
                    _, target_name = command.split()
                    self.select_target(target_name)

    def adjust_speed(self, ship, command):
        if command == "STOP":
            ship.speed = 0
        elif command == "PARTIAL":
            ship.speed = 1
        elif command == "FULL":
            ship.speed = 2

    def change_direction(self, ship, command):
        if command == "LEFT":
            ship.change_direction(15)  # Turn left by 15 degrees
        elif command == "RIGHT":
            ship.change_direction(-15)  # Turn right by 15 degrees

    def fire_weapon(self, attacking_ship, target_name):
        if target_name in self.ships:
            target_ship = self.ships[target_name]
            if attacking_ship.distance_to(target_ship) <= 100:  # Assuming 100 is the max range
                target_ship.decrease_health()
            else:
                print(f"Target {target_name} is out of range.")

    def select_target(self, target_name):
        if self.selected_target:
            self.ships[self.selected_target].selected = False  # Deselect previous target
        if target_name in self.ships:
            self.ships[target_name].selected = True
            self.selected_target = target_name

    def display_health(self, ship):
        font = pygame.font.Font(None, 36)
        text = font.render(f"HP: {ship.health}", True, (255, 255, 255))
        self.screen.blit(text, (ship.position[0], ship.position[1] - 20))
