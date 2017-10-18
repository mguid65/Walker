# author: Wilson Zhu
# the main execution file for the simulation

# GOAL => must get 300 pts in 1600 time steps

import gym
from bipedalwalker_env import *
import neat
import os

env = gym.make('BiPedalWalker-v0')
observation = env.reset()

generation_fitness = []
# this is the fitness function
def eval_genomes(genomes, config):
  best_genome = None
  for genome_id, genome in genomes:
    obs = env.reset()
    nnet =  neat.nn.FeedForwardNetwork.create(genome, config)

    genome.fitness = 0
    # the total runtime of the environment
    for time_step in range(1600):
      output = nnet.activate(obs)
      obs, reward, done, info = env.step(output)
      genome.fitness += reward
      if done:
        generation_fitness.append(genome.fitness)
        if best_genome is None or best_genome.fitness < genome.fitness:
          best_genome = genome
        break
  print("\nBest performance of this generation: {}".format(best_genome.fitness))

def run(config_file):
  # load the configuration
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

  # create the population & display progress
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))

  winner = p.run(eval_genomes, 500)
  print(winner)
  
if __name__ == '__main__':
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config')
  run(config_path)
