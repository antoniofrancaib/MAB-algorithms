from cmath import isnan
import random
import numpy as np
import matplotlib.pyplot as plt
import copy
from epsilongreedy import *

class Campaign():

    def __init__(self,id,budget,spent,impressions,conversions,roi):
        #falta determinar como podemos saber el tiempo que lleva la campaña 
        self.id = id    
        self.budget = budget #daily budget
        self.spent = spent
        self.impressions = impressions
        self.conversions = conversions
        self.roi = roi

    def update(self,impressions,conversions,roi):
        self.spent += self.budget
        self.impressions += int(impressions)
        self.conversions += int(conversions)
        self.roi = float(roi)

    def change_budget(self,increment):
        #increment debe ser un valor numerico para editar el ( daily budget )
        self.budget = self.budget + increment
    

class State(Campaign):

    def __init__(self,budget,total_time,campaigns,initial_allocation=0):
        self.budget = budget
        self.time = total_time
        self.campaigns = campaigns
        self.current_time = 0
        self.current_budget = self.budget/self.time
        #dictionary that contains all states, where the key is a timestamp
        self.history = {}
        self.budget_allocation = {}
        self.remaining = budget

        self.step = 0.005

        self.k_arms = len(campaigns)

        self.stopped = []
        if initial_allocation == 0: 
            self.initial_allocation()
        else:
            for campaign in campaigns:
                self.budget_allocation[campaign.id] = initial_allocation[campaign.id]

    def next_timestamp(self):
        self.current_time += 1
        self.remaining-=self.current_budget
        if self.remaining <= 0:
            raise Exception('No budget left')
        #increase the capacity of an agent to take significant budget decisions
        self.step *= 1.001


    def get_reward(self):
        if self.current_time == 0:
            return list(np.zeros(len(self.budget_allocation)))
        rewards = [] 
        for campaign in self.campaigns:
            rewards.append(campaign.roi*self.current_budget*self.budget_allocation[campaign.id])
        # norm = [float(i)/sum(rewards) for i in rewards]
        #print(f'The rewards at timestamp {self.current_time} is {rewards}')
        return rewards

    def take_action(self,arm,q_values):
        random_action = []
        if self.current_time < 1:
            print('AI still has no data so no action taken')
        else:
            print(f'AI is increasing budget of campaign {arm}')
            self.act2(arm,q_values)
        b = copy.deepcopy(self.budget_allocation)
        rewards = self.get_reward()
        self.history[self.current_time] = [b,rewards]
        print(f'Current state: {self.budget_allocation} at timestamp {self.current_time}')
        self.allocate_budget()
        self.next_timestamp()
        return rewards

    def act2(self, arm, q_values):
        """
        Given a chosen campaign, change budget distribution.
        The policy is to increase with step % campaigns[arm],
        and decrease another arm based on
        stochastic process based on q_values.
        """
        population = list(range(len(self.campaigns)))  # list of campaigns to index
        step = self.step  # step = degrees of freedom
        temp_budget = copy.deepcopy(self.budget_allocation)  # create a temporary variable  ( if not we overwrite )
        temp_budget[arm] += step  # we increase campaign[arm]
        q_values = q_values.tolist()  # we transform q_values to a list

        """
        stochastic process to choose and decrease another campaign 
        """
        # SOLUTION TO BUG  7
        if len(population) - len(self.stopped) == 1:
            temp_budget[arm] = 1
        else:
            """
            if we have no data, randomly decrease a campaign
            """
            if all(v == 0 for v in q_values):
                dec = random.randint(0, len(self.campaigns) - 1)
                if dec != arm:
                    temp_budget[dec] -= step
                else:
                    while dec == arm:
                        dec = random.randint(0, len(self.campaigns) - 1)
                    temp_budget[dec] -= step
                """
            if we have data, take a stochastic approach 
                """
            else:
                norm = [float(i) / sum(q_values) for i in q_values]
                decrease_prob = [1 - p for p in norm]
                dec = int(random.choices(population, weights=decrease_prob, k=1)[0])
                if dec != arm and dec not in self.stopped:
                    # TSOLUTION OF BUG 1
                    if temp_budget[dec] < step:
                        temp_budget[arm] -= temp_budget[dec]
                        temp_budget[dec] = 0
                        print(f'##### Campaign {dec} was stopped completely ###')
                        # BUG 3 delete campaign from the state ( make it ignore it )
                        self.stopped.append(dec)
                    else:
                        temp_budget[dec] -= step
                else:
                    while True:
                        dec = int(random.choices(population, weights=decrease_prob, k=1)[0])
                        if dec == arm:
                            continue
                        if dec in self.stopped:
                            continue
                        else:
                            break
                    # SOLUTION OF BUG 1
                    if temp_budget[dec] < step:
                        temp_budget[arm] -= temp_budget[dec]
                        temp_budget[arm] -= step
                        temp_budget[dec] = 0
                        print(f'##### Campaign {dec} was stopped completely ###')
                        self.stopped.append(dec)
                    else:
                        temp_budget[dec] -= step
                print(f'Ai has decreased campaign {dec} given probs {decrease_prob}')

        for campaign in temp_budget:
            temp_budget[campaign] = round(temp_budget[campaign], 8)
        assert self.validate_budget(temp_budget)
        self.budget_allocation = temp_budget
            
    @staticmethod        
    def get_state(budget_allocation):
        return tuple(budget_allocation.values())

    def initial_allocation(self):
        for campaign in self.campaigns:
            self.budget_allocation[campaign.id] = round(1/len(self.campaigns),8)
        b = copy.deepcopy(self.budget_allocation)
        self.history[self.current_time] = [b,self.get_reward()]
        self.allocate_budget()

    def allocate_budget(self):
        #turns a distribution into a value
        #campaign budget = current budget * campaign%allocation
        for campaign in self.campaigns:
            campaign.budget = round(self.current_budget*self.budget_allocation[campaign.id],8)
        
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
            #it is better that we spend less than more. 
            return True
        else:
            return False
    
    def dynamic(self):
        for campaign in self.campaigns:
            a = random.randint(0,2)
            if a == 0:
                campaign.roi *= 1.05
            elif a == 1:
                if campaign.roi > 1:
                    campaign.roi *= 0.95
                elif campaign.roi > 0:
                    campaign.roi *= 0.99
                else:
                    campaign.roi *= 1.01
            else: 
                return self
    
                