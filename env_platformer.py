import pygame
import numpy as np
from game_config import *

class PlatformerEnv:
    def __init__(self, render_mode=False, screen=None, offset_x=0, offset_y=0):
        pygame.init()
        self.render_mode = render_mode
        self.screen = screen
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.ground = Ground()
        self.player = Player()
        self.blocks, self.spikes, self.goals = generate_level()
        self.done = False
        return self.get_state()

    def step(self, action):
        if action == 1:
            self.player.jump()

        self.blocks.update()
        self.spikes.update()
        self.goals.update()
        status = self.player.update(self.blocks, self.spikes, self.ground, self.goals)

        reward = -0.01
        if status == "dead":
            reward = -100
            self.done = True
        elif status == "win":
            reward = 100
            self.done = True
        else:
            goal = self.goals.sprites()[0] if self.goals else None
            if goal:
                distance = goal.rect.centerx - self.player.rect.centerx
                reward += 0.1 * (WIDTH - distance) / WIDTH

        return self.get_state(), reward, self.done, {}

    def get_state(self):
        grid = np.zeros((3, 3))
        px, py = self.player.rect.centerx, self.player.rect.centery

        for i in range(3):
            for j in range(3):
                cell_x = px + (i - 1) * BLOCK_SIZE
                cell_y = py + (j - 1) * BLOCK_SIZE
                for block in self.blocks:
                    if block.rect.collidepoint(cell_x, cell_y):
                        grid[j, i] = 1
                for spike in self.spikes:
                    if spike.rect.collidepoint(cell_x, cell_y):
                        grid[j, i] = 2
                for goal in self.goals:
                    if goal.rect.collidepoint(cell_x, cell_y):
                        grid[j, i] = 3

        goal = self.goals.sprites()[0] if self.goals else None
        goal_distance = (goal.rect.centerx - px) / WIDTH if goal else 1.0
        state = tuple(grid.flatten()) + (self.player.velocity_y / 10.0, goal_distance)
        return state

    def render(self):
        if self.render_mode and self.screen:
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill(BACKGROUND)
            surface.blit(self.ground.image, self.ground.rect)
            self.blocks.draw(surface)
            self.spikes.draw(surface)
            self.goals.draw(surface)
            surface.blit(self.player.rotated_image, self.player.rotated_image.get_rect(center=self.player.rect.center))
            self.screen.blit(surface, (self.offset_x, self.offset_y))
            pygame.display.flip()
            self.clock.tick(60)

    def close(self):
        if self.render_mode and self.screen:
            pygame.quit()