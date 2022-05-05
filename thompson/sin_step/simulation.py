from main import *
from thompson import *
import numpy as np

budget = 1000             #input('Introduce amount of budget: ')
time = 100                  #input('Introduce total number of time steps: ')
amount_campaigns = 3        #input('How many campaigns would you like to initialize?: ')

"""COLLECT INFORMATION OF EVERY CAMPAIGN: """
"""1) Collect id names of each campaign  # id_names as the names of the platforms i.e. Facebook, Snapchat, etc
id_names = []
for i in range(amount_campaigns):
    id_names.append(input(f'ID name of campaign {i + 1}: '))"""
id_names = ['facebook', 'instagram', 'snapchat']

"""2) Collect last ROI estimates for each campaign 
answer1 = input('Any ROI to fulfill beforehand? (answer y OR n): ')
ROIs = []
if answer1 == 'y':
    for name in id_names:
        ROIs.append(input(f'ROI estimate for campaign {name}'))
else:
    for i in range(amount_campaigns):
        ROIs.append(np.random.uniform(0.5, 1.5))"""
initial_ROIs = []
for i in range(amount_campaigns):
    initial_ROIs.append(np.random.uniform(1.2, 2.5))

"""3) Collect if wished a guess initial allocation, otherwise assign an egalitarian one 
This initial_allocation is asked in a percentual way e.g. {facebook: 0.6, snapchat: 0.2, instagram: 0.2}

answer2 = input('Any initial_allocation to fulfill beforehand? (answer y OR n): ')
initial_percentual_allocation = {}
if answer2 == 'y':
    while sum(initial_percentual_allocation.values) != 1:
        for name in id_names:
            initial_percentual_allocation[name] = input(f'{name}: ')
else:
    for name in id_names:
        initial_percentual_allocation[name] = 1 / amount_campaigns"""
initial_percentual_allocation = {}
for name in id_names:
    initial_percentual_allocation[name] = 1 / amount_campaigns

"""INITIALIZE CAMPAIGNS and THOMPSON CAMPAIGNS, we use ROI list and initial_budget_allocation list"""
initial_budget_allocation = [(budget / time) * initial_percentual_allocation[i] for i in initial_percentual_allocation]
campaigns = []
t_campaigns = []
for n in range(amount_campaigns):
    campaigns.append(Campaign(id_names[n],initial_budget_allocation[n],0,0,initial_ROIs[n]))
    t_campaigns.append(ThompsonCampaign(id_names[n]))

"""INITIALIZE STATE and THOMPSON AGENT"""
state = State(budget,time,campaigns,t_campaigns, initial_percentual_allocation)
thompson_agent = ThompsonAgent(state)

"""Actuación del conserje"""

for i in range(10):
    budgets = [campaign.budget for campaign in campaigns]
    print('\n#######################################################################\n')
    print(f'BUDGET FOR TIME STEP {state.current_time + 1}: {state.current_budget}\n')
    print(f'Budget percentual distribution {state.budget_percentual_allocation}')
    print(f'Budget distribution: {budgets}') # change to dictionary instead

    rois_obtained = [campaign.roi[-1] for campaign in state.campaigns]
    print(f'ROIs for each campaign: {rois_obtained}')

    """this function gives a spent value to the state and ROI values for every campaign, simulates the real world """
    state.dynamic(budgets)

    """ thompson acts: changes state.budget_percentual_allocation
    --> gives the next time step budget for each campaign according to that allocation
    --> updates current_time and remaining_budget"""
    thompson_agent.act()

    """plot distributions"""
    #  thompson_agent.plot()

    """para ver como se actualiza el mean_estimate y la variance
    for i, t_campaign in enumerate(t_campaigns):
        print(f'Mean estimate t_campaign {i + 1}: {t_campaign.mean_estimate}')
        print(f'Variance t_campaign {i + 1}: {t_campaign.variance}')
        print(f'Profitability t_campaign {i + 1}: {sum(t_campaign.profitability_campaign)}')
        print(f'Spent t_campaign {i + 1}: {sum(t_campaign.spent_campaign)}')"""

"""RESULTADO FINAL: Este es el beneficio total de haber seguido esta politica de accion"""
absolute_profit = []
total_spent = []
for t_campaign in t_campaigns:
    absolute_profit.append(sum(t_campaign.profitability_campaign))
    total_spent.append(sum(t_campaign.spent_campaign))

print('\n#######################################################################\n')
print('----------------------------GENERAL RESULTS----------------------------')
print(f'ABSOLUTE PROFIT: {sum(absolute_profit)}')
print(f'TOTAL SPENT: {sum(total_spent)}')
print(f'NET PROFIT: {sum(absolute_profit) - sum(total_spent)}')
print(f'PERCENTUAL PROFIT: {round((sum(absolute_profit) / sum(total_spent)) * 100 - 100, 2)}% of final ROI')


