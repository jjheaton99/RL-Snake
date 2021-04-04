import numpy as np
import matplotlib.pyplot as plt

rewards = np.loadtxt('agents/multi_ddqn/rewards.txt')[0:2999]
episode_lengths = np.loadtxt('agents/multi_ddqn/episode_lengths.txt')[0:2999]

fig, axis = plt.subplots(2)
fig.suptitle('Multi-input DDQN agent training history')

axis[0].plot(rewards)
axis[0].set_xlabel('Episode number')
axis[0].set_ylabel('Reward')

axis[1].plot(episode_lengths)
axis[1].set_xlabel('Episode number')
axis[1].set_ylabel('Number of timesteps')

plt.show()