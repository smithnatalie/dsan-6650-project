#this is a "main()" style file that runs both the tabular and deep q learning games at the same time
#then the results are plotted together

import matplotlib.pyplot as plt

#SHALLOW RL - Tabular Q Learning
def run_tabular_q_learning():
    from search_rescue_tabular_q import run