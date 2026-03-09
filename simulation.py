import pygame
import numpy as np
import math

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Mobile Manipulator Simulation")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Arm lengths
L1 = 150
L2 = 120

# Car position
car_x = 250
car_y = 650

# Objects
objects = [
    {"x": 950, "y": 450, "picked": False, "placed": False, "dest_x": 300, "dest_y": 250},
    {"x": 1050, "y": 350, "picked": False, "placed": False, "dest_x": 550, "dest_y": 250}
]

current_object = None

# Gripper animation
gripper_target = 20
gripper_current = 20
pick_delay = 0

# Smooth servo angles
current_theta1 = 0
current_theta2 = 0

def inverse_kinematics(x, y):
    D = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    D = np.clip(D, -1, 1)
    theta2 = math.acos(D)
    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2),
                                          L1 + L2 * math.cos(theta2))
    return theta1, theta2

running = True

while running:
    screen.fill((240,240,240))

    # Workspace circle (Improvement 1)
    pygame.draw.circle(screen, (200,200,255),
                       (int(car_x), int(car_y)),
                       L1 + L2, 2)

    # Grid
    for i in range(0, WIDTH, 50):
        pygame.draw.line(screen, (220,220,220), (i,0), (i,HEIGHT))
    for j in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (220,220,220), (0,j), (WIDTH,j))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and current_object is not None:
                current_object["picked"] = False
                current_object["placed"] = True
                current_object = None
                gripper_target = 20

    # Car movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= 5
    if keys[pygame.K_RIGHT]:
        car_x += 5
    if keys[pygame.K_UP]:
        car_y -= 5
    if keys[pygame.K_DOWN]:
        car_y += 5

    # Target selection
    target_x, target_y = car_x, car_y

    if current_object is not None:
        target_x = current_object["x"]
        target_y = current_object["y"]
    else:
        for obj in objects:
            if not obj["picked"] and not obj["placed"]:
                target_x = obj["x"]
                target_y = obj["y"]
                break

    dx = target_x - car_x
    dy = target_y - car_y

    target_theta1, target_theta2 = inverse_kinematics(dx, dy)

    # Smooth Servo Motion (Improvement 4)
    current_theta1 += (target_theta1 - current_theta1) * 0.1
    current_theta2 += (target_theta2 - current_theta2) * 0.1

    x1 = car_x + L1 * math.cos(current_theta1)
    y1 = car_y + L1 * math.sin(current_theta1)

    x2 = x1 + L2 * math.cos(current_theta1 + current_theta2)
    y2 = y1 + L2 * math.sin(current_theta1 + current_theta2)

    # Smooth Pick Animation (Improvement 7)
    if current_object is None:
        for obj in objects:
            if not obj["picked"] and not obj["placed"]:
                distance = math.sqrt((x2 - obj["x"])**2 + (y2 - obj["y"])**2)
                if distance < 30:
                    gripper_target = 5
                    pick_delay += 1
                    if pick_delay > 20:
                        obj["picked"] = True
                        current_object = obj
                        pick_delay = 0
                    break
    else:
        current_object["x"] = x2
        current_object["y"] = y2

    # Smooth gripper movement
    gripper_current += (gripper_target - gripper_current) * 0.2

    # Draw car
    pygame.draw.rect(screen, (0,100,255), (car_x-70, car_y, 140, 40))
    pygame.draw.circle(screen, (0,0,0), (car_x-50, car_y+40), 20)
    pygame.draw.circle(screen, (0,0,0), (car_x+50, car_y+40), 20)

    # Draw arm
    pygame.draw.line(screen, (255,0,0), (car_x,car_y), (x1,y1), 12)
    pygame.draw.line(screen, (0,200,0), (x1,y1), (x2,y2), 12)

    pygame.draw.circle(screen, (0,0,0), (int(car_x),int(car_y)), 10)
    pygame.draw.circle(screen, (0,0,0), (int(x1),int(y1)), 10)

    # Draw gripper
    grip_len = 40
    angle = current_theta1 + current_theta2

    gx1 = x2 + grip_len * math.cos(angle + math.pi/2)
    gy1 = y2 + grip_len * math.sin(angle + math.pi/2)

    gx2 = x2 + grip_len * math.cos(angle - math.pi/2)
    gy2 = y2 + grip_len * math.sin(angle - math.pi/2)

    pygame.draw.line(screen, (0,0,0), (x2,y2),
                     (gx1 + gripper_current * math.cos(angle),
                      gy1 + gripper_current * math.sin(angle)), 6)

    pygame.draw.line(screen, (0,0,0), (x2,y2),
                     (gx2 + gripper_current * math.cos(angle),
                      gy2 + gripper_current * math.sin(angle)), 6)

    # Draw objects and destination boxes
    for obj in objects:
        pygame.draw.rect(screen, (200,50,50),
                         (obj["x"]-20, obj["y"]-20, 40, 40))

        pygame.draw.rect(screen, (0,180,0),
                         (obj["dest_x"]-35, obj["dest_y"]-35, 70, 70), 4)

    # Display angles
    screen.blit(font.render(f"Theta1: {round(math.degrees(current_theta1),1)} deg", True, (0,0,0)), (20,20))
    screen.blit(font.render(f"Theta2: {round(math.degrees(current_theta2),1)} deg", True, (0,0,0)), (20,50))
    screen.blit(font.render(f"End Effector: ({int(x2)}, {int(y2)})", True, (0,0,0)), (20,80))

    status = "IDLE"
    if current_object is not None:
        status = "HOLDING OBJECT - Press P to Place"

    screen.blit(font.render(status, True, (0,0,0)), (20,120))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()