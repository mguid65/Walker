# author: Wilson Zhu
# the main execution file for the simulation

# GOAL => must get 300 pts in 1600 time steps

import gym
from bipedalwalker_env import *
import neat
import os
import sys
import visualize
import getopt

env = gym.make('BiPedalWalker-v0')
render = None

TIMESTEPS = 1600
GENERATIONS = 1000

# this is the fitness function
def eval_genome(genome, config):
  nnet = neat.nn.FeedForwardNetwork.create(genome, config)
  #nnet = neat.nn.RecurrentNetwork.create(genome,config)
  obs = env.reset()
  fitnesses = []
  for trail in range(4):
    # runtime of the environment
    fitness = 0
    for time_step in range(TIMESTEPS):
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
  print("Best performance of this generation: {}\n".format(best_genome.fitness))
  if render:
    depict(best_genome,config)
    
    #print(best_genome)


def depict(genome, config):
      nnet = neat.nn.RecurrentNetwork.create(genome,config)
      obs = env.reset()
      for time_step in range(TIMESTEPS):
            env.render()
            output = nnet.activate(obs)
            obs, reward, done, info = env.step(output)
            if done:
                  env.reset()
                  break


def run(checkPoint, threads=1):
      evaluator = createEvaluator(threads)
      p = None
    
      if checkPoint:
           p = genFromCP(checkPoint,evaluator)
      else:
            local_dir = os.path.dirname(__file__)
            config_path = os.path.join(local_dir, 'config')
            p = genNewPop(config_path,evaluator)
      if p:
        winner = p.run(evaluator, GENERATIONS)


def createEvaluator(thread):
      evaluator = None
  
      if thread > 1:
            pe = neat.ParallelEvaluator(thread, eval_genome)
            evaluator = pe.evaluate
      else: 
            evaluator = eval_genomes
      
      return evaluator

def genNewPop(config_file,evaluator):
  # load the configuration
  print('\nGenerating new population.')
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
  
  # create the population & display progress
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  
  return p
  
     
def genFromCP(checkPoint,evaluator):
  
  #generate population from checkpoint
  print('\nLoading from checkpoint {}'.format(checkPoint))
  p = neat.Checkpointer.restore_checkpoint(checkPoint)
  #p.generation=1
  p.add_reporter(neat.StdOutReporter(True))
  p.add_reporter(neat.Checkpointer(100, 10000))
  return p

def main(argv):
      
      global render
      threads = 1
      checkPoint = None

      try:
        opts, args = getopt.getopt(argv,"m:f:t:")
      except getopt.GetoptError:
        print('Invalid command line arguments provided. \nFormat: python main.py -m <mode> -f <config> -t <threads>')
        sys.exit(2)
      
      for opt, arg in opts:
            if opt == '-m':
                  render = arg
            elif opt == '-f':
                  checkPoint = arg
            elif opt == '-t':
                  try:
                    threads = int(arg)
                  except TypeError as e:
                    print(e)
      
      run(checkPoint,threads)


if __name__ == '__main__':
      main(sys.argv[1:])
