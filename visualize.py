from __future__ import print_function

import copy
import warnings

import graphviz
import matplotlib.pyplot as plt
import numpy as np

def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False, node_colors=None, fmt='svg'):
  # Attributes for network nodes.
  if graphviz is None:
    warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
    return
    
  if node_names is None:
    node_names = {}
    
  assert type(node_names) is dict
  
  if node_colors is None:
    node_colors = {}
    
  assert type(node_colors) is dict
  
  node_attrs = {
    'shape': 'circle',
    'fontsize': '9',
    'height': '0.2',
    'width': '0.2'
  }

  dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)
  
  inputs = set()
  outputs = set()
  
  if prune_unused:
    nodes = []
    for cg in genome.connections.values():
      if cg.enabled or show_disabled:
        ikey, okey = cg.key
        nodes.append(ikey)
        nodes.append(okey)

    used_nodes = set(nodes)
    for i in used_nodes:
      if i < 0:
        inputs.add(i)
        name = node_names.get(i, str(i))
        input_attrs = {'style': 'filled', 'shape': 'box'}
        input_attrs['fillcolor'] = node_colors.get(i, 'lightgray')
        dot.node(name, _attributes=input_attrs)
      elif i >= 0 and i <= 3:
        outputs.add(i)
        name = node_names.get(i, str(i))
        node_attrs = {'style': 'filled'}
        node_attrs['fillcolor'] = node_colors.get(i, 'lightblue')
        dot.node(name, _attributes=node_attrs)
  else:
    for k in config.genome_config.input_keys:
      inputs.add(k)
      name = node_names.get(k, str(k))
      input_attrs = {'style': 'filled', 'shape': 'box'}
      input_attrs['fillcolor'] = node_colors.get(k, 'lightgray')
      dot.node(name, _attributes=input_attrs)
      
    outputs = set()
    for k in config.genome_config.output_keys:
      outputs.add(k)
      name = node_names.get(k, str(k))
      node_attrs = {'style': 'filled'}
      node_attrs['fillcolor'] = node_colors.get(k, 'lightblue')
      dot.node(name, _attributes=node_attrs)
      
  used_nodes = set(genome.nodes.keys())
  for n in used_nodes:
    if n in inputs or n in outputs:
      continue  
    attrs = {'style': 'filled', 'fillcolor': node_colors.get(n, 'white')}
    dot.node(str(n), _attributes=attrs)
    
  for cg in genome.connections.values():
    if cg.enabled or show_disabled:
      input, output = cg.key
      a = node_names.get(input, str(input))
      b = node_names.get(output, str(output))
      style = 'solid' if cg.enabled else 'dotted'
      color = 'green' if cg.weight > 0 else 'red'
      width = str(0.2 + abs(cg.weight / 5.0))
      dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})
      
  dot.render(filename, view=view)
  return dot

def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
  if plt is None:
    warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
    return
  generation = range(len(statistics.most_fit_genomes))
  best_fitness = [c.fitness for c in statistics.most_fit_genomes]
  avg_fitness = np.array(statistics.get_fitness_mean())
  stdev_fitness = np.array(statistics.get_fitness_stdev())
  
  plt.plot(generation, avg_fitness, 'b-', label="average")
  plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
  plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
  plt.plot(generation, best_fitness, 'r-', label="best")
  
  plt.title("Population's average and best fitness")
  plt.xlabel("Generations")
  plt.ylabel("Fitness")
  plt.grid()
  plt.legend(loc="best")
  
  if ylog:
    plt.gca().set_yscale('symlog')
    
  plt.savefig(filename)
  
  if view:
    plt.show()
    
  plt.close()
  
def plot_species(statistics, view=False, filename='speciation.svg'):
  if plt is None:
    warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
    return
  species_sizes = statistics.get_species_sizes()
  num_generations = len(species_sizes)
  curves = np.array(species_sizes).T
  
  fig, ax = plt.subplots()
  ax.stackplot(range(num_generations), *curves)
  
  plt.title("Speciation")
  plt.ylabel("Size per Species")
  plt.xlabel("Generations")
  
  plt.savefig(filename)
  
  if view:
    plt.show()
    
  plt.close()
