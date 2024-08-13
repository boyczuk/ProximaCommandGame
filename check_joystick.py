import pygame

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("No joysticks connected.")
else:
    print(f"{joystick_count} joystick(s) connected:")
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"Joystick {i}: {joystick.get_name()}")

pygame.quit()
