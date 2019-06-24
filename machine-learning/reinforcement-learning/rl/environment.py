import gym, numpy, imageio
from enum import Enum
from rl.preprocessing import ProcessBuffer, transform_state
from rl.utils import Signal

class EnvNames(Enum):

    SPACE_INVADER = 'SpaceInvadersNoFrameskip-v4'

class Environment():

    def __init__(self, env_name = EnvNames.SPACE_INVADER, NUM_FRAMES = 4, process_buffer = ProcessBuffer(4, transform_state), render = False):
        
        self.on_new_state = Signal()

        self.env = gym.make(env_name)
        self.life_count = None # To stop the game after the first life loss
        self.NUM_FRAMES = NUM_FRAMES # The number of time the action is repeated

        self.render = render

        self.process_buffer = process_buffer
        
        state = self.env.reset()
        
        if self.process_buffer is not None:
            self.process_buffer.reinit_buffer(state)
            self.shape = self.process_buffer.get_processed_state().shape
        else:
            self.shape = self.env.observation_space.shape
        
    def get_number_of_actions(self):
        """ return the number of actions"""
        return self.env.action_space.n
    
    def get_state_shape(self):
        return self.shape
    
    def update_life_count(self, info, done = False):

        if self.life_count is None:
            self.life_count = info['ale.lives']
            
        if info['ale.lives'] < self.life_count and not done:
            self.life_count = info['ale.lives']
            done = True
            
        return done

    def reset(self):
        """ Reset the environment and return the new state """
        state = self.env.reset()
        self.life_count = None
        self.process_buffer.reinit_buffer(state)

        return self.process_buffer.get_processed_state()

    def make_step(self, action):
        """ Return the next state, the reward, if the game has ended and some info"""
        states = []
        rewards = 0
        done = False
        info = None

        for i in range(self.NUM_FRAMES):

            state, reward, done, info = self.env.step(action)
            states.append(state)
            rewards += reward
            done = self.update_life_count(info, done)
            if done:
                info = None
                rewards = 0
                self.reset()
                break
        
        self.on_new_state.emit(state)
        state = self.process_buffer.add_state(numpy.amax(states, axis = 0))
        state = self.process_buffer.get_processed_state()

        if self.render:
            self.env.render()

        return state, rewards, done, info
