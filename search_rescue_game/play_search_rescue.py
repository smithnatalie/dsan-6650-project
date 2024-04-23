#this is a "main()" style file that runs both the tabular and deep q learning games at the same time
#then the results are plotted together

import matplotlib.pyplot as plt
from search_rescue_tabular_q import run_tabular_q_learning

#SHALLOW RL - Tabular Q Learning
    
def plot_results(tabular_rewards, deep_rewards):
    plt.figure(figsize=(10, 5))
    plt.plot(tabular_rewards, label='Tabular Q-Learning Rewards')
    plt.plot(deep_rewards, label='Deep Q-Learning Rewards')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Comparison of Tabular and Deep Q-Learning Rewards')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    tabular_rewards = run_tabular_q_learning()
    # deep_rewards = run_deep_q_learning()
    plot_results(tabular_rewards)#, deep_rewards)