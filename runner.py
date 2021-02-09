import os
import neat
from game import Game
from visualizer import *

def load_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"configs\config-feedforward.txt")
    
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path)

    population = neat.Population(config)
    return config, population

def add_stats(population):
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

def main(config,population):
    num_gen = 100
    game = Game()
    winner = population.run(game.run,num_gen)
    plot_stats(population.reporters.reporters[1])
    plot_species(population.reporters.reporters[1])
    # draw_net(config, winner, view = True, filename='network')



if __name__ == '__main__':
    config, population = load_config()
    add_stats(population)
    main(config,population)
    