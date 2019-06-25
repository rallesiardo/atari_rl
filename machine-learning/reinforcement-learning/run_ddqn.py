from rl.agents import DoubleDQN, DQNParameters
from rl.brain import DQN
from rl.environment import get_env_and_input_layer, EnvNames
from rl.game import Game
from rl.monitoring import Monitor


if __name__ == "__main__":
    """
    env, input_net = get_env_and_input_layer(env_name=EnvNames.POLECART, render=False)
    param = DQNParameters(capacity=10000, waiting_time = 1000, lr = 1E-4, frozen_steps=100, gamma=0.99)
    brain = DQN(input_net, env.get_number_of_actions())
    agent = DoubleDQN(brain, param)
    game = Game(agent, env)

    monitor = Monitor(agent, game)

    game.run(100000)
    """
    env = AtariEnvironment(env_name=EnvNames.SPACE_INVADER, render=False)
    brain = AtariDQN(env.get_number_of_actions())    
    agent = DoubleDQN(brain)
    game = Game(agent, env)

    monitor = Monitor(agent, game)

    game.run(horizon=10000000)
