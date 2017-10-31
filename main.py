# author: Christopher Schayer, Wilson Zhu
# the main execution file for the simulation

# todo: organize import statements
import gym
from bipedalwalker_env import *
from checkpoint import *
from nnetreporter import *
from replay import *
import neat
import os, sys, getopt
from threading import Thread, Lock

TIMESTEPS = 1600
GENERATIONS = 1000
mode = None

env = gym.make('BiPedalWalker-v0')

# this is the fitness function
def eval_genome(genome, config):
  nnet = neat.nn.FeedForwardNetwork.create(genome, config)
  # nnet = neat.nn.RecurrentNetwork.create(genome,config)
  obs = env.reset()
  fitness = 0
  for time_step in range(TIMESTEPS):
    output = nnet.activate(obs)
    obs, reward, done, info = env.step(output)
    fitness += reward
    if done: break
  return fitness

def eval_genomes(genomes, config):
  best_genome = None
  for genome_id, genome in genomes:
    genome.fitness = eval_genome(genome, config)

def run(cp, threads=1):
  evaluator = create_evaluator(threads)
  
  # initialize the population
  p = None
  if cp: 
    p = load_from_checkpoint(cp, evaluator)
  else:
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    p = new_population(config_path, evaluator)
  
  if p:
    p.add_reporter(nnetreporter())
    if mode != 'replay':
      p.add_reporter(neat.StdOutReporter(True))
      p.add_reporter(checkpointer())
    else:
      p.add_reporter(replay())
    winner = p.run(evaluator, GENERATIONS)


def create_evaluator(thread):
  evaluator = None
  if thread > 1:
    pe = neat.ParallelEvaluator(thread, eval_genome)
    evaluator = pe.evaluate
  else:
    evaluator = eval_genomes
  return evaluator


def new_population(config_file, evaluator):
  # load the configuration
  print('\nGenerating new population.')
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
  
  # create the population & display progress
  p = neat.Population(config)
  return p


# load population from checkpoint
def load_from_checkpoint(cp, evaluator):
  print('\nLoading from checkpoint {}'.format(cp))
  p = neat.Checkpointer.restore_checkpoint(cp)
  return p

def main(argv):
  global mode
  threads = 1
  cp_flag = None
  
  try:
    opts, args = getopt.getopt(argv, "m:f:t:")
  except getopt.GetoptError:
    print('Invalid command line arguments provided. \nFormat: python main.py -m <mode> -f <config> -t <threads>')
    sys.exit(2)
    
  for opt, arg in opts:
    if opt == '-m':
      mode = arg
    elif opt == '-f':
      cp_flag = arg
    elif opt == '-t':
      try:
        threads = int(arg)
      except TypeError as e:
        print(e)
  run(cp_flag, threads)

if __name__ == '__main__':
  main(sys.argv[1:])
