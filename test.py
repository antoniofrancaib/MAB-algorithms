"""Here, we aim to make general tests that automatically save the information in a csv file"""

from thompson.sin_step.test import run_test as thompson_sin_step
# from thompson.con_step.test import run_test as thompson_con_step
# from optimistic.test import run_test as optimistic
# from ucb.test import run_test as ucb
# from epsilon_greedy.test import run_test as epsilon_greedy

"""THESE ARE THE INPUTS OF THE TEST, THE VARIABLES"""
# For the sake of uniformity in names: the possible names of the algorithms are =
# thompson_con_step, thompson_sin_step, optimistic, epsilon_greedy, optimistic, ucb
algorithm = 'thompson_sin_step'
iterations = 2000
total_budget = 5000 #  random.randint(500, 9000000)
total_time = 100 #  random.randint(50, 200)
amount_campaigns = 3 #  random.randint(3, 8)
initial_rois_range = [1.2, 2.6] # which is the range of values we expect to get for the first ROI

"""THIS IS THE OUTPUT OF THE TEST, THE OVERALL ROI OBTAINED"""
if algorithm == 'thompson_sin_step':
    roi = thompson_sin_step(total_budget, total_time, amount_campaigns, iterations, initial_rois_range)
    print(roi)

# if algorithm == 'thompson_con_step':
#     roi = thompson_con_step(total_budget, total_time, amount_campaigns, iterations, initial_rois_range)