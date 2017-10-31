# author: Christopher Schayer
# outputs the structure of the best neural network

from __future__ import print_function

import gym
import neat
try:
  import cPickle as pickle
except ImportError:
  import pickle

from neat.population import Population
from neat.reporting import BaseReporter

class nnetreporter(BaseReporter):
  def __init__(self, filename_prefix='neat-checkpoint-'):
    self.filename_prefix = filename_prefix # rm this for later testing
    self.current_generation = None
    self.TIMESTEPS = 1600
    
  def start_generation(self, generation):
    self.current_generation = generation
    
  def post_evaluate(self, config, population, species_set, best_genome):
    nodes = list(best_genome.nodes)
    connections = list(best_genome.connections)
    # self.neural_activity(best_genome, config)
    
  def end_generation(self, config, population, species_set):
    pass
    
  def neural_activity(self, genome, config):
    env = gym.make('BiPedalWalker-v0')

    # construct the network using the genome and print out the structure of the network
    nnet = neat.nn.FeedForwardNetwork.create(genome, config)
    print("Input Nodes: {}\nOutput Nodes: {}".format(nnet.input_nodes, nnet.output_nodes))
    print("nNode Evals")
    for items in nnet.node_evals:
      print(items)
      print("\n")

    # the outputs of the network when running
    print('Action List\n')
    obs = env.reset()
    for time_step in range(self.TIMESTEPS):
      output = nnet.activate(obs)
      print("Output 1:%.4f Output 2:%.4f Output 3:%.4f Output 4:%.4f"%(round(output[0], 4), round(output[1], 4), round(output[2], 4), round(output[3], 4)))
      obs, reward, done, info = env.step(output)
      if done: break

    print("") # Chris?
        
