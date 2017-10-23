"""Uses `pickle` to save and restore populations (and other aspects of the simulation state)."""
from __future__ import print_function

import gzip
import random
import time

import gym
import neat #needed to execute replay


try:
    import cPickle as pickle # pylint: disable=import-error
except ImportError:
    import pickle # pylint: disable=import-error

from neat.population import Population
from neat.reporting import BaseReporter
from neat.six_util import iteritems, itervalues

class NNetReporter(BaseReporter):
    """
    A reporter class that performs checkpointing using `pickle`
    to save and restore populations (and other aspects of the simulation state).
    """
    def __init__(self,filename_prefix='neat-checkpoint-'):
        """
        Saves the current state (at the end of a generation) every ``generation_interval`` generations or
        ``time_interval_seconds``, whichever happens first.

        :param generation_interval: If not None, maximum number of generations between save intervals
        :type generation_interval: int or None
        :param time_interval_seconds: If not None, maximum number of seconds between checkpoint attempts
        :type time_interval_seconds: float or None
        :param str filename_prefix: Prefix for the filename (the end will be the generation number)
        """
        
        self.filename_prefix = filename_prefix
        self.bestFitness = None
        self.current_generation = None
        self.best_genome = None
        self.best_population = None
        self.best_species = None
        self.checkpoint_due = False
        self.TIMESTEPS = 1600

    def start_generation(self, generation):
        self.current_generation = generation
    
    def post_evaluate(self, config, population, species_set, bestGenome):
        nodes = list(bestGenome.nodes)
        connections = list(bestGenome.connections)
       
        #print(sorted(connections, key=lambda tup: (tup[0],tup[1])))

        #print("BEST GENOME INFORMATION\n{}\n{}".format(sorted(list(bestGenome.nodes),),list(bestGenome.connections)))
        self.depict(bestGenome,config)
        
            
    def end_generation(self, config, population, species_set):
        pass
        

    def depict(self,genome, config):
      env = gym.make('BiPedalWalker-v0')
      
      nnet = neat.nn.FeedForwardNetwork.create(genome,config)
      print("Input Nodes: {}\nOutput Nodes: {}".format(nnet.input_nodes,nnet.output_nodes))
      print("nNode Evals")
      for items in nnet.node_evals:
          print(items)
          print("\n\n")
      
      print('Action List\n')
      obs = env.reset()
      for time_step in range(self.TIMESTEPS):
            output = nnet.activate(obs)
            print("Output 1:%.4f Output 2:%.4f Output 3:%.4f Output 4:%.4f"%(round(output[0],4),round(output[1],4),round(output[2],4),round(output[3],4)))
            obs, reward, done, info = env.step(output)
            if done:
                  env.reset()
                  break
      print("")
        
