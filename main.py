# author: Christopher Schayer, Wilson Zhu
# the main execution file for the simulation

import gym
from bipedalwalker_env import *
import neat
import os
import sys
import getopt
import checkPointPlus
import replayReporter
import nnetreporter
from threading import Thread, Lock

TIMESTEPS = 1600
GENERATIONS = 1000
mode = None

env = gym.make('BiPedalWalker-v0')

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


def run(checkPoint, threads=1):
    evaluator = createEvaluator(threads)
    p = None

    if checkPoint:
        p = genFromCP(checkPoint, evaluator)
    else:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config')
        p = genNewPop(config_path, evaluator)

    if p:
        p.add_reporter(nnetreporter.NNetReporter())
        if mode != 'replay':
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(checkPointPlus.CheckpointerPlus())
        else:
            p.add_reporter(replayReporter.ReplayReporter())
        winner = p.run(evaluator, GENERATIONS)


def createEvaluator(thread):
    evaluator = None

    if thread > 1:
        pe = neat.ParallelEvaluator(thread, eval_genome)
        evaluator = pe.evaluate
    else:
        evaluator = eval_genomes

    return evaluator


def genNewPop(config_file, evaluator):
    # load the configuration
    print('\nGenerating new population.')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # create the population & display progress
    p = neat.Population(config)
    return p


def genFromCP(checkPoint, evaluator):
    # generate population from checkpoint
    print('\nLoading from checkpoint {}'.format(checkPoint))
    p = neat.Checkpointer.restore_checkpoint(checkPoint)
    return p


def main(argv):
    global mode
    threads = 1
    checkPoint = None

    try:
        opts, args = getopt.getopt(argv, "m:f:t:")
    except getopt.GetoptError:
        print('Invalid command line arguments provided. \nFormat: python main.py -m <mode> -f <config> -t <threads>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-m':
            mode = arg
        elif opt == '-f':
            checkPoint = arg
        elif opt == '-t':
            try:
                threads = int(arg)
            except TypeError as e:
                print(e)

    run(checkPoint, threads)


if __name__ == '__main__':
    main(sys.argv[1:])
