# Author: xuejinlin
# Date: 2023/3/6 22:18
"""An OpenAI Gym Super Mario Bros. environment that randomly selects levels."""
import gym
import numpy as np
from nes_py.nes_env import SCREEN_HEIGHT, SCREEN_WIDTH
from .infer.python.infer import Infer
import os
from PIL import Image
from .status import categories
from .actions import move_handle,skill_handle,skill_upgrade_handle,threez_handle,shopping_handle,map_handel

class HeroKeyEnv(gym.Env):
    def __init__(self,scrypt=False,img_dir=None):
        self.img_dir = img_dir
        self.img_files = []
        if img_dir is not None:
            self.img_files = os.listdir(img_dir)
        self.scrypt = scrypt
        self._init_();
        self.infer = Infer(save_result=False)

    def _init_(self):
        self._init_status_()
        self.move_handle = move_handle
        self.skill_handle = skill_handle
        self.skill_upgrade_handle = skill_upgrade_handle
        self.threez_handle = threez_handle
        self.shopping_handle = shopping_handle
        self.map_handel = map_handel
        self.observation_space = np.zeros((439, 960, 3))
        self.reward = 0.0
        self.img_steps = 0
        self.done = False

    def _init_status_(self):
        self.status = []
        for c in categories:
            ca = dict()
            ca['id'] = c['id']
            ca['name'] = c['name']
            ca['reward'] = c['reward']
            self.status.append(ca)

    def _get_imgfile(self):
        img_file = self.img_dir  + self.img_files[self.img_steps]
        self.img_steps += 1
        if self.img_steps >= len(self.img_files):
            self.done = True
        return img_file

    def reset(self):
        self._init_()
        return self.observation_space

    def set_reward(self,state_name,reward):
        for c in self.status:
            if c['name'] == state_name:
                c['reward'] = reward
                break

    def _handle_actions_(self,actions):
        if not self.scrypt:
            img_path = self._get_imgfile()
            return img_path
        else:
            # todo 接入scrypt
            pass

    def _step_info_(self,actions):
        img = self._handle_actions_(actions)
        r = self.infer.infer(img)
        self.observation_space = Image.open(img).convert('RGB')
        reward = 0.0
        for dt in r:
            clsid, bbox, score = int(dt[0]), dt[2:], dt[1]
            xmin, ymin, xmax, ymax = bbox
            c_index = 0
            for c in self.status:
                if c["id"] == clsid:
                    reward += c['reward']
                    if c['name'] == 'victory' or c['name'] == 'defeated':
                        self.done = True
                    break
                c_index += 1
        return self.observation_space, reward, self.done

    def _select_random_level(self):
        pass

    def step(self, actions):
        abs, reward, done = self._step_info_(actions)
        self.reward += reward
        return abs, self.reward, done, {}

    def seed(self, seed=None):
        if seed is None:
            return []
        # set the random number seed for the NumPy random number generator
        self.np_random.seed(seed)
        # return the list of seeds used by RNG(s) in the environment
        return [seed]

    def close(self):

        if self.env is None:
            raise ValueError('env has already been closed.')
        # iterate over each list of stages
        for stage_lists in self.envs:
            # iterate over each stage
            for stage in stage_lists:
                # close the environment
                stage.close()

        self.env = None
        if self.viewer is not None:
            self.viewer.close()

    def render(self, mode='human'):
        if mode == 'human':
            # if the viewer isn't setup, import it and create one
            if self.viewer is None:
                from nes_py._image_viewer import ImageViewer
                # get the caption for the ImageViewer
                # create the ImageViewer to display frames
                self.viewer = ImageViewer(
                    caption=self.__class__.__name__,
                    height=SCREEN_HEIGHT,
                    width=SCREEN_WIDTH,
                )
            # show the screen on the image viewer
            self.viewer.show(self.env.screen)
        elif mode == 'rgb_array':
            return self.env.screen
        else:
            # unpack the modes as comma delineated strings ('a', 'b', ...)
            render_modes = [repr(x) for x in self.metadata['render.modes']]
            msg = 'valid render modes are: {}'.format(', '.join(render_modes))
            raise NotImplementedError(msg)

    def get_keys_to_action(self):
        """Return the dictionary of keyboard keys to actions."""
        return self.env.get_keys_to_action()

    def get_action_meanings(self):
        """Return the list of strings describing the action space actions."""
        return self.env.get_action_meanings()
