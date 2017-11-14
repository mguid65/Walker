# author: Christopher Schayer, Wilson Zhu
# the logger functionality

from neat.population import Population
from neat.reporting import BaseReporter
from neat.math_util import mean
from neat.six_util import itervalues, iterkeys

class logger(BaseReporter):
  def __init__(self):
    self.generation = None
    self.file = open("data.csv", "w")
    
  def start_generation(self, generation):
    self.generation = generation
  
  def end_generation(self, config, population, species_set):
    pass
    
  def post_evaluate(self, config, population, species, best_genome):
    fitnesses = [c.fitness for c in itervalues(population)]
    fit_mean = mean(fitnesses)  
    species_ids = list(iterkeys(species.species))
    for i in species_ids:
      species = species.species[i]
      self.file.write("{}, {}, {}, {}\n".format(self.generation, i, species.fitness, fit_mean))
      
  def complete_extinction(self):
    print('All species extinct.')
    
  def found_solution(self, config, generation, best):
    print('\nBest individual in generation {0} meets fitness threshold - complexity: {1!r}'.format(self.generation, best.size()))
    
  def species_stagnant(self, sid, species):
    print("\nSpecies {0} with {1} members is stagnated: removing it".format(sid, len(species.members)))

  def info(self, msg):
    pass
