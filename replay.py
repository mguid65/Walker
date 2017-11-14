# author: Christopher Schayer
# the replay component of the program, this will allow us to see the AI in action

from __future__ import print_function

import gym
import neat
try:
  import cPickle as pickle
except ImportError:
  import pickle

from neat.population import Population
from neat.reporting import BaseReporter

class replay(BaseReporter):
  def __init__(self, filename_prefix='neat-checkpoint-'):
    self.filename_prefix = filename_prefix
    self.current_generation = None
    self.TIMESTEPS = 1600
    
  def start_generation(self, generation):
    print('Generating replay data from checkpoint')
    self.current_generation = generation
    pass
    
  def post_evaluate(self, config, population, species_set, best_genome):
    self.render(best_genome, config)
    
  def end_generation(self, config, population, species_set):
    pass
    
  def render(self,genome, config):
    env = gym.make('BiPedalWalker-v0')
    print('Running replay')
    nnet = neat.nn.FeedForwardNetwork.create(genome,config)
    obs = env.reset()
    for time_step in range(self.TIMESTEPS):
      env.render()
      output = nnet.activate(obs)
      obs, reward, done, info = env.step(output)
      if done: break
      
    quit()
