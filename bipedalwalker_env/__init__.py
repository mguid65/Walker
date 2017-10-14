from gym.envs.registration import register

register(
    id='BiPedalWalker-v0',
    entry_point='bipedalwalker_env.bipedal_walker:BipedalWalker',
)
