from stable_baselines3 import PPO
import os
import time
from pump_env import PumpEnv

models_dir = f"models/{int(time.time())}"
logs_dir = f"logs/{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Environment
env = PumpEnv(goal_pressure_range=[1.1, 4.0])  # Set goal pressure range
# env = make_vec_env(lambda: env, n_envs=1)  # Multi-process (This behaves like batchsize)
env.reset()

# Model
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logs_dir)

# Train and save every TIMESTEPS steps
TIMESTEPS = 10000
for i in range(1,1000000000):
    # Turn off "reset_num_timesteps" so that the learning won't stop
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", progress_bar=True)
    
    # Save the model every {TIMESTEPS} steps
    model.save(f"{models_dir}/{TIMESTEPS*i}")



env.close()


# Note on tensorboard
# Command line: tensorboard --logdir=logs
# Then copy paste the link to your browser