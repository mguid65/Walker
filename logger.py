# author: Christopher Schayer, Wilson Zhu
# the logger functionality

from neat.population import Population
from neat.reporting import BaseReporter
from neat.math_util import mean
from neat.six_util import itervalues, iterkeys
import csv, visualize

class logger(BaseReporter):
  def __init__(self):
    self.generation = None
    
  def start_generation(self, generation):
    self.generation = generation
  
  def end_generation(self, config, population, species_set):
    pass
  
  def post_evaluate(self, config, population, species, best_genome):  
    fitnesses = [c.fitness for c in itervalues(population)]
    fit_mean = mean(fitnesses)  
    species_ids = list(iterkeys(species.species))
    best_species = None
    for i in species_ids:
      s = species.species[i]
      if best_species is None or s.fitness > best_species.fitness:
        best_species = s
      self.log(self.generation, i, s.fitness, fit_mean)
    visualize.draw_net(config, best_genome, view=False, filename='nnet_{}.gv'.format(self.generation))

  def complete_extinction(self):
    print('All species extinct.')
    
  def found_solution(self, config, generation, best):
    print('\nBest individual in generation {0} meets fitness threshold - complexity: {1!r}'.format(self.generation, best.size()))
    
  def species_stagnant(self, sid, species):
    print("\nSpecies {0} with {1} members is stagnated: removing it".format(sid, len(species.members)))

  def info(self, msg):
    pass
  
  def log(self, generation, id, fitness, fit_mean):
    with open("data.csv", "a") as file:
      log = csv.writer(file, delimiter=",")
      data = (str(generation), str(id), str(fitness), str(fit_mean))
      log.writerow(data)
