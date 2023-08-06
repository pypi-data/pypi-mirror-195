# Author: xuejinlin
# Date: 2023/3/7 22:50
from gym.envs.registration import register

register(
    id="hero_key_env-v0",
    entry_point='hero_key_env:HeroKeyEnv',
    max_episode_steps=9999999,
    reward_threshold=9999999,
    nondeterministic=True,
)

