"""TEST ALL THE ALGORITHMS WITH THIS DOC. DO NOT DO IT WITH THE INDIVIDUAL TEST DOCS
Here, we aim to make general tests that compare different algorithms + save this information in a csv file"""

import csv
from thompson.sin_step.test import run_test as thompson_sin_step
from thompson.con_step.test import run_test as thompson_con_step
# from optimistic.test import run_test as optimistic
# from ucb.test import run_test as ucb
# from epsilon_greedy.test import run_test as epsilon_greedy
#  import os, sys
#  sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(_file_))))


"""HOW DO YOU THINK ROIs IS GOING TO BE IN THAT ENVIRONMENT?
we can change this variable by changing the dynamic function that is in the main.py of each algorithm
dynamic_mode = 'soft' #  maybe, we could put it as a new variable in the csv"""


"""THESE ARE THE INPUTS OF THE TEST, THE VARIABLES"""
# For the sake of uniformity in names: the possible names of the algorithms are =
# thompson_con_step, thompson_sin_step, optimistic, epsilon_greedy, optimistic, ucb
algorithm = 'thompson_con_step'
iterations = 4000
budget = 500000 #  random.randint(500, 9000000)
time = 10 #  random.randint(50, 200)
amount_campaigns = 10 #  random.randint(3, 8)
initial_rois_range = [0.4, 4] # which is the range of values we expect to get for the first ROI


"""THIS IS THE OUTPUT OF THE TEST, THE OVERALL ROI OBTAINED"""
if algorithm == 'thompson_sin_step':
    final_roi = thompson_sin_step(budget, time, amount_campaigns, iterations, initial_rois_range)

if algorithm == 'thompson_con_step':
    final_roi = thompson_con_step(budget, time, amount_campaigns, iterations, initial_rois_range)


print(f'FINAL ROI: {final_roi}')

""" ADD THIS INFORMATION INTO A CSV FILE"""
"""EXTREMELY IMPORTANT: running with mode='w', you will rewrite all the csv file so TAKE CARE
 use mode='a' to append new rows instead; when appending, comment out writer.writeheader() 
 because it will add the header in an intermediate row otherwise; that is only to create a new csv file"""

with open('test_data.csv', mode='a') as csv_file:
    fieldnames = ['ALGORITHM', 'ITERATIONS', 'BUDGET', 'TIME', 'AMOUNT CAMPAIGNS', 'INITIAL ROIS RANGE', 'FINAL ROI']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    row = {'ALGORITHM': algorithm, 'ITERATIONS': iterations, 'BUDGET': budget, 'TIME': time,
           'AMOUNT CAMPAIGNS': amount_campaigns, 'INITIAL ROIS RANGE': initial_rois_range, 'FINAL ROI': final_roi}

    #  writer.writeheader()
    writer.writerow(row)

