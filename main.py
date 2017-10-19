# author: Wilson Zhu
# the main execution file for the simulation

# GOAL => must get 300 pts in 1600 time steps

import gym
from bipedalwalker_env import *
import neat
import os
import sys

env = gym.make('BiPedalWalker-v0')

# this is the fitness function
def eval_genome(genome, config):
  nnet = neat.nn.FeedForwardNetwork.create(genome, config)
  obs = env.reset()
  fitnesses = []
  for trail in range(4):
    # runtime of the environment
    fitness = 0
    for time_step in range(1600):
      output = nnet.activate(obs)
      obs, reward, done, info = env.step(output)
      fitness += reward
      if done: break
    fitnesses.append(fitness)
  return sum(fitnesses) / len(fitnesses)

def eval_genomes(genomes, config):
  best_genome = None
  for genome_id, genome in genomes:
    genome.fitness = eval_genome(genome, config)
    if best_genome is None or best_genome.fitness < genome.fitness:
      best_genome = genome
  if render:
    simulate(best_genome, config)

# this will render the simulation if the user desires it
def simulate(genome, config):
  nnet = neat.nn.FeedForwardNetwork.create(genome, config)
  obs = env.reset()
  for time_step in range(1600):
    output = nnet.activate(obs)
    obs, reward, done, info = env.step(output)
    env.render()

def run(config_file):
  # load the configuration
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

  # create the population & display progress
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  p.add_reporter(neat.Checkpointer(100, 10000))
  winner = p.run(eval_genomes, 1000)

if __name__ == '__main__':
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config')
  render = False
  if len(sys.argv) == 2:
    render = True
  run(config_path)
