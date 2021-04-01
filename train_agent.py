import numpy as np

import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from tensorforce.agents import Agent
from tensorforce.execution import Runner

from snake_environment import SnakeEnvironment

directory = 'agents/conv'
filename = 'dqn_agent'

epsilon_decay = {'type': 'decaying',
                 'decay': 'exponential',
                 'unit' : 'episodes',
                 'num_steps': 10,
                 'initial_value': 1.0,
                 'decay_rate': 5e-2}

dense_network = dict(type='auto',
                     size=64,
                     depth=4)

conv_network = [dict(type='conv2d', size=32),
                dict(type='conv2d', size=32),
                dict(type='flatten'),
                dict(type='dense', size=64),
                dict(type='dense', size=64)]

agent_config = {
    'agent': 'dqn',
    'memory': 200000,
    'batch_size': 25,
    'network': conv_network,
    'learning_rate': 1e-3,
    'discount': 0.99,
    'exploration': epsilon_decay,
    'target_update_weight': 1.0,
    }

env = SnakeEnvironment(network_type='conv')

agent = Agent.create(agent=agent_config,
                     environment=env)
                   
runner = Runner(agent=agent,
                environment=env)

runner.run(num_episodes=10000)
runner.agent.save(directory=directory, filename=filename)

rewards = np.asarray(runner.episode_rewards)
episode_lengths = np.asarray(runner.episode_timesteps)

np.savetxt('agents/conv/rewards.txt', rewards)
np.savetxt('agents/conv/episode_lengths.txt', episode_lengths)

runner.close()


