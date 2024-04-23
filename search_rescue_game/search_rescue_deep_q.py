import torch
import torch.nn as nn
import torch.optim as optim
import random
import gymnasium
from . import envs
import numpy as np
import matplotlib.pyplot as plt

#initializing the deep q neural network class
class Q_NeuralNet(nn.Module):
    def __init__(self, input, output):
        super(Q_NeuralNet, self).__init__()
        
        #input layer
        self.lyr1 = nn.Linear(input, 64)
        
        #hidden layer
        self.lyr2 = nn.Linear(64, 64)
        
        #output layer
        self.lyr3 = nn.Linear(64, output)

    def forward(self, x):
        x = torch.relu(self.lyr1(x))
        x = torch.relu(self.lyr2(x))
        return self.lyr3(x)

class Q_Agent:
    #may change learning rate
    def __init__(self, dim_state, dim_action, learning_rate=0.001, batch_size = 32):
        self.model = Q_NeuralNet(dim_state, dim_action)
        #learned what adam was 
        #source: https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
        #source: https://snyk.io/advisor/python/torch/functions/torch.optim.Adam 
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.memory = []
        self.batch_size = batch_size
        
    def recall(self, state, action, reward, next_state, done):
        if isinstance(state, tuple):  
            state = state[0]
        if isinstance(next_state, tuple):  
            next_state = next_state[0]
        self.memory.append((state, action, reward, next_state, done))
        
    def train(self):
        if len(self.memory) < self.batch_size:
            return
        
        sample = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*sample)
        
        states = np.array([np.array(state) for state in states])  # Ensure all are numpy arrays
        next_states = np.array([np.array(state) for state in next_states])
        
        
        #making tensors for training
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)
        
        current_q = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        next_q  = self.model(next_states).max(1)[0]
        
        #bellman 
        expected_q =  rewards + 0.99 * next_q * (1 - dones)
        
        #handling losses, back propagation
        loss = self.criterion(current_q, expected_q.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
    def play_game(self, state, epsilon):
        #exploration vs exploitation code
        if random.random() < epsilon:
            return random.randint(0, self.model.lyr3.out_features - 1)
        else:
            if isinstance(state, tuple):
                state_numeric = state[0]
            elif isinstance(state, np.ndarray):
                state_numeric = state
            else:
                raise ValueError("Unrecognized state format")

            if not isinstance(state_numeric, np.ndarray):
                state_numeric = np.array(state_numeric)
                
            state_tensor = torch.tensor(state_numeric, dtype=torch.float32).unsqueeze(0)
            
            if state_tensor.shape[1] != self.model.lyr1.in_features:
                raise ValueError("incorrect state shape. expected {self.model.fc1.in_features}, got {state_tensor.shape[1]}")
        
            with torch.no_grad():
                return self.model(state_tensor).argmax().item()



##++_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_++_+_+___

total_episodes = 500
# total_episodes = 50       

if __name__ == "__main__":
    
    env = gymnasium.make("map-random-10x10-v0", render_mode = "rgb_array")
    agent = Q_Agent(dim_state=env.observation_space.shape[0], dim_action=env.action_space.n, learning_rate=0.001, 
                    batch_size=32)

    #so i can track and plot
    total_rewards = []
    
    
    for episode in range(total_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.play_game(state, epsilon=0.1)
            next_state, reward, terminated, truncated, info = env.step(action)
            agent.recall(state, action, reward, next_state, done)
            done = terminated or truncated
            
            agent.recall(state, action, reward, next_state, done)
            agent.train()
            
            state = next_state
            total_reward += reward
        
        total_rewards.append(total_reward)
        
        #commenting out to speed up run
        print(f"Episode: {episode}, Total reward: {total_reward}")
    
    
    env.close()
    
##++_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_++_+_+___

#plotting

# plt.plot(total_rewards)
# plt.title('Total Rewards per Episode')
# plt.xlabel('Episode')
# plt.ylabel('Total Reward')
# plt.show()

import json
with open('deep_q_rewards.json', 'w') as f:
    json.dump(total_rewards, f)