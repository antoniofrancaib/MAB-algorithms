from cmath import isnan
from dataclasses import dataclass
import random
from xml.sax import parseString
import numpy as np
import matplotlib.pyplot as plt
import copy
from thompson import *

@dataclass
class Campaign():
    def __init__(self, id, budget, impressions, conversions, roi):
        """IMPORTANTE: en caso de que se introduzcan parametros (i.e. impressions, conversions, roi, etc),
        han de introducirse como el valor medio (mean_estimate) conocido hasta la fecha
        falta determinar como podemos saber el tiempo que lleva la campaña """
        self.id = id
        self.budget = budget  # daily budget
        self.impressions = [impressions]
        self.conversions = [conversions]
        self.roi = [roi]
        self.spent =[]


class State(Campaign):
    def __init__(self, total_budget, total_time, campaigns, t_campaigns, initial_percentual_allocation):
        self.total_budget = total_budget
        self.remaining_budget = total_budget
        self.total_time = total_time
        self.campaigns = campaigns
        self.t_campaigns = t_campaigns
        self.current_time = 0
        self.spent = []
        self.current_budget = self.remaining_budget / self.total_time
        self.history = {}  # key is time step, value is state
        self.budget_percentual_allocation = initial_percentual_allocation

    def update(self, distribution):
        """updates the budget_distribution in the state"""
        for i, campaign in enumerate(self.budget_percentual_allocation):
            self.budget_percentual_allocation[campaign] = distribution[i]
        assert self.validate_budget(self.budget_percentual_allocation), 'Budget distribution is incorrect'
        self.allocate_budget()
        self.next_step()

    def allocate_budget(self):
        """updates the next time step budget for each campaign"""
        for campaign in self.campaigns:
            campaign.budget = round(self.current_budget * self.budget_percentual_allocation[campaign.id], 8)

    def next_step(self):
        """updates current time, and remaining_budget """
        self.current_time += 1
        self.remaining_budget -= self.spent[-1]
        if self.remaining_budget <= 0:
            raise Exception('No budget left')
        #restamos al remaining SOLO lo que se ha gastado en el time step, no lo que se le ha asignado gastar

    def dynamic(self, budget_distribution):
        """gives new ROI, gives new spent, i.e. simulates an interaction with the real world
        adds a new roi for every roi list of each campaign, adds a new spent for the list in the state"""
        for campaign in self.campaigns:
            a = random.randint(0, 2)
            roi_obtained = []
            if a == 0:
                roi_obtained.append(campaign.roi[-1] * 1.05)
            elif a == 1:
                if campaign.roi[-1] > 1:
                    roi_obtained.append(campaign.roi[-1] * 0.95)
                elif campaign.roi[-1] > 0:
                    roi_obtained.append(campaign.roi[-1] * 0.99)
                else:
                    roi_obtained.append(campaign.roi[-1] * 1.01)
            else:
                roi_obtained.append(campaign.roi[-1])
            campaign.roi.append(sum(roi_obtained))

        total_spent = []
        for i, budget in enumerate(budget_distribution):
            percentual_spent = random.randint(95, 100)
            spent = (percentual_spent / 100)*budget
            total_spent.append(spent)
        self.spent.append(sum(total_spent))
        for i, campaign in enumerate(self.campaigns):
            campaign.spent.append(total_spent[i])

    @staticmethod
    def get_state(budget_allocation):
        return tuple(budget_allocation.values())


    @staticmethod
    def validate_budget(budget_allocation):
        total = 0
        for campaign in budget_allocation.values():
            if campaign > 1: return False
            elif campaign < 0: return False
            else:
                total += campaign
        total = round(total,4)
        if total > 0.95 and total <= 1.025:
            return True
        else: return False