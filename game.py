import pygame
import sys
from queue import Queue
import math
import time
import random
import threading

command_queue = Queue()

class PowerUp:
    def __init__(self, type, position):
        self.type = type
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 20, 20)
        self.collected = False

    def draw(self, screen):
        if self.type == "power_cell":
            color = (255, 255, 0)
        elif self.type == "torpedo":
            color = (255, 0, 0)
        elif self.type == "engineer":
            color = (0, 255, 0)
        pygame.draw.rect(screen, color, self.rect)

class Ship:
    def __init__(self, name, team, position, facing, speed):
        self.name = name
        self.team = team
        self.position = list(position)
        self.facing = facing
        self.speed = speed
        self.max_speed = 2
        self.health = 5
        self.shields_up = False
        self.shield_raised_time = 0
        self.shield_cooldown = False
        self.rect = pygame.Rect(position[0], position[1], 20, 20)
        self.selected = False
        self.deactivated = False
        self.disabled_consoles = {"helm": False, "shields": False, "weapons": False}
        self.repairing = False
        self.repair_cooldowns = {"helm": 0, "shields": 0, "weapons": 0}
        self.power = 100
        self.max_power = 100
        self.power_cooldown = False
        self.torpedo_powerup = False
        self.repair_rate_multiplier = 1
        self.collision_cooldown = 0
        self.collected_powerups = []  # New attribute to store collected power-ups

    def move(self, screen_width, screen_height):
        if self.deactivated or self.disabled_consoles["helm"] or self.power <= 0:
            return
        if self.speed > 0:
            power_cost = 0.01 if self.speed == 1 else 0.02
            if self.consume_power(power_cost):
                rad = math.radians(self.facing)
                dx = self.max_speed * self.speed * math.cos(rad) / 5
                dy = -self.max_speed * math.sin(rad) * self.speed / 5
                new_x = self.position[0] + dx
                new_y = self.position[1] + dy

                # Boundary check
                if 0 <= new_x <= screen_width - 20 and 0 <= new_y <= screen_height - 20:
                    self.position[0] = new_x
                    self.position[1] = new_y
                    self.rect.update(self.position[0], self.position[1], 20, 20)

    def distance_to(self, other_ship):
        return math.sqrt((self.position[0] - other_ship.position[0]) ** 2 + (self.position[1] - other_ship.position[1]) ** 2)

    def decrease_health(self, damage):
        if self.shields_up:
            print(f"{self.name} was hit but shields absorbed the damage!")
        else:
            if self.health > 0:
                self.health -= damage
                print(f"{self.name} has been hit! Health: {self.health}")
                if self.health <= 0:
                    self.deactivate()
                else:
                    self.disable_random_console()

    def change_direction(self, angle):
        if self.deactivated or self.disabled_consoles["helm"] or self.power <= 0:
            return
        if self.consume_power(1):
            self.facing = (self.facing + angle) % 360

    def toggle_shields(self):
        if self.deactivated or self.disabled_consoles["shields"] or self.power <= 0:
            return
        current_time = time.time()
        if not self.shield_cooldown:
            if not self.shields_up:
                if self.consume_power(3):
                    self.shields_up = True
                    self.shield_raised_time = current_time
                    self.shield_cooldown = True
            else:
                self.shields_up = False

    def update_shields(self):
        current_time = time.time()
        if self.shields_up and current_time - self.shield_raised_time >= 3:
            self.shields_up = False
        if self.shield_cooldown and not self.shields_up:
            if current_time - self.shield_raised_time >= 8:
                self.shield_cooldown = False

    def disable_random_console(self):
        if not self.repairing:
            console = random.choice(["helm", "shields", "weapons", "none"])
            if console != "none":
                self.disabled_consoles[console] = True
                print(f"{self.name} had its {console} console disabled!")

    def repair_console(self, console):
        current_time = time.time()
        if self.disabled_consoles[console] and not self.repairing and current_time - self.repair_cooldowns[console] >= 60:
            self.repairing = True
            print(f"Repairing {console} console on {self.name}...")
            if self.consume_power(5):
                repair_time = 3 / self.repair_rate_multiplier
                time.sleep(repair_time)
                self.disabled_consoles[console] = False
                self.health += 1
                self.repair_cooldowns[console] = current_time
                self.repairing = False
                print(f"{console} console on {self.name} has been repaired and health restored!")
            else:
                self.repairing = False
                print(f"Not enough power to repair {console} console on {self.name}.")

    def fire_weapon(self, target_ship):
        if self.torpedo_powerup:
            target_ship.decrease_health(2)
            self.torpedo_powerup = False
        else:
            target_ship.decrease_health(1)

    def restore_power(self):
        if not self.power_cooldown:
            print(f"Restoring power on {self.name}...")
            self.power = self.max_power
            self.power_cooldown = True
            time.sleep(5)
            self.power_cooldown = False
            print(f"Power restored on {self.name}.")

    def consume_power(self, amount):
        if self.power >= amount:
            self.power -= amount
            return True
        return False

    def deactivate(self):
        self.deactivated = True
        self.speed = 0
        self.shields_up = False
        print(f"{self.name} has been deactivated!")

    def activate_powerup(self, powerup_type):
        if powerup_type == "power_cell":
            self.max_power = 150
            self.power = 150
        elif powerup_type == "torpedo":
            self.torpedo_powerup = True
        elif powerup_type == "engineer":
            self.repair_rate_multiplier = 2
        print(f"{self.name} activated {powerup_type} power-up!")

    def draw(self, screen):
        if self.deactivated:
            color = (100, 100, 100)
        else:
            color = (0, 255, 0) if self.team == "green" else (0, 0, 255)
        pygame.draw.rect(screen, color, self.rect)

        rad = math.radians(self.facing)
        tip = (self.position[0] + 10 * math.cos(rad), self.position[1] - 10 * math.sin(rad))
        left = (self.position[0] + 5 * math.cos(rad + 2.5), self.position[1] - 5 * math.sin(rad + 2.5))
        right = (self.position[0] + 5 * math.cos(rad - 2.5), self.position[1] - 5 * math.sin(rad - 2.5))
        pygame.draw.polygon(screen, (255, 255, 0), [tip, left, right])

        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 25, 2)

        if self.shields_up:
            pygame.draw.circle(screen, (0, 0, 255), self.rect.center, 25, 2)

class Game:
    def __init__(self):
        self.ships = {}
        self.screen_width = 400
        self.screen_height = 300
        self.powerups = []
        self.initialize_pygame()
        self.create_ships()
        self.create_powerups()
        self.selected_target = None

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def create_ships(self):
        ship1 = Ship("Enterprise", "green", (100, 50), 90, 0)
        ship2 = Ship("Voyager", "green", (100, 75), 270, 0)
        ship3 = Ship("Voq'leth", "blue", (200, 150), 90, 0)
        ship4 = Ship("Negh'Var", "blue", (200, 100), 270, 0)
        self.add_ship(ship1)
        self.add_ship(ship2)
        self.add_ship(ship3)
        self.add_ship(ship4)

    def add_ship(self, ship):
        self.ships[ship.name] = ship

    def create_powerups(self):
        powerup_types = ["power_cell", "torpedo", "engineer"]
        num_powerups = random.randint(1,5)
        for _ in range(num_powerups):
            powerup_type = random.choice(powerup_types)
            position = (random.randint(0, self.screen_width - 20), random.randint(0, self.screen_height - 20))
            powerup = PowerUp(powerup_type, position)
            self.powerups.append(powerup)

    def check_powerup_collisions(self):
        for ship in self.ships.values():
            for powerup in self.powerups:
                if not powerup.collected and ship.rect.colliderect(powerup.rect):
                    ship.collected_powerups.append(powerup.type)
                    powerup.collected = True
                    print(f"{ship.name} collected a {powerup.type} power-up!")

    def check_ship_collisions(self):
        current_time = time.time()
        ships = list(self.ships.values())
        for i in range(len(ships)):
            for j in range(i + 1, len(ships)):
                if ships[i].rect.colliderect(ships[j].rect):
                    if ships[i].health > 0 and ships[j].health > 0:
                        if current_time - ships[i].collision_cooldown > 1 and current_time - ships[j].collision_cooldown > 1:
                            ships[i].decrease_health(1)
                            ships[j].decrease_health(1)
                            ships[i].collision_cooldown = current_time
                            ships[j].collision_cooldown = current_time
                            print(f"Collision detected between {ships[i].name} and {ships[j].name}")

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
                ship.move(self.screen_width, self.screen_height)
                ship.update_shields()
                ship.draw(self.screen)
                self.display_health(ship)
            for powerup in self.powerups:
                if not powerup.collected:
                    powerup.draw(self.screen)
            self.check_powerup_collisions()
            self.check_ship_collisions()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_commands(self):
        while not command_queue.empty():
            ship_name, command = command_queue.get()
            ship = self.ships.get(ship_name)
            if ship and not ship.deactivated:
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
                elif command.startswith("REPAIR"):
                    _, console = command.split()
                    threading.Thread(target=ship.repair_console, args=(console,)).start()
                elif command.startswith("ACTIVATE"):
                    _, powerup_type = command.split()
                    threading.Thread(target=ship.activate_powerup, args=(powerup_type,)).start()
                elif command == "RESTORE_POWER":
                    threading.Thread(target=ship.restore_power).start()

    def adjust_speed(self, ship, command):
        if command == "STOP":
            ship.speed = 0
        elif command == "PARTIAL":
            ship.speed = 1
        elif command == "FULL":
            ship.speed = 2

    def change_direction(self, ship, command):
        if command == "LEFT":
            ship.change_direction(15)
        elif command == "RIGHT":
            ship.change_direction(-15)

    def fire_weapon(self, attacking_ship, target_name):
        if attacking_ship.disabled_consoles["weapons"] or attacking_ship.power <= 0:
            print(f"{attacking_ship.name}'s weapons are disabled or no power!")
            return
        if target_name in self.ships:
            if attacking_ship.consume_power(2):
                target_ship = self.ships[target_name]
                if attacking_ship.distance_to(target_ship) <= 100:
                    attacking_ship.fire_weapon(target_ship)
                else:
                    print(f"Target {target_name} is out of range.")
            else:
                print(f"Not enough power to fire weapons on {attacking_ship.name}.")

    def select_target(self, target_name):
        if self.selected_target:
            self.ships[self.selected_target].selected = False
        if target_name in self.ships:
            self.ships[target_name].selected = True
            self.selected_target = target_name

    def display_health(self, ship):
        font = pygame.font.Font(None, 36)
        text = font.render(f"HP: {ship.health}", True, (255, 255, 255))
        self.screen.blit(text, (ship.position[0], ship.position[1] - 20))

        rounded_power = round(ship.power)
        text = font.render(f"Power: {rounded_power}", True, (255, 255, 255))
        self.screen.blit(text, (ship.position[0], ship.position[1] + 20))
