import pygame
import time
import os
import neat
import random
from bird import Bird
from base import Base
from pipe import Pipe

class Game:
    
    def __init__(self):
        pygame.font.init()
        self.WIN_WIDTH = 500
        self.WIN_HEIGHT = 800
        self.BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
        self.STAT_FONT = pygame.font.SysFont("ComicSans",50)
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()


    def run(self, genomes, config):
        
        nets = []
        ge = []
        birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(230,250))
            g.fitness = 0
            ge.append(g)

        
        base = Base(730)
        pipes = [Pipe(600)]
        score = 0
        runFlag = True
        
        while runFlag:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runFlag = False
                    pygame.quit()
                    quit()

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_ind = 1
            else:
                runFlag = False
                break

            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.1
                output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
                if output[0] > 0.5:
                    bird.jump() 

            add_pipe = False
            rem = []

            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        ge[x].fitness = ge[x].fitness - 1
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)                       

                    if pipe.isPassedByBird(bird):
                        pipe.passed = True
                        add_pipe = True

                if pipe.hasCrossedScreen():
                    rem.append(pipe)
                pipe.move()

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5

                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)

            for x, bird in enumerate(birds):
                if bird.hasFallen():
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            base.move()
            self.draw_window(birds, pipes, base, score)



    def draw_window(self, birds, pipes, base, score):
        self.win.blit(self.BG_IMG,(0,0))
        for pipe in pipes:
            pipe.draw(self.win)

        text = self.STAT_FONT.render("Score: "+str(score),1,(255,255,255))
        self.win.blit(text, (self.WIN_WIDTH-10-text.get_width(),10))
        base.draw(self.win)
        for bird in birds:
            bird.draw(self.win)
        pygame.display.update()
