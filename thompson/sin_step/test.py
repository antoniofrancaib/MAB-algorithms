from main import *
from thompson import *
import numpy as np
import random


def test(budget, time, amount_campaigns):

    id_names = []
    initial_rois = []
    for i in range(amount_campaigns):
        id_names.append(i)
        initial_rois.append(np.random.uniform(1.2, 2.6))

    initial_percentual_allocation = {}
    for name in id_names:
        initial_percentual_allocation[name] = 1 / amount_campaigns

    initial_budget_allocation = [(budget / time) * initial_percentual_allocation[i] for i in
                                 initial_percentual_allocation]
    campaigns = []
    t_campaigns = []
    for n in range(amount_campaigns):
        campaigns.append(Campaign(id_names[n], initial_budget_allocation[n], 0, 0, initial_rois[n]))
        t_campaigns.append(ThompsonCampaign(id_names[n]))

    state = State(budget, time, campaigns, t_campaigns, initial_percentual_allocation)
    thompson_agent = ThompsonAgent(state)

    for i in range(10):
        budgets = [campaign.budget for campaign in campaigns]
        state.dynamic(budgets)
        thompson_agent.act()

    absolute_profit = []
    total_spent = []
    for t_campaign in t_campaigns:
        absolute_profit.append(sum(t_campaign.profitability_campaign))
        total_spent.append(sum(t_campaign.spent_campaign))

    return round((sum(absolute_profit) / sum(total_spent)) * 100 - 100, 2)


iterations = 2000

total_budget = 5000 #  random.randint(500, 9000000)
total_time = 100 #  random.randint(50, 200)
amount_campaigns = 3 #  random.randint(3, 8)

total_results = []
for i in range(iterations):
    result = test(total_budget, total_time, amount_campaigns)
    total_results.append(result)

average_ROI = sum(total_results) / iterations
print(f'AVERAGE ROI: {round(average_ROI, 2)}%')

