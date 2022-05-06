import numpy as np
from thompson.con_step.main import *
from scipy.stats import norm
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

class ThompsonCampaign(object):
    """ This class has information about the probability distribution of the ROI estimate for each campaign"""
    def __init__(self, id):
        self.id = id
        self.N = 0  # Time step num
        self.variance = 100  # Flatten distributions
        self.sum = 0  # sum of ROI across time steps
        self.mean_estimate = 0  # ROI mean estimate
        self.spent_campaign = []
        self.profitability_campaign = []  # absolute return on that campaign

    def update(self, roi, spent):
        """ updates the mean estimate and the variance given a new roi and new spent (in the last time step)"""
        self.variance = pow((1 / pow(100, 2) + self.N), -1)
        self.spent_campaign.append(spent)
        self.profitability_campaign.append(roi * spent)
        self.mean_estimate = sum(self.profitability_campaign) / sum(self.spent_campaign)
        self.N += 1

    def sample(self):
        return np.random.randn() / np.sqrt(self.variance) + self.mean_estimate


class ThompsonAgent(object):
    def __init__(self, state):
        self.state = state

    def act(self):
        """updates the t_campaigns distributions"""
        for i, t_campaign in enumerate(self.state.t_campaigns):
            t_campaign.update(self.state.campaigns[i].roi[-1], self.state.campaigns[i].spent[-1])

        """samples each distribution, choose one arm to increase a step and one arm to decrease"""
        samples = []
        for t_campaign in self.state.t_campaigns:
            samples.append(t_campaign.sample())

        self.state.budget_percentual_allocation[samples.index(min(samples))] -= self.state.step
        self.state.budget_percentual_allocation[samples.index(max(samples))] += self.state.step

        distribution = [round(num, 4) for num in self.state.budget_percentual_allocation]

        """updates state.percentual_budget_allocation """
        self.state.update(distribution)

    def plot(self):
        """plots the current probability distributions of the existing campaigns """
        x = np.linspace(-3, 6, 200)
        for t_campaign in self.state.t_campaigns:
            y = norm.pdf(x, t_campaign.mean_estimate, np.sqrt(t_campaign.variance))
            plt.plot(x, y, label=f"estimated mean: {t_campaign.mean_estimate:.4f}")
        plt.title(f"Bandit distributions after {self.state.current_time} time steps")
        plt.legend()
        plt.show()
