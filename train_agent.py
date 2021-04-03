import numpy as np

import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from tensorforce.agents import Agent
from tensorforce.execution import Runner

from snake_environment import SnakeEnvironment

epsilon_decay = {'type': 'decaying',
                 'decay': 'polynomial',
                 'unit' : 'episodes',
                 'num_steps': 50,
                 'initial_value': 1.0,
                 'final_value': 0.0,
                 'decay_rate': 5e-2,
                 'power': 2}

dense_network = dict(type='auto',
                     size=64,
                     depth=4)

conv_network = [dict(type='conv2d', size=16, window=4, stride=2, padding='valid'),
                dict(type='conv2d', size=32, window=3, stride=1, padding='valid'),
                dict(type='flatten'),
                dict(type='dense', size=64),
                dict(type='dense', size=64)]

multi_network = [
        [
            dict(type='retrieve', tensors=['image_input']),
            dict(type='conv2d', size=8, window=4, stride=2, padding='valid'),
            dict(type='conv2d', size=16, window=4, stride=1, padding='valid'),
            dict(type='conv2d', size=32, window=4, stride=1, padding='valid'),
            dict(type='conv2d', size=64, window=3, stride=1, padding='valid'),
            dict(type='flatten'),
            dict(type='dense', size=64),
            dict(type='register', tensor='conv_output')
        ],
        [
            dict(type='retrieve', tensors=['info_input']),
            dict(type='dense', size=64),
            dict(type='dense', size=64),
            dict(type='register', tensor='dense_output')
        ],
        [
            dict(type='retrieve', aggregation='concat',
                 tensors=['conv_output', 'dense_output']),
            dict(type='dense', size=64),
            dict(type='dense', size=64)
        ]
    ]

dense_env = SnakeEnvironment(network_type='dense')
dense_config = {'agent': 'dqn',
                'memory': 200000,
                'batch_size': 25,
                'network': dense_network,
                'learning_rate': 1e-3,
                'discount': 0.99,
                'exploration': epsilon_decay,
                'target_update_weight': 1.0}

conv_env = SnakeEnvironment(network_type='conv')
conv_config = {'agent': 'dqn',
               'memory': 200000,
               'batch_size': 25,
               'network': conv_network,
               'learning_rate': 1e-3,
               'discount': 0.99,
               'exploration': epsilon_decay,
               'target_update_weight': 1.0}

multi_env = SnakeEnvironment(network_type='multi')
multi_config = {'agent': 'dqn',
               'memory': 200000,
               'batch_size': 25,
               'network': multi_network,
               'learning_rate': 1e-3,
               'discount': 0.99,
               'exploration': epsilon_decay,
               'target_update_weight': 1.0}

multi_ddqn_config = {'agent': 'ddqn',
               'memory': 200000,
               'batch_size': 25,
               'network': multi_network,
               'learning_rate': 1e-3,
               'discount': 0.99,
               'exploration': epsilon_decay,
               'target_update_weight': 1.0}
                   
if __name__ == '__main__':
    """
    agent = Agent.create(agent=multi_config,
                         environment=multi_env)
    
    runner = Runner(agent=agent,
                    environment=multi_env)

    runner.run(num_episodes=10000)
    runner.agent.save(directory='agents/multi', filename='dqn_agent')
    
    rewards = np.asarray(runner.episode_rewards)
    episode_lengths = np.asarray(runner.episode_timesteps)
    
    np.savetxt('agents/multi/rewards.txt', rewards)
    np.savetxt('agents/multi/episode_lengths.txt', episode_lengths)
    """
    
    agent = Agent.create(agent=multi_ddqn_config,
                         environment=multi_env)
    
    runner = Runner(agent=agent,
                    environment=multi_env)

    runner.run(num_episodes=10000)
    runner.agent.save(directory='agents/multi_ddqn', filename='dqn_agent')
    
    rewards = np.asarray(runner.episode_rewards)
    episode_lengths = np.asarray(runner.episode_timesteps)
    
    np.savetxt('agents/multi_ddqn/rewards.txt', rewards)
    np.savetxt('agents/multi_ddqn/episode_lengths.txt', episode_lengths)
    
    runner.close()
