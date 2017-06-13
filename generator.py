import sys
import random

def GenerateGraph(n, m):
  # Generate vertices.
  print n
  for i in range(n): 
    passenger = True
    driver = True

    num_passengers = int(random.random() * 10) + 1
    vacant_seats = num_passengers + int(random.random() * 10)
    benefit = random.random() * 100
    print i + 1, "1 1", num_passengers, vacant_seats, round(benefit, 2)

  # Generate edges.
  arr = [] 

  print m
  counter = 0
  for i in range(n): 
    for j in range(n): 
      if i != j:
        arr.append((i + 1, j + 1))

  random.shuffle(arr)
  for i in range(m): 
    print arr[i][0], arr[i][1]

if len(sys.argv) != 3:
  print "Wrong number of arguments"
  sys.exit()

GenerateGraph(int(sys.argv[1]), int(sys.argv[2]))
