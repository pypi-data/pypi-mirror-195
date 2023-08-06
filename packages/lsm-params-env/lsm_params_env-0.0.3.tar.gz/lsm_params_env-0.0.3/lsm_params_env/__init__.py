from gym.envs.registration import register

register(
    id='lsm_params_env',
    entrypoints='lsm_params_env.envs:ParamsEnv'
)