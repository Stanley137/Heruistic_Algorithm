import os
import random
import neat
import pygame

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROL_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 # angle of the bird
        self.tick_count = 0 # time since the bird was created
        self.vel = 0 # velocity of the bird
        self.height = self.y # height of the bird // last y position
        self.img_count = 0 # index of the bird image
        self.img = self.IMGS[0] # current bird image
    def jump(self):
        self.vel = -10.5 # jump velocity
        self.tick_count = 0 # reset the tick count
        self.height = self.y # reset the height
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d
        
        if d < 0 or self.y < (self.height + 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90:
                    self.tilt -= self.ROL_VEL
                    
    def draw(self, win):
        self.img_count = (self.img_count + 1) % self.ANIMATION_TIME
        self.img = self.IMGS[int(self.img_count//2)]
        if self.tilt <= -80:
            self.img = self.IMGS[1]
        elif self.tilt <= 25:
            self.img = self.IMGS[0]
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
                



