from gym.envs.registration import register

register(
    id='ship_env-v0',
    entry_point='ship_env.envs:ShipEnv',

)