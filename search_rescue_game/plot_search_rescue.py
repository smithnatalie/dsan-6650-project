#this is a "main()" style file that runs both the tabular and deep q learning games at the same time
#then the results are plotted together
import matplotlib.pyplot as plt
import json

def load_rewards(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    

def plot_results(tabular_rewards, deep_rewards):
    plt.figure(figsize=(12, 6))
    plt.plot(tabular_rewards, label="Tabular Q-Learning", color = "red")
    plt.plot(deep_rewards, label="Deep Q-Learning", color = "blue")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    # plt.title("Tabular vs Deep Q-Learning Rewards (50 Episodes)")
    plt.title("Tabular vs Deep Q-Learning Rewards (500 Episodes)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    tabular_rewards = load_rewards("tabular_q_rewards.json")
    deep_rewards = load_rewards("deep_q_rewards.json")
    plot_results(tabular_rewards, deep_rewards)