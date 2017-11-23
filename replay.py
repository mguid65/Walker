# author: Christopher Schayer
# the replay component of the program, this will allow us to see the AI in action 
# and display the structure of the neural network

from __future__ import print_function

import gym
import neat
from neat.six_util import itervalues, iterkeys
import visualize

try:
  import cPickle as pickle
except ImportError:
  import pickle

from neat.population import Population
from neat.reporting import BaseReporter

class replay(BaseReporter):
  def __init__(self, filename_prefix='neat-checkpoint-'):
    self.filename_prefix = filename_prefix
    self.generation = None
    self.TIMESTEPS = 1600
    self.node_names = {
      -1: 'ha', -2: 'hav', -3: 'Vx', -4: 'Vy', -5:'ULA',-6:'ULS',-7:'LLA',
      -8: 'LLS', -9: 'LGC', -10:'URA', -11:'URS', -12:'LRA', -13:'LRS', -14:'RGC',
      -15: 'L1', -16: 'L2', -17:'L3', -18:'L4', -19:'L5', -20:'L6', -21:'L7',
      -22: 'L8', -23: 'L9', -24:'L10', 0: 'ULL', 1: 'LLL', 2:'URL', 3:'LRL'}
    
  def start_generation(self, generation):
    print('Generating replay data from checkpoint')
    self.generation = generation
    pass
    
  def post_evaluate(self, config, population, species_set, best_genome):
    self.render(best_genome, config)
    self.generateNNet(config, species_set)
    quit()
    
  def end_generation(self, config, population, species_set):
    pass
    
  def render(self,genome, config):
    env = gym.make('BiPedalWalker-v0')
    print('Running replay')
    nnet = neat.nn.FeedForwardNetwork.create(genome, config)
    obs = env.reset()
    for time_step in range(self.TIMESTEPS):
      env.render()
      output = nnet.activate(obs)
      obs, reward, done, info = env.step(output)
      if done: break

  def generateNNet(self, config, species):
    species_ids = list(iterkeys(species.species))
    for i in species_ids:
      s = species.species[i]
      best_genome = None
      for g in itervalues(s.members):
        if best_genome is None or (g.fitness > best_genome.fitness):
          best_genome = g
      visualize.draw_net(config, best_genome, view=False, prune_unused=False, node_names=self.node_names, filename='nnet_{}_{}.gv'.format(self.generation, i))
