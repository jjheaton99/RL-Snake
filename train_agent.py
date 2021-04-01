import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from tensorforce.agents import Agent
from tensorforce.execution import Runner

from snake_environment import SnakeEnvironment

environment = SnakeEnvironment()
agent = Agent.create(agent='dqn', 
                     environment=environment, 
                     batch_size=10, 
                     learning_rate=1e-3,
                     network=dict(type='auto',
                                  size=64,
                                  depth=4),
                     memory=10000,
                     #exploration=0.01,
                     #l2_regularization=0.1,
                     #huber_loss=1.0,
                     saver=dict(directory='agents',
                                frequency=1000),
                     )

runner = Runner(agent=agent,
                environment=environment,
                max_episode_timesteps=1000000)

runner.run(num_episodes=10000)

runner.run(num_episodes=10, evaluation=True)

runner.close()