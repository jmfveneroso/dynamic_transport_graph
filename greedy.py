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
      if p != self.trip_id:
        self.final_passengers.append(p)
    self.final_passengers.sort()

# This variable holds all trip vertices. This is our representation of
# the graph model.
graph = {}
the_drivers = []
max_benefit = 0

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

def WriteOutput(filename):
  out = open(filename, 'w+')

  drivers = []
  for i in graph.keys(): 
    if graph[i].driver and len(graph[i].final_passengers) > 0: 
      drivers.append(graph[i])

  out.write(str(len(drivers)) + " " + str(float(max_benefit)) + "\n")
  the_drivers.sort(key = lambda x: x.trip_id)

  for driver in the_drivers:
    if len(driver.final_passengers) == 0:
      the_drivers.remove(driver)
      continue

  print len(the_drivers), float(max_benefit)
  for driver in the_drivers:
    out.write(str(driver.trip_id) + " " + ' '.join(driver.final_passengers) + "\n")
    print str(driver.trip_id), ' '.join(driver.final_passengers)

def GetDrivers():
  drivers = []
  for i in graph.keys(): 
    if graph[i].driver:
      drivers.append(graph[i])
  return drivers

def RemoveVertice(trip_id):
  del graph[trip_id]
  for i in graph.keys(): 
    if trip_id in graph[i].adj_list: 
      graph[i].adj_list.remove(trip_id)

def GetDrivers():
  drivers = []
  for i in graph.keys(): 
    if graph[i].driver and len(graph[i].adj_list) > 0:
      drivers.append(graph[i])
  return drivers

def KnapsackGreedy(driver):
  p_by_efficiency = []
  for p in driver.adj_list: 
    efficiency = graph[p].benefit / graph[p].num_passengers
    p_by_efficiency.append((graph[p], efficiency))

  p_by_efficiency.sort(key = lambda x: x[1])
  
  passengers = []
  total_passengers = 0
  benefit = 0
  p = p_by_efficiency.pop()[0]
  while (True):
    if (total_passengers + p.num_passengers <= driver.vacant_seats):
      total_passengers += p.num_passengers
      benefit += p.benefit
      passengers.append(p.trip_id)
    if len(p_by_efficiency) == 0:
      break
    p = p_by_efficiency.pop()[0]

  return (passengers, benefit)

def GreedyMaxBenefit():
  max_benefit = 0
  while True:
    drivers = GetDrivers()
    if len(drivers) == 0: 
      break

    max_local_benefit = -1
    best_driver = None
    best_tuple = None
    for driver in drivers:
      t = KnapsackGreedy(driver)
      if (t[1] > max_local_benefit):
        max_local_benefit = t[1]
        best_driver = driver
        best_tuple = t

    max_benefit += best_tuple[1]
    best_driver.SetFinalPassengers(best_tuple[0])
    the_drivers.append(best_driver)
    for p in best_tuple[0]:
      RemoveVertice(p)
    RemoveVertice(best_driver.trip_id)
      
  return max_benefit

# =================================
# Main
# =================================

# The program takes 2 arguments. One input file and one output file.
if len(sys.argv) != 3:
  print "Wrong number of arguments"
  sys.exit()

ReadInput(sys.argv[1])
max_benefit = GreedyMaxBenefit() 
WriteOutput(sys.argv[2])
