import numpy as np

class Q_learning():
    def __init__(self, alpha = 0.1, gamma = 0.99, epsilon = 0.1, n = 54, num_actions = 4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n = n
        self.num_actions = num_actions

        self.w = np.zeros((n,num_actions))
        self.delta = 0.0
        self.q_value = 0.0
        self.next_q_value = 0.0

    def Q_value(self, features, action):
        self.q_value = np.sum(self.w[features,action])

    def calc_q_value(self, features, action):
        return np.sum(self.w[features,action])

    def greedy_Q(self, features):
        q_vals = np.sum(self.w[features,:], axis=0)
        maxQ = np.max(q_vals)
        greedy_action = np.argmax(q_vals)
        return  maxQ, greedy_action

    def Next_Q_value(self,features):
        q_vals = np.sum(self.w[features, :], axis=0)
        self.next_q_value = np.max(q_vals)
        greedy_action = np.argmax(q_vals)

    def calc_delta(self, reward):
        self.delta = reward + self.gamma*self.next_q_value - self.q_value

    def weight_update(self, features, action):
        self.w[features, action] += self.alpha*self.delta

    def sample_action(self, features):
        maxQ, greedy_action = self.greedy_Q(features=features)
        if np.random.rand() < self.epsilon:
            return np.random.choice(range(self.num_actions))
        else:
            return greedy_action

    def master_func(self, current_features, next_features, reward, action):
        self.Q_value(current_features, action)
        self.Next_Q_value(next_features)
        self.calc_delta(reward)
        self.weight_update(features=current_features, action=action)
