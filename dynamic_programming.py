import sys
import time
import random
import numpy as np

# Vertex: each trip is an instance of the vertex class.
class Vertex:
  def __init__(self, trip_id, passenger = True, driver = True, num_passengers = 0, vacant_seats = 0, benefit = 0):
    self.adj_list = []
    self.trip_id = trip_id
    self.num_passengers = num_passengers
    self.vacant_seats = vacant_seats - num_passengers
    self.benefit = benefit
    self.benefit = benefit
    self.driver = driver
    self.passenger = passenger
    self.final_passengers = []
    self.activated = True

  # Adds an edge representing a sharing possibility.
  def AddSharing(self, sharing):
    self.adj_list.append(sharing)

  def GetPassengerCombinations(self, i = 0):
    if (i >= len(self.adj_list)):
      return [[]];

    new_combs = []
    combs = self.GetPassengerCombinations(i + 1)
    for comb in combs:
      new_combs.append(comb)
      new_combs.append([self.adj_list[i]] + comb)

    return new_combs

  def SetFinalPassengers(self, passengers):
    for p in passengers:
      if p.trip_id != self.trip_id:
        self.final_passengers.append(p.trip_id)
    self.final_passengers.sort()

# This variable holds all trip vertices. This is our representation of
# the graph model.
graph = {}
max_benefit = -1

# Reads input from file and creates the sharing graph.
def ReadInput(filename):
  txt = open(filename)
  lines = txt.readlines()

  num_trips = int(lines[0].split()[0])
  for i in range(num_trips):
    arr = lines[1 + i].split()
    trip_id = arr[0]
    passenger = arr[1] == "1"
    driver = arr[2] == "1"
    num_passengers = int(arr[3])
    vacant_seats = int(arr[4])
    benefit = float(arr[5])
    graph[trip_id] = Vertex(trip_id, passenger, driver, num_passengers, vacant_seats, benefit)

  num_sharings = int(lines[num_trips + 1].split()[0])
  for i in range(num_sharings):
    arr = lines[num_trips + 2 + i].split()

    passenger_id = arr[0]
    driver_id = arr[1]

    # We are actually building the transposed graph here. Because
    # we need to know from the perspective of each driver, which
    # passengers she will be taking.
    if graph[passenger_id].passenger and graph[driver_id].driver:
      graph[driver_id].AddSharing(passenger_id)

def GetDrivers():
  drivers = []
  for i in graph.keys(): 
    if graph[i].driver:
      drivers.append(graph[i])
  return drivers

# Activate the right vertices in graph G according to the iterator
# code provided.
def ActivateCombination(binary_code):
  for i in graph.keys(): 
    bit = 1 << int(i) - 1
    activate = (int(binary_code) & bit) != 0
    graph[i].activated = activate

def GetGraphIndex():
  binary_code = 0
  for i in graph.keys(): 
    bit = 1 << int(i) - 1
    if graph[i].activated:
      binary_code += bit 
  return binary_code

def GetPassengersByIndexDifference(j, prev_j):
  ActivateCombination(j)

  passengers = []
  binary_code = int(prev_j)
  for i in graph.keys(): 
    bit = 1 << int(i) - 1
    activate = (binary_code & bit) != 0
    if graph[i].activated and not activate:
      passengers.append(graph[i])
  return passengers

def WriteOutput(filename):
  out = open(filename, 'w+')

  drivers = []
  for i in graph.keys(): 
    if graph[i].driver and len(graph[i].final_passengers) > 0: 
      drivers.append(graph[i])

  out.write(str(len(drivers)) + " " + str(float(max_benefit)) + "\n")
  print len(drivers), float(max_benefit)
  for driver in drivers:
    out.write(str(driver.trip_id) + " " + ' '.join(driver.final_passengers) + "\n")
    print str(driver.trip_id), ' '.join(driver.final_passengers)

def DPMaxBenefit():
  v_combinations = 2**len(graph)
  drivers = GetDrivers()
  
  b_max = np.ndarray((len(drivers), v_combinations))
  prev_j = np.ndarray((len(drivers), v_combinations))
  
  last_driver = None
  for i, val in enumerate(drivers):
    for j in range(v_combinations):
      ActivateCombination(j)
      if not drivers[i].activated:
        if i > 0:
          b_max[i][j] = b_max[i - 1][j]
          prev_j[i][j] = j
        else:
          b_max[i][j] = 0
        continue
  
      max_prev_j = -1
      max_benefit = 0
      if i > 0:
        # Not taking any passengers.
        max_prev_j = j
        max_benefit = b_max[i - 1][j]
  
      drivers[i].activated = False
      p_combs = drivers[i].GetPassengerCombinations()
      for p_comb in p_combs:
        if len(p_comb) == 0:
          continue
  
        invalid = False
        total_passengers = 0
        for p in p_comb:
          if not graph[p].activated:
            invalid = True
            break
          total_passengers += graph[p].num_passengers
        
        if total_passengers > drivers[i].vacant_seats or invalid: 
          continue;
  
        benefit = 0
        for p in p_comb:
          graph[p].activated = False
          benefit += graph[p].benefit
  
        j_index = GetGraphIndex()
        if i > 0:
          benefit += b_max[i - 1][j_index]

        if (benefit > max_benefit):
          max_benefit = benefit
          max_prev_j = j_index
  
        for p in p_comb:
          graph[p].activated = True
        
      b_max[i][j] = max_benefit
      if i > 0:
        prev_j[i][j] = max_prev_j
      else: 
        prev_j[i][j] = -1
  
  max_benefit = 0
  i = len(drivers) - 1
  best_j = 0
  for j in range(v_combinations):
    if b_max[i][j] > max_benefit:
      max_benefit = b_max[i][j]
      best_j = j

  while (i >= 0):
    best_prev_j = 0
    if i > 0:
      best_prev_j = prev_j[int(i)][int(best_j)]

    passengers = GetPassengersByIndexDifference(best_j, best_prev_j)
    drivers[i].SetFinalPassengers(passengers)
    best_j = best_prev_j
    i -= 1

  return max_benefit

# =================================
# Main
# =================================

# The program takes 2 arguments. One input file and one output file.
if len(sys.argv) != 3:
  print "Wrong number of arguments"
  sys.exit()

ReadInput(sys.argv[1])

max_benefit = DPMaxBenefit() 
WriteOutput(sys.argv[2])
