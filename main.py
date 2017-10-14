# author: Wilson Zhu
# the main execution file for the simulation

# GOAL => must get 300 pts in 1600 time steps

import gym
from bipedalwalker_env import *
import neat
import os

env = gym.make('BiPedalWalker-v0')
observation = env.reset()

# this is the fitness function
def eval_genomes(genomes, config):
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
        env.reset()
        break

def run(config_file):
  # load the configuration
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
  
  # create the population
  p = neat.Population(config)
  
  winner = p.run(eval_genomes, 500)
  print(winner)
  
if __name__ == '__main__':
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config')
  run(config_path)
