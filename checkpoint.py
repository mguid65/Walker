# author: Christopher Schayer
# a custom checkpointer that is based on the best genome encountered

from __future__ import print_function

import gzip
import random
try:
  import cPickle as pickle
except ImportError:
  import pickle

from neat.population import Population
from neat.reporting import BaseReporter

class checkpointer(BaseReporter):
  def __init__(self, filename_prefix='neat-checkpoint-', interval=50):
    self.filename_prefix = filename_prefix
    self.current_generation = None
    self.best_genome = None
    self.best_fitness = None
    self.population = None
    self.species = None
    self.interval = interval
    
  def start_generation(self, generation):
    self.current_generation = generation
    
  def post_evaluate(self, config, population, species_set, best_genome):
    if self.best_genome is None or best_genome.fitness > self.best_fitness:
      self.best_genome = best_genome
      self.population = population
      self.species = species_set
      self.best_fitness = best_genome.fitness
      self.save_checkpoint(config, self.population, self.species, self.current_generation)
    elif self.current_generation % self.interval == 0:
      self.save_checkpoint(config, population, species_set, self.current_generation)
      
  def end_generation(self, config, population, species_set):
    pass
  
  def save_checkpoint(self, config, population, species_set, generation):
    filename = '{0}{1}'.format(self.filename_prefix, generation)
    print("Top fitness found with a value of {0}. Saving checkpoint to {1}".format(self.best_genome.fitness, filename))
    with gzip.open(filename, 'w', compresslevel=5) as f:
      data = (generation, config, population, species_set, random.getstate())
      pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)