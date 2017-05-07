import numpy as np

class Q_learning():
    def __init__(self, alpha = 0.1, gamma = 0.99, lmbda=0.1, epsilon = 0.1, n = 54, num_actions = 4):
        self.alpha = alpha
        self.gamma = gamma
        self.lmbda = lmbda
        self.epsilon = epsilon
        self.n = n
        self.num_actions = num_actions

        self.w = np.zeros((n,num_actions))
        self.e = np.zeros((n,num_actions))
        self.delta = 0.0
        self.q_value = 0.0
        self.next_q_value = 0.0
        self.greedy = False

    def Q_value(self, features, action):
        self.q_value = self.w[features,action]

    def calc_q_value(self, features, action):
        return self.w[features,action]

    def greedy_Q(self, features):
        q_vals = self.w[features,:]
        maxQ = np.max(q_vals)
        if np.unique(q_vals).size == 1:
            greedy_action = np.random.choice(range(self.num_actions))
        else:
            greedy_action = np.argmax(q_vals)
        return  maxQ, greedy_action

    def Next_Q_value(self,features):
        q_vals = self.w[features, :]
        self.next_q_value = np.max(q_vals)

    def calc_delta(self, reward):
        self.delta = reward + self.gamma*self.next_q_value - self.q_value

    def weight_update(self, features, action):
        self.w[features, action] += self.alpha*self.delta

    def sample_action(self, features):
        maxQ, greedy_action = self.greedy_Q(features=features)
        if np.random.rand() < self.epsilon:
            action = np.random.choice(range(self.num_actions))
            self.greedy = False
        else:
            action = greedy_action
            self.greedy = True
        return action

    def async_delta_calc(self, reward):
        return reward + self.gamma * self.next_q_value - self.q_value

    def master_func(self, current_features, next_features, reward, action):
        self.Q_value(current_features, action)
        self.Next_Q_value(next_features)
        self.calc_delta(reward)
        self.weight_update(features=current_features, action=action)

