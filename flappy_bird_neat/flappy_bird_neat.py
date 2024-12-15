import os
import random
import neat
import pygame
pygame.font.init()


BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WIN_WIDTH = 500
WIN_HEIGHT = 800

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
        self.img_count += 1

        # Loop through the bird images for animation
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If the bird is diving, keep the wings in the middle position
        if self.tilt <= -80:
            self.img = self.IMGS[1]

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    def move(self):
        self.x -= self.VEL
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset) # check if the bird collides with the bottom of the pipe
        top_point = bird_mask.overlap(top_mask, top_offset) # check if the bird collides with the top of the pipe
        return top_point or bottom_point
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # if the base is out of the screen, reset the position
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
      
  
def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    base.draw(win)
    score_label = SCORE_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 20))
    for pipe in pipes:
        pipe.draw(win)
    pygame.display.update()
    
def main():
    bird = Bird(200, 200)
    base = Base(680)
    pipes = [Pipe(550)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # create the window
    clock = pygame.time.Clock()
    run = True
    score = 0
    add_pipe = False
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Clear the rem list at the start of each iteration
        rem = []
        
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe) # remove the pipe over the screen
            if not pipe.passed and pipe.x < bird.x: 
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            pipes.append(Pipe(550))
            score += 1
            add_pipe = False
            
        # Remove pipes using a list comprehension to avoid the ValueError
        pipes = [pipe for pipe in pipes if pipe not in rem]
        
        if bird.y + bird.img.get_height() >= 680:    
            pass
        bird.move() 
        base.move()
        draw_window(win, bird, pipes, base, score)
    # kill the game
    score_label = SCORE_FONT.render("LOSE!" , 1,(255, 255, 255))
    win.blit(score_label, ((WIN_WIDTH - score_label.get_width()) // 2, (WIN_HEIGHT - score_label.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

main()

