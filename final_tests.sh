#!/bin/bash
FILES=complete_tests/*
for f in $FILES; do
  echo "Testing $f..."
  echo "Brute force"
  python brute_force.py $f x 
  echo "Dynamic programming"
  python dynamic_programming.py $f x 
  echo "Greedy"
  python greedy.py $f x
done
