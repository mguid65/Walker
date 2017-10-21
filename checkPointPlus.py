"""Uses `pickle` to save and restore populations (and other aspects of the simulation state)."""
from __future__ import print_function

import gzip
import random
import time



try:
    import cPickle as pickle # pylint: disable=import-error
except ImportError:
    import pickle # pylint: disable=import-error

from neat.population import Population
from neat.reporting import BaseReporter
from neat.six_util import iteritems, itervalues

class CheckpointerPlus(BaseReporter):
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
        

    def start_generation(self, generation):
        self.current_generation = generation
    
    def post_evaluate(self, config, population, species_set, bestGenome):
        self.checkpoint_due = False
        
        for g in itervalues(population):   
            if self.bestFitness is None or g.fitness > self.bestFitness:
                self.bestFitness = g.fitness
                self.best_population = population
                self.best_species = species_set
                self.best_genome = g
                self.checkpoint_due = True
            
    def end_generation(self, config, population, species_set):
        if self.checkpoint_due:
            #self.save_checkpoint(config, population, species_set, self.current_generation)
            self.save_checkpoint(config,self.best_population,self.best_species,self.current_generation)
            self.last_generation_checkpoint = self.current_generation
            

    def save_checkpoint(self, config, population, species_set, generation):
        """ Save the current simulation state. """
        filename = '{0}{1}'.format(self.filename_prefix,generation)
        print("New Best Fitness: {0} Saving checkpoint to {1}".format(self.bestFitness,filename))

        with gzip.open(filename, 'w', compresslevel=5) as f:
            data = (generation, config, population, species_set, random.getstate())
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    '''
    @staticmethod
    def restore_checkpoint(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as f:
            generation, config, population, species_set, rndstate = pickle.load(f)
            random.setstate(rndstate)
            return Population(config, (population, species_set, generation))
    '''
    
