# -*- coding: utf-8 -*-
"""fuel_consumption.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e_cNSgR9WLAMnf8M9-UHBBGWcxtfZtqg
"""

import pandas as pd
import pandas_datareader as data
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import csv
import math
from statistics import *
import xml.etree.ElementTree as ET

def xml_to_csv(path, output):
  tree = ET.parse(path)
  root = tree.getroot()
  root.tag
  root.attrib

  d = {}
  i = 0
  for child in root:
      #print(child.attrib["time"])
      for childs in child:
        dt = {"time" : child.attrib["time"]}
        d[i] = {**dt, **dict(childs.attrib.items())}
        i += 1

  df = pd.DataFrame.from_dict(d,orient="index")
  df.to_csv(output)

def fuel_per_vehicle(file_path, output):
    df = pd.read_csv(file_path)
    fuel_values = df['fuel']
    fuel_values = list(fuel_values)
    v_id = df['id']
    v_id = list(v_id)
    d = {}
    for value in fuel_values:
      for id in v_id:
      
        if id not in d:
          d[id] = int(value)
        else:
          d[id] = d[id] + int(value)
    df = pd.DataFrame.from_dict(d,orient="index")
    df.to_csv(output)

def fuel_per_step(file_path, output):
    df = pd.read_csv(file_path)
    fuel_values = df['fuel']
    fuel_values = list(fuel_values)
    step = df['time']
    step = list(step)
    v_id = df['id']
    v_id = list(v_id)
    d = {}
    j = 1
    fuel_cons = 0
    print(len(step))
    i = 1
    fuel_cons = float(fuel_values[0])
    for stp in step[1:]:
      if stp == step[i-1]:
        j += 1
        fuel_cons = fuel_cons + float(fuel_values[i])
        d[stp] = {'vehicles': j, 'fuel':  fuel_cons}
      else:
        j = 1
        fuel_cons = float(fuel_values[i])
        d[stp] = {'vehicles': j, 'fuel':  fuel_cons}
        j = 0
      i += 1
    df = pd.DataFrame.from_dict(d,orient="index")
    df.to_csv(output)

#def average_fuel_consumption(input1, input2, output):

def fuel_plots(conv_path, adapt_path):
  df = pd.read_csv(conv_path)
  timestep = list(df.iloc[:, 0])
  vehicles = list(df['vehicles'])
  fuel = list(df['fuel'])


  z = [m/n for m, n in zip(fuel, vehicles)]
  fig, ax = plt.subplots(num=0, dpi=80, figsize=(10, 5))
  ax.grid(True)
  ax.plot(timestep[:900], z[:900], label='modèle conventionnel')

  df = pd.read_csv(adapt_path)
  timestep = list(df.iloc[:, 0])
  vehicles = list(df['vehicles'])
  fuel = list(df['fuel'])


  z = [m/n for m, n in zip(fuel, vehicles)]
  ax.grid(True)
  ax.plot(timestep[:900], z[:900], label='modèle adaptive')

  ax.set_xlabel('seconds')
  ax.set_ylabel('ml/s')
  ax.legend()
  plt.title('consommation de carburant')
  plt.savefig("fuel_consumption")

xml_to_csv('emission500with.xml', 'emission500with.csv')
#fuel_per_vehicle('/content/emission500with.csv', '/content/fuel500with.csv')
fuel_per_step('emission500with.csv', 'fuelstep500with.csv')

xml_to_csv('emission500without.xml', 'emission500without.csv')
#fuel_per_vehicle('/content/emission500without.csv', '/content/fuel500without.csv')
fuel_per_step('emission500without.csv', 'fuelstep500without.csv')

fuel_plots('fuelstep500without.csv', 'fuelstep500with.csv')
