# game/entities.py
import pygame
from config import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - GROUND_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.alive = True

    def jump(self):
        if self.on_ground and self.alive:
            self.vel_y = JUMP_VEL
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def handle_collisions(self, platforms, obstacles):
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0 and self.rect.bottom <= p.rect.top + 10:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                else:
                    self.alive = False
                    return
        for o in obstacles:
            if self.rect.colliderect(o.rect):
                self.alive = False
                return
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def update(self, platforms, obstacles):
        if not self.alive: return
        self.apply_gravity()
        self.handle_collisions(platforms, obstacles)

    def draw(self, surf):
        color = PLAYER_COLOR if self.alive else (150, 50, 50)
        pygame.draw.rect(surf, color, self.rect)


class Platform:
    def __init__(self, x, y, width, speed, obj_id=None):
        self.rect = pygame.Rect(x, y, width, 20)
        self.speed = speed
        self.id = obj_id

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, PLATFORM_COLOR, self.rect)
        if self.id is not None:
            txt = FONT.render(str(self.id), True, TEXT_COLOR)
            text_rect = txt.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            surf.blit(txt, text_rect)

    def off_screen(self):
        return self.rect.right < 0


class Obstacle:
    def __init__(self, x, speed, y=None, obj_id=None):
        base_y = HEIGHT - GROUND_HEIGHT - PLAYER_SIZE if y is None else y - PLAYER_SIZE
        self.rect = pygame.Rect(x, base_y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = speed
        self.id = obj_id

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surf):
        points = [
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
            (self.rect.centerx, self.rect.top)
        ]
        pygame.draw.polygon(surf, OBSTACLE_COLOR, points)
        if self.id is not None:
            txt = FONT.render(str(self.id), True, TEXT_COLOR)
            text_rect = txt.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            surf.blit(txt, text_rect)

    def off_screen(self):
        return self.rect.right < 0